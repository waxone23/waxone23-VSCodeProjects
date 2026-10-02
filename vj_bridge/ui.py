"""Main window: device/OSC setup, live meters + history, mapping and band editors, presets."""

from __future__ import annotations

import sys
import time
from collections import deque
from pathlib import Path

import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import QRectF, QSettings, Qt, QTimer, QUrl
from PySide6.QtGui import QAction, QColor, QDesktopServices, QFont, QIcon, QKeySequence, QPainter
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from . import __version__
from .audio import list_input_devices
from .config import KICK_PULSE, MANUAL, PRESET_DIR, Band, Mapping, MidiBinding, Preset, Settings, save_settings
from .engine import Engine
from .midi_in import MIDI_NONE, MidiInput, list_midi_inputs, pick_default_port
from .resources import asset_path
from .theme import AMBER, BG, GREEN, MUTED, RED

COLORS = ["#ff5d73", "#ffb347", "#5dd39e", "#5db0ff", "#c07bff", "#ff8fd0"]
HISTORY = 300  # ~5 s at 60 fps
LOOPBACK_HINTS = ("blackhole", "cable output", "vb-audio", "loopback", "soundflower", "voicemeeter")
NO_SIGNAL_AFTER_S = 4.0
LEARN_TIMEOUT_S = 15.0

pg.setConfigOptions(antialias=True, background=BG, foreground="#8b8b96")


def _spin(value: float, lo: float, hi: float, step: float, decimals: int = 2, suffix: str = "") -> QDoubleSpinBox:
    spin = QDoubleSpinBox()
    spin.setRange(lo, hi)
    spin.setDecimals(decimals)
    spin.setSingleStep(step)
    spin.setKeyboardTracking(False)
    if suffix:
        spin.setSuffix(suffix)
    spin.setValue(value)
    return spin


def guide_html() -> str:
    if sys.platform == "darwin":
        route = (
            "<li>Install <b>BlackHole 2ch</b> (free loopback driver).</li>"
            "<li>Open <i>Audio MIDI Setup</i> and create a <b>Multi-Output Device</b> containing your "
            "speakers/headphones <b>and</b> BlackHole 2ch. This lets you hear the music while VJ Bridge listens.</li>"
            "<li>In Ableton: <i>Settings → Audio → Output Device</i> → choose that Multi-Output Device.</li>"
            "<li>In VJ Bridge, choose <b>BlackHole 2ch</b> as the input.</li>"
        )
        perm = "<li>macOS will ask for microphone access the first time. Allow it (BlackHole counts as a microphone).</li>"
    elif sys.platform == "win32":
        route = (
            "<li>Install <b>VB-Cable</b> (free virtual audio cable).</li>"
            "<li>In Ableton: <i>Settings → Audio → Output Device</i> → <b>CABLE Input</b> "
            "(use the same driver type as your normal output, e.g. WASAPI).</li>"
            "<li>To keep hearing the music: Windows <i>Sound settings → Recording → CABLE Output → Properties → "
            "Listen → Listen to this device</i> and pick your speakers.</li>"
            "<li>In VJ Bridge, choose <b>CABLE Output</b> as the input.</li>"
        )
        perm = ""
    else:
        route = "<li>Route Ableton's output to a loopback/monitor source and choose it as the input here.</li>"
        perm = ""
    return (
        "<h3>Quick setup</h3>"
        "<ol>"
        f"{route}"
        "<li>In Resolume: <i>Preferences → OSC</i> → enable <b>OSC Input</b> (port 7000 by default).</li>"
        "<li>Press <b>Start</b>. The meters should move when Ableton plays.</li>"
        "<li>In <b>Mappings</b>, set each row's OSC address to a real Resolume parameter "
        "(Resolume: Shortcuts edit mode shows a parameter's OSC address). Use <b>Test</b> to check it.</li>"
        "<li><b>APC40 knobs (optional):</b> put the APC40 in Generic mode (in Ableton's MIDI settings set its "
        "control surface to <i>None</i>, then replug it). In the Mappings tab choose it under <i>Controller</i>, "
        "click <b>Learn…</b> on a row and move a knob. That knob now sets how strongly the music drives that "
        "parameter. Use the <b>manual</b> source for direct control.</li>"
        f"{perm}"
        "</ol>"
        "<p style='color:#8b8b96'>Reopen this guide any time from <i>Help → Setup guide</i>.</p>"
    )


class GuideDialog(QDialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setWindowTitle("Setup guide")
        self.setMinimumWidth(560)
        layout = QVBoxLayout(self)
        label = QLabel(guide_html())
        label.setTextFormat(Qt.TextFormat.RichText)
        label.setWordWrap(True)
        layout.addWidget(label)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)


class KnobButton(QPushButton):
    """Shows a row's MIDI assignment; click it, then move a knob to (re)assign."""

    def __init__(self, binding: MidiBinding | None) -> None:
        super().__init__()
        self.binding = binding
        self.refresh()

    def set_binding(self, binding: MidiBinding | None) -> None:
        self.binding = binding
        self.refresh()

    def refresh(self) -> None:
        self.setText(self.binding.label() if self.binding else "Learn…")
        self.setToolTip("Click, then move a knob or fader on your controller to assign it to this row's Amount")


class MeterPanel(QWidget):
    """Level bars with peak-hold markers and percentages, colour-matched to the history plot."""

    def __init__(self) -> None:
        super().__init__()
        self.names: list[str] = []
        self.values: dict[str, float] = {}
        self.peaks: dict[str, float] = {}
        self.idle = True
        self.setMinimumHeight(150)

    def set_names(self, names: list[str]) -> None:
        self.names = names
        self.peaks = {}
        self.update()

    def set_idle(self, idle: bool) -> None:
        if idle != self.idle:
            self.idle = idle
            self.update()

    def set_values(self, values: dict[str, float]) -> None:
        self.values = values
        for name in self.names:
            self.peaks[name] = max(values.get(name, 0.0), self.peaks.get(name, 0.0) - 0.008)
        self.update()

    def paintEvent(self, _event: object) -> None:
        if not self.names:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        row_h = self.height() / len(self.names)
        label_w, value_w = 84, 46
        for i, name in enumerate(self.names):
            y = i * row_h + 5
            h = row_h - 10
            track = QRectF(label_w, y, self.width() - label_w - value_w - 8, h)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(42, 42, 50))
            painter.drawRoundedRect(track, 5, 5)

            level = max(0.0, min(self.values.get(name, 0.0), 1.0))
            color = QColor(COLORS[i % len(COLORS)])
            if level > 0.8:
                color = color.lighter(125)  # brighten on hard hits
            painter.setBrush(color)
            painter.drawRoundedRect(QRectF(track.x(), track.y(), max(track.width() * level, 0), track.height()), 5, 5)

            peak = max(0.0, min(self.peaks.get(name, 0.0), 1.0))
            if peak > 0.02:
                px = track.x() + track.width() * peak
                painter.setBrush(QColor(255, 255, 255, 170))
                painter.drawRoundedRect(QRectF(px - 1.5, track.y() + 2, 3, track.height() - 4), 1.5, 1.5)

            painter.setPen(QColor(200, 200, 208))
            painter.drawText(
                QRectF(0, y, label_w - 10, h),
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                name,
            )
            painter.setPen(QColor(139, 139, 150))
            painter.drawText(
                QRectF(track.right() + 6, y, value_w - 6, h),
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                f"{int(level * 100)}%",
            )

        if self.idle:
            painter.fillRect(self.rect(), QColor(31, 31, 37, 200))
            painter.setPen(QColor(200, 200, 208))
            font = QFont(self.font())
            font.setPointSize(font.pointSize() + 2)
            painter.setFont(font)
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Press Start to begin")


class MainWindow(QMainWindow):
    AMOUNT_COL = 6
    KNOB_COL = 7
    LIVE_COL = 8

    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self.settings = settings
        self.engine = Engine(settings)
        self._loading = False
        self._frame = 0
        self._device_name = ""
        self._last_signal = time.monotonic()
        self._signal_warned = False
        self._learn_button: KnobButton | None = None
        self._learn_row = -1
        self._learn_started = 0.0
        self.midi_input = MidiInput(self.engine.midi)
        self.history: dict[str, deque[float]] = {}
        self.curves: dict[str, pg.PlotDataItem] = {}

        self.setWindowTitle("VJ Bridge")
        self.setWindowIcon(QIcon(asset_path("icon.png")))
        self.setMinimumSize(1020, 640)
        self._build_menu()
        self._build_ui()
        self._refresh_devices()
        self._refresh_presets()
        self._refresh_midi()
        self._populate_bands()
        self._populate_mappings()
        self._rebuild_visuals()
        self._set_running_ui(False)

        geometry = QSettings("VJBridge", "VJBridge").value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        else:
            self.resize(1260, 800)

        self.timer = QTimer(self)
        self.timer.setInterval(16)
        self.timer.timeout.connect(self._tick)
        self.timer.start()

    # ------------------------------------------------------------------ layout

    @property
    def source_names(self) -> list[str]:
        return [b.name for b in self.settings.preset.bands] + [KICK_PULSE]

    @property
    def mapping_sources(self) -> list[str]:
        return self.source_names + [MANUAL]

    def _build_menu(self) -> None:
        def add(menu, text: str, slot, shortcut: str | None = None) -> None:
            action = QAction(text, self)
            if shortcut:
                action.setShortcut(QKeySequence(shortcut))
            action.triggered.connect(slot)
            menu.addAction(action)

        file_menu = self.menuBar().addMenu("&File")
        add(file_menu, "Start / Stop", self._toggle, "Ctrl+Return")
        file_menu.addSeparator()
        add(file_menu, "Save preset…", self._save_preset, "Ctrl+S")
        add(file_menu, "Open presets folder", self._open_presets_folder)
        file_menu.addSeparator()
        add(file_menu, "Quit", self.close, "Ctrl+Q")

        help_menu = self.menuBar().addMenu("&Help")
        add(help_menu, "Setup guide", self._show_guide)
        add(help_menu, "About VJ Bridge", self._show_about)

    def _build_ui(self) -> None:
        root = QWidget()
        layout = QVBoxLayout(root)
        layout.setContentsMargins(14, 10, 14, 14)
        layout.setSpacing(10)

        header = QHBoxLayout()
        header.setSpacing(8)
        header.addWidget(self._muted("Input"))
        self.device_combo = QComboBox()
        self.device_combo.setMinimumWidth(250)
        self.device_combo.setToolTip("The audio source to analyse. Choose your loopback device (BlackHole / CABLE Output).")
        header.addWidget(self.device_combo)
        refresh = QPushButton("↻")
        refresh.setFixedWidth(36)
        refresh.setToolTip("Rescan audio devices")
        refresh.clicked.connect(self._refresh_devices)
        header.addWidget(refresh)

        header.addSpacing(14)
        header.addWidget(self._muted("Resolume"))
        self.ip_edit = QLineEdit(self.settings.resolume_ip)
        self.ip_edit.setFixedWidth(118)
        self.ip_edit.setToolTip("IP address of the machine running Resolume (127.0.0.1 = this computer)")
        self.ip_edit.textChanged.connect(lambda t: setattr(self.settings, "resolume_ip", t.strip()))
        header.addWidget(self.ip_edit)
        self.port_spin = QSpinBox()
        self.port_spin.setRange(1, 65535)
        self.port_spin.setValue(self.settings.resolume_port)
        self.port_spin.setToolTip("Resolume OSC input port (Preferences → OSC)")
        self.port_spin.valueChanged.connect(lambda v: setattr(self.settings, "resolume_port", v))
        header.addWidget(self.port_spin)

        header.addSpacing(14)
        header.addWidget(self._muted("Preset"))
        self.preset_combo = QComboBox()
        self.preset_combo.setMinimumWidth(150)
        self.preset_combo.setToolTip("Switch between saved mapping sets")
        self.preset_combo.currentIndexChanged.connect(self._on_preset_chosen)
        header.addWidget(self.preset_combo)
        save_button = QPushButton("Save…")
        save_button.setToolTip("Save the current bands and mappings as a preset (Ctrl+S)")
        save_button.clicked.connect(self._save_preset)
        header.addWidget(save_button)

        header.addStretch()
        self.status = QLabel()
        header.addWidget(self.status)
        self.start_button = QPushButton("Start")
        self.start_button.setObjectName("startButton")
        self.start_button.setMinimumWidth(110)
        self.start_button.setToolTip("Start / stop listening (Ctrl+Enter)")
        self.start_button.clicked.connect(self._toggle)
        header.addWidget(self.start_button)
        layout.addLayout(header)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self._build_left())
        splitter.addWidget(self._build_tabs())
        splitter.setStretchFactor(0, 4)
        splitter.setStretchFactor(1, 7)
        splitter.setChildrenCollapsible(False)
        layout.addWidget(splitter, 1)
        self.setCentralWidget(root)

    @staticmethod
    def _muted(text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("muted")
        return label

    def _build_left(self) -> QWidget:
        panel = QWidget()
        box = QVBoxLayout(panel)
        box.setContentsMargins(0, 0, 0, 0)

        levels = QGroupBox("Levels")
        lv = QVBoxLayout(levels)
        self.meters = MeterPanel()
        lv.addWidget(self.meters)
        box.addWidget(levels, 2)

        history = QGroupBox("Last 5 seconds")
        hv = QVBoxLayout(history)
        self.plot = pg.PlotWidget()
        self.plot.setYRange(0, 1.05, padding=0)
        self.plot.setMouseEnabled(False, False)
        self.plot.setMenuEnabled(False)
        self.plot.hideAxis("bottom")
        self.plot.showGrid(y=True, alpha=0.12)
        self.plot.setFrameShape(QFrame.Shape.NoFrame)
        hv.addWidget(self.plot)
        box.addWidget(history, 3)
        return panel

    def _build_tabs(self) -> QWidget:
        tabs = QTabWidget()
        tabs.addTab(self._build_mappings_tab(), "Mappings")
        tabs.addTab(self._build_bands_tab(), "Bands")
        tabs.addTab(self._build_monitor_tab(), "OSC monitor")
        return tabs

    def _build_mappings_tab(self) -> QWidget:
        page = QWidget()
        mv = QVBoxLayout(page)
        mv.setContentsMargins(0, 6, 0, 0)
        midi_row = QHBoxLayout()
        midi_row.addWidget(self._muted("Controller"))
        self.midi_combo = QComboBox()
        self.midi_combo.setMinimumWidth(210)
        self.midi_combo.setToolTip("MIDI controller for knob control (APC40 is picked automatically if found)")
        self.midi_combo.currentIndexChanged.connect(self._on_midi_chosen)
        midi_row.addWidget(self.midi_combo)
        midi_rescan = QPushButton("↻")
        midi_rescan.setFixedWidth(36)
        midi_rescan.setToolTip("Rescan MIDI devices")
        midi_rescan.clicked.connect(self._refresh_midi)
        midi_row.addWidget(midi_rescan)
        self.midi_status = QLabel()
        midi_row.addWidget(self.midi_status)
        midi_row.addStretch()
        mv.addLayout(midi_row)
        self.map_table = QTableWidget(0, 9)
        self.map_table.setHorizontalHeaderLabels(
            ["On", "Source", "OSC address", "Min", "Max", "Curve", "Amount", "Knob", "Live"]
        )
        self.map_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.map_table.setAlternatingRowColors(True)
        self.map_table.setShowGrid(False)
        self.map_table.verticalHeader().setVisible(False)
        self.map_table.verticalHeader().setDefaultSectionSize(40)
        hh = self.map_table.horizontalHeader()
        hh.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        for col in (0, 1, 3, 4, 5, 6, 7):
            hh.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(self.LIVE_COL, QHeaderView.ResizeMode.Fixed)
        self.map_table.setColumnWidth(self.LIVE_COL, 64)
        self.map_table.itemChanged.connect(self._on_mappings_changed)
        mv.addWidget(self.map_table)

        buttons = QHBoxLayout()
        for text, slot, tip in (
            ("Add", self._add_mapping, "Add a mapping row"),
            ("Remove", self._remove_mapping, "Remove the selected row"),
            ("Unassign knob", self._clear_knob, "Remove the knob assignment from the selected row"),
            ("Test", self._test_mapping, "Send Max, then Min half a second later, to the selected row's address"),
        ):
            button = QPushButton(text)
            button.setToolTip(tip)
            button.clicked.connect(slot)
            buttons.addWidget(button)
        buttons.addStretch()
        mv.addLayout(buttons)
        hint = self._muted(
            "Each row turns one sound source into one Resolume parameter. Amount is how strongly the sound drives it; "
            "assign a knob to ride it live. Source 'manual' makes the knob control the parameter directly. "
            "Knobs only act while VJ Bridge is started. 'Live' shows the value being sent."
        )
        hint.setWordWrap(True)
        mv.addWidget(hint)
        return page

    def _build_bands_tab(self) -> QWidget:
        page = QWidget()
        bv = QVBoxLayout(page)
        bv.setContentsMargins(0, 6, 0, 0)
        self.band_table = QTableWidget(0, 5)
        self.band_table.setHorizontalHeaderLabels(["Band", "Low", "High", "Attack", "Release"])
        self.band_table.setShowGrid(False)
        self.band_table.setAlternatingRowColors(True)
        self.band_table.verticalHeader().setVisible(False)
        self.band_table.verticalHeader().setDefaultSectionSize(40)
        self.band_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        bv.addWidget(self.band_table)

        onset = QGroupBox("Kick pulse")
        ov = QHBoxLayout(onset)
        ov.addWidget(QLabel("Sensitivity"))
        self.thresh_spin = _spin(self.settings.preset.onset_threshold, 0.05, 1.0, 0.05)
        self.thresh_spin.setToolTip("How sharply the kick band must rise to count as a hit. Lower = more sensitive.")
        self.thresh_spin.valueChanged.connect(self._on_onset_changed)
        ov.addWidget(self.thresh_spin)
        ov.addWidget(QLabel("Cooldown"))
        self.cooldown_spin = _spin(self.settings.preset.onset_cooldown, 0.05, 0.5, 0.01, 2, " s")
        self.cooldown_spin.setToolTip("Minimum time between detected hits. Raise it if fast hats retrigger the pulse.")
        self.cooldown_spin.valueChanged.connect(self._on_onset_changed)
        ov.addWidget(self.cooldown_spin)
        ov.addStretch()
        bv.addWidget(onset)
        hint = self._muted("Attack = how fast a band reacts. Release = how slowly it falls back. Changes apply instantly.")
        hint.setWordWrap(True)
        bv.addWidget(hint)
        return page

    def _build_monitor_tab(self) -> QWidget:
        page = QWidget()
        mov = QVBoxLayout(page)
        mov.setContentsMargins(0, 6, 0, 0)
        self.monitor_table = QTableWidget(0, 2)
        self.monitor_table.setHorizontalHeaderLabels(["Address", "Last value"])
        self.monitor_table.setShowGrid(False)
        self.monitor_table.setAlternatingRowColors(True)
        self.monitor_table.verticalHeader().setVisible(False)
        self.monitor_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.monitor_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        mov.addWidget(self.monitor_table)
        return page

    # ------------------------------------------------------------------ devices & presets

    def _refresh_devices(self) -> None:
        self.device_combo.blockSignals(True)
        self.device_combo.clear()
        self.device_combo.addItem("System default", None)
        labels: list[str] = []
        try:
            labels = [label for _index, label in list_input_devices()]
        except Exception as exc:  # PortAudio problems shouldn't kill the window
            self._set_status(f"Device scan failed: {exc}", "error")
        for label in labels:
            self.device_combo.addItem(label, label)

        position = self.device_combo.findData(self.settings.device)
        if position < 0:
            # First run or device gone: prefer an obvious loopback device over the mic.
            for i, label in enumerate(labels, start=1):
                if any(hint in label.lower() for hint in LOOPBACK_HINTS):
                    position = i
                    break
        self.device_combo.setCurrentIndex(max(position, 0))
        self.device_combo.blockSignals(False)

    def _refresh_presets(self, select: str | None = None) -> None:
        PRESET_DIR.mkdir(parents=True, exist_ok=True)
        combo = self.preset_combo
        combo.blockSignals(True)
        combo.clear()
        combo.addItem("Default", None)
        for path in sorted(PRESET_DIR.glob("*.json")):
            combo.addItem(path.stem, str(path))
        wanted = select or self.settings.preset_name or "Default"
        combo.setCurrentIndex(max(combo.findText(wanted), 0))
        combo.blockSignals(False)

    def _on_preset_chosen(self, index: int) -> None:
        path = self.preset_combo.itemData(index)
        if path is None:
            self.settings.preset = Preset()
            self.settings.preset_name = None
        else:
            try:
                self.settings.preset = Preset.model_validate_json(Path(path).read_text())
            except (OSError, ValueError) as exc:
                QMessageBox.warning(self, "Couldn't load preset", str(exc))
                self._refresh_presets()
                return
            self.settings.preset_name = Path(path).stem
        self._reload_preset_ui()

    def _save_preset(self) -> None:
        name, ok = QInputDialog.getText(self, "Save preset", "Preset name:", text=self.settings.preset_name or "")
        if not ok:
            return
        safe = "".join(c for c in name.strip() if c.isalnum() or c in " -_")[:60].strip()
        if not safe:
            return
        PRESET_DIR.mkdir(parents=True, exist_ok=True)
        path = PRESET_DIR / f"{safe}.json"
        if path.exists() and safe != self.settings.preset_name:
            answer = QMessageBox.question(self, "Overwrite preset?", f"'{safe}' already exists. Overwrite it?")
            if answer != QMessageBox.StandardButton.Yes:
                return
        path.write_text(self.settings.preset.model_dump_json(indent=2))
        self.settings.preset_name = safe
        self._refresh_presets(safe)

    def _open_presets_folder(self) -> None:
        PRESET_DIR.mkdir(parents=True, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(PRESET_DIR)))

    def _reload_preset_ui(self) -> None:
        self.engine.rebuild_analyzer()
        self._populate_bands()
        self._populate_mappings()
        self._rebuild_visuals()

    # ------------------------------------------------------------------ populate tables

    def _populate_bands(self) -> None:
        self._loading = True
        preset = self.settings.preset
        table = self.band_table
        table.setRowCount(len(preset.bands))
        for row, band in enumerate(preset.bands):
            name_item = QTableWidgetItem(band.name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            table.setItem(row, 0, name_item)
            cells = (
                (1, band.low_hz, 20, 20000, 10, " Hz"),
                (2, band.high_hz, 20, 20000, 10, " Hz"),
                (3, band.attack * 1000, 1, 500, 1, " ms"),
                (4, band.release * 1000, 10, 2000, 10, " ms"),
            )
            for col, value, lo, hi, step, suffix in cells:
                spin = _spin(value, lo, hi, step, 0, suffix)
                spin.valueChanged.connect(self._on_bands_changed)
                table.setCellWidget(row, col, spin)
        self.thresh_spin.setValue(preset.onset_threshold)
        self.cooldown_spin.setValue(preset.onset_cooldown)
        self._loading = False

    def _populate_mappings(self) -> None:
        self._cancel_learn()
        self._loading = True
        self.map_table.setRowCount(0)
        for mapping in self.settings.preset.mappings:
            self._add_mapping_row(mapping)
        self._loading = False

    def _add_mapping_row(self, mapping: Mapping) -> None:
        was_loading = self._loading
        self._loading = True  # row is built piecemeal; don't read it back yet
        table = self.map_table
        row = table.rowCount()
        table.insertRow(row)

        enabled = QCheckBox()
        enabled.setChecked(mapping.enabled)
        enabled.setToolTip("Turn this mapping on or off")
        enabled.toggled.connect(self._on_mappings_changed)
        table.setCellWidget(row, 0, enabled)

        source = QComboBox()
        source.addItems(self.mapping_sources)
        source.setCurrentText(mapping.source)
        source.currentTextChanged.connect(self._on_mappings_changed)
        table.setCellWidget(row, 1, source)

        table.setItem(row, 2, QTableWidgetItem(mapping.address))

        for col, value, lo, hi, step in (
            (3, mapping.out_min, -100000, 100000, 0.05),
            (4, mapping.out_max, -100000, 100000, 0.05),
            (5, mapping.curve, 0.1, 10, 0.1),
        ):
            spin = _spin(value, lo, hi, step)
            spin.valueChanged.connect(self._on_mappings_changed)
            table.setCellWidget(row, col, spin)

        amount = _spin(mapping.amount, 0.0, 1.0, 0.05)
        amount.setToolTip("How strongly the sound drives this parameter (0 = not at all, 1 = fully). Mirrors the knob if one is assigned.")
        amount.setEnabled(mapping.knob is None)
        amount.valueChanged.connect(self._on_mappings_changed)
        table.setCellWidget(row, self.AMOUNT_COL, amount)

        knob = KnobButton(mapping.knob)
        knob.clicked.connect(lambda _checked=False, b=knob: self._start_learn(b))
        table.setCellWidget(row, self.KNOB_COL, knob)

        live = QTableWidgetItem("–")
        live.setFlags(live.flags() & ~Qt.ItemFlag.ItemIsEditable)
        live.setForeground(QColor(MUTED))
        live.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        table.setItem(row, self.LIVE_COL, live)
        self._loading = was_loading

    def _rebuild_visuals(self) -> None:
        names = self.source_names
        self.meters.set_names(names)
        self.plot.clear()
        self.history = {n: deque([0.0] * HISTORY, maxlen=HISTORY) for n in names}
        self.curves = {
            n: self.plot.plot(pen=pg.mkPen(COLORS[i % len(COLORS)], width=2)) for i, n in enumerate(names)
        }

    # ------------------------------------------------------------------ edits -> settings

    def _read_mappings(self) -> list[Mapping]:
        table = self.map_table
        out: list[Mapping] = []
        for row in range(table.rowCount()):
            item = table.item(row, 2)
            out.append(
                Mapping(
                    enabled=table.cellWidget(row, 0).isChecked(),
                    source=table.cellWidget(row, 1).currentText(),
                    address=item.text().strip() if item else "",
                    out_min=table.cellWidget(row, 3).value(),
                    out_max=table.cellWidget(row, 4).value(),
                    curve=table.cellWidget(row, 5).value(),
                    amount=table.cellWidget(row, self.AMOUNT_COL).value(),
                    knob=table.cellWidget(row, self.KNOB_COL).binding,
                )
            )
        return out

    def _on_mappings_changed(self, *_args: object) -> None:
        if not self._loading:
            self.settings.preset.mappings = self._read_mappings()

    def _add_mapping(self) -> None:
        mapping = Mapping(source=self.source_names[0], address="/composition/layers/1/video/opacity")
        self._add_mapping_row(mapping)
        self.map_table.selectRow(self.map_table.rowCount() - 1)
        self._on_mappings_changed()

    def _remove_mapping(self) -> None:
        row = self.map_table.currentRow()
        if row >= 0:
            self._cancel_learn()
            self.map_table.removeRow(row)
            self._on_mappings_changed()

    def _test_mapping(self) -> None:
        row = self.map_table.currentRow()
        if row < 0:
            self._set_status("Select a mapping row first, then press Test", "warn")
            return
        mapping = self._read_mappings()[row]
        if not mapping.address.startswith("/"):
            self._set_status("OSC addresses start with '/', e.g. /composition/layers/1/video/opacity", "warn")
            return
        self.engine.osc.set_target(self.settings.resolume_ip, self.settings.resolume_port)
        self.engine.osc.send(mapping.address, mapping.out_max)
        QTimer.singleShot(500, lambda: self.engine.osc.send(mapping.address, mapping.out_min))

    def _on_bands_changed(self, *_args: object) -> None:
        if self._loading:
            return
        table = self.band_table
        bands: list[Band] = []
        for row in range(table.rowCount()):
            low = table.cellWidget(row, 1).value()
            high = table.cellWidget(row, 2).value()
            if low >= high:
                return  # invalid while mid-edit; wait for a valid range
            bands.append(
                Band(
                    name=table.item(row, 0).text(),
                    low_hz=low,
                    high_hz=high,
                    attack=table.cellWidget(row, 3).value() / 1000,
                    release=table.cellWidget(row, 4).value() / 1000,
                )
            )
        self.settings.preset.bands = bands
        self.engine.rebuild_analyzer()

    def _on_onset_changed(self, *_args: object) -> None:
        if self._loading:
            return
        self.settings.preset.onset_threshold = self.thresh_spin.value()
        self.settings.preset.onset_cooldown = self.cooldown_spin.value()
        self.engine.update_onset()

    # ------------------------------------------------------------------ MIDI controller

    def _set_midi_status(self, text: str, kind: str = "ok") -> None:
        color = {"ok": GREEN, "warn": AMBER, "error": RED, "idle": MUTED}[kind]
        self.midi_status.setText(f"● {text}")
        self.midi_status.setStyleSheet(f"color: {color};")

    def _refresh_midi(self) -> None:
        combo = self.midi_combo
        combo.blockSignals(True)
        combo.clear()
        combo.addItem("None", MIDI_NONE)
        ports: list[str] = []
        error: str | None = None
        try:
            ports = list_midi_inputs()
        except Exception as exc:
            error = f"MIDI unavailable: {exc}"
        for port in ports:
            combo.addItem(port, port)
        position = combo.findData(self.settings.midi_device) if self.settings.midi_device else -1
        if position < 0 and self.settings.midi_device is None:
            wanted = pick_default_port(ports)  # never chosen before: look for an APC40
            position = combo.findData(wanted) if wanted else -1
        combo.setCurrentIndex(max(position, 0))
        combo.blockSignals(False)
        self._apply_midi_selection(interactive=False)
        if error:
            self._set_midi_status(error, "error")

    def _on_midi_chosen(self, index: int) -> None:
        self.settings.midi_device = self.midi_combo.itemData(index)
        self._apply_midi_selection(interactive=True)

    def _apply_midi_selection(self, interactive: bool) -> None:
        self._cancel_learn()
        self.midi_input.close()
        name = self.midi_combo.currentData()
        if not name or name == MIDI_NONE:
            self._set_midi_status("No controller selected", "idle")
            return
        try:
            self.midi_input.open(name)
        except Exception as exc:
            self._set_midi_status("Couldn't open this MIDI port", "error")
            if interactive:
                QMessageBox.warning(
                    self,
                    "Couldn't open the MIDI port",
                    "Another app (Ableton or Resolume) is probably using this controller. On Windows a MIDI "
                    "port can only be opened by one app at a time: switch off the controller's Track/Remote "
                    "ports in Ableton's MIDI settings, or route it through a virtual port such as loopMIDI.\n\n"
                    f"Details: {exc}",
                )
            return
        self._set_midi_status(f"Connected · {name}", "ok")

    def _row_of(self, widget: QWidget, col: int) -> int:
        for row in range(self.map_table.rowCount()):
            if self.map_table.cellWidget(row, col) is widget:
                return row
        return -1

    def _restore_status(self) -> None:
        if not self.engine.running:
            self._set_status("Stopped", "idle")
        elif self._signal_warned:
            self._set_status("No audio signal: check Ableton's output routing", "warn")
        else:
            self._set_status(f"Listening · {self._device_name}", "ok")

    def _start_learn(self, button: KnobButton) -> None:
        if self._learn_button is button:
            self._cancel_learn()  # second click cancels
            return
        if not self.midi_input.is_open:
            self._set_status("Pick a MIDI controller first (top of the Mappings tab)", "warn")
            return
        self._cancel_learn()
        self._learn_button = button
        self._learn_row = self._row_of(button, self.KNOB_COL)
        self._learn_started = time.monotonic()
        button.setText("Move a knob…")
        self.engine.midi.start_learn()
        self._set_status("Move a knob or fader on your controller…", "warn")

    def _cancel_learn(self) -> None:
        button = self._learn_button
        if button is None:
            return
        self._learn_button = None
        self.engine.midi.cancel_learn()
        button.refresh()
        self._restore_status()

    def _poll_learn(self) -> None:
        binding = self.engine.midi.pop_learned()
        if binding is not None:
            button, row = self._learn_button, self._learn_row
            self._learn_button = None
            if button is not None:
                button.set_binding(binding)
                self._sync_amount_enabled(row)
                self._on_mappings_changed()
            self._restore_status()
        elif time.monotonic() - self._learn_started > LEARN_TIMEOUT_S:
            self._cancel_learn()

    def _sync_amount_enabled(self, row: int) -> None:
        """A knob-bound row's Amount box is read-only: it just mirrors the knob."""
        if row < 0:
            return
        knob = self.map_table.cellWidget(row, self.KNOB_COL)
        spin = self.map_table.cellWidget(row, self.AMOUNT_COL)
        if knob is not None and spin is not None:
            spin.setEnabled(knob.binding is None)

    def _clear_knob(self) -> None:
        row = self.map_table.currentRow()
        if row < 0:
            self._set_status("Select a mapping row first", "warn")
            return
        self._cancel_learn()
        button = self.map_table.cellWidget(row, self.KNOB_COL)
        button.set_binding(None)
        self._sync_amount_enabled(row)
        self._on_mappings_changed()

    def _update_knob_column(self) -> None:
        table = self.map_table
        was_loading = self._loading
        self._loading = True  # mirroring the knob must not look like a user edit
        for row in range(table.rowCount()):
            button = table.cellWidget(row, self.KNOB_COL)
            spin = table.cellWidget(row, self.AMOUNT_COL)
            if button is None or spin is None or button.binding is None:
                continue
            value = self.engine.midi.value(button.binding)
            if value is not None and abs(spin.value() - value) > 0.004:
                spin.setValue(value)
        self._loading = was_loading

    # ------------------------------------------------------------------ help

    def maybe_show_first_run(self) -> None:
        if not self.settings.first_run_done:
            self.settings.first_run_done = True
            self._show_guide()

    def _show_guide(self) -> None:
        GuideDialog(self).exec()

    def _show_about(self) -> None:
        QMessageBox.about(
            self,
            "About VJ Bridge",
            f"<b>VJ Bridge</b> {__version__}<br>Audio-reactive link between Ableton Live and Resolume Avenue.",
        )

    # ------------------------------------------------------------------ run / stop

    def _set_status(self, text: str, kind: str = "ok") -> None:
        color = {"ok": GREEN, "warn": AMBER, "error": RED, "idle": MUTED}[kind]
        self.status.setText(f"● {text}")
        self.status.setStyleSheet(f"color: {color};")

    def _set_running_ui(self, running: bool, device: str = "") -> None:
        self._device_name = device
        self.start_button.setText("Stop" if running else "Start")
        self.start_button.setProperty("running", running)
        self.start_button.style().unpolish(self.start_button)
        self.start_button.style().polish(self.start_button)
        self.device_combo.setEnabled(not running)
        self.meters.set_idle(not running)
        if running:
            self._last_signal = time.monotonic()
            self._signal_warned = False
            self._set_status(f"Listening · {device}", "ok")
        else:
            self._set_status("Stopped", "idle")

    def _toggle(self) -> None:
        if self.engine.running:
            self.engine.stop()
            self._set_running_ui(False)
            return
        self.settings.device = self.device_combo.currentData()
        try:
            device = self.engine.start()
        except Exception as exc:
            self._set_status("Couldn't open the audio input", "error")
            QMessageBox.warning(
                self,
                "Couldn't open the audio input",
                "Try another input device, close apps that hold it exclusively, or check that this app is "
                "allowed to use the microphone (macOS: System Settings → Privacy & Security → Microphone).\n\n"
                f"Details: {exc}",
            )
            return
        self._set_running_ui(True, device)

    def _tick(self) -> None:
        snap = self.engine.snapshot()
        values = {n: snap.get(n, 0.0) for n in self.source_names}
        self.meters.set_values(values)
        for name, curve in self.curves.items():
            buf = self.history[name]
            buf.append(values.get(name, 0.0))
            curve.setData(np.fromiter(buf, dtype=np.float32, count=len(buf)))

        self._frame += 1
        if self._frame % 4 == 0:
            sent = self.engine.osc.snapshot()
            self._update_live_column(sent)
            self._update_knob_column()
            if self._frame % 12 == 0:
                self._update_monitor(sent)

        if self._learn_button is not None:
            self._poll_learn()

        if self.engine.running:
            self._check_health()

    def _check_health(self) -> None:
        if not self.engine.healthy:
            self.engine.stop()
            self._set_running_ui(False)
            self._set_status("Audio device disconnected", "error")
            return
        now = time.monotonic()
        if self.engine.input_level() > 1e-4:
            self._last_signal = now
            if self._signal_warned:
                self._signal_warned = False
                self._set_status(f"Listening · {self._device_name}", "ok")
        elif not self._signal_warned and now - self._last_signal > NO_SIGNAL_AFTER_S:
            self._signal_warned = True
            self._set_status("No audio signal: check Ableton's output routing", "warn")

    def _update_live_column(self, sent: dict[str, float]) -> None:
        table = self.map_table
        was_loading = self._loading
        self._loading = True  # setText below must not look like a user edit
        for row in range(table.rowCount()):
            address_item, live_item = table.item(row, 2), table.item(row, self.LIVE_COL)
            if address_item is None or live_item is None:
                continue
            value = sent.get(address_item.text().strip())
            text = "–" if value is None else f"{value:.2f}"
            if live_item.text() != text:
                live_item.setText(text)
        self._loading = was_loading

    def _update_monitor(self, sent: dict[str, float]) -> None:
        rows = sorted(sent.items())
        table = self.monitor_table
        if table.rowCount() != len(rows):
            table.setRowCount(len(rows))
        for row, (address, value) in enumerate(rows):
            for col, text in enumerate((address, f"{value:.3f}")):
                item = table.item(row, col)
                if item is None:
                    table.setItem(row, col, QTableWidgetItem(text))
                elif item.text() != text:
                    item.setText(text)

    def closeEvent(self, event: object) -> None:
        self.timer.stop()
        self.settings.device = self.device_combo.currentData()
        self.engine.stop()
        self.midi_input.close()
        save_settings(self.settings)
        QSettings("VJBridge", "VJBridge").setValue("geometry", self.saveGeometry())
        super().closeEvent(event)
