"""Dark theme: palette + stylesheet."""

from __future__ import annotations

from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication

ACCENT = "#5b8cff"
GREEN = "#2fbf71"
RED = "#e5484d"
AMBER = "#f0b429"
BG = "#17171b"
PANEL = "#1f1f25"
RAISED = "#2a2a32"
BORDER = "#34343e"
TEXT = "#e6e6ea"
MUTED = "#8b8b96"

STYLESHEET = f"""
QWidget {{ font-size: 13px; color: {TEXT}; }}
QMainWindow, QDialog {{ background: {BG}; }}
QLabel#muted {{ color: {MUTED}; }}

QGroupBox {{
    background: {PANEL}; border: 1px solid {BORDER}; border-radius: 10px;
    margin-top: 14px; padding: 14px 10px 10px 10px; font-weight: 600;
}}
QGroupBox::title {{ subcontrol-origin: margin; left: 14px; padding: 0 6px; color: {MUTED}; }}

QPushButton {{
    background: {RAISED}; border: 1px solid {BORDER}; border-radius: 8px; padding: 7px 14px;
}}
QPushButton:hover {{ background: #34343f; }}
QPushButton:pressed {{ background: #24242b; }}
QPushButton:disabled {{ color: #666670; }}
QPushButton#startButton {{
    background: {GREEN}; border: none; color: #07130c; font-weight: 700; padding: 9px 28px;
}}
QPushButton#startButton:hover {{ background: #3fd083; }}
QPushButton#startButton[running="true"] {{ background: {RED}; color: white; }}
QPushButton#startButton[running="true"]:hover {{ background: #f0595e; }}

QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
    background: {BG}; border: 1px solid {BORDER}; border-radius: 6px; padding: 5px 8px;
    selection-background-color: {ACCENT};
}}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {{ border: 1px solid {ACCENT}; }}
QComboBox:disabled {{ color: #666670; }}
QComboBox QAbstractItemView {{
    background: {PANEL}; border: 1px solid {BORDER}; selection-background-color: {ACCENT};
}}

QTableWidget {{
    background: {BG}; alternate-background-color: #1b1b20; border: 1px solid {BORDER};
    border-radius: 8px; gridline-color: transparent; selection-background-color: #2b3a66;
}}
QTableWidget::item {{ padding: 4px 8px; }}
QHeaderView::section {{
    background: {PANEL}; color: {MUTED}; border: none; border-bottom: 1px solid {BORDER};
    padding: 7px 8px; font-weight: 600;
}}

QTabWidget::pane {{ border: none; top: 4px; }}
QTabBar::tab {{ background: transparent; color: {MUTED}; padding: 8px 18px; border-bottom: 2px solid transparent; }}
QTabBar::tab:selected {{ color: {TEXT}; border-bottom: 2px solid {ACCENT}; }}
QTabBar::tab:hover {{ color: {TEXT}; }}

QSplitter::handle {{ background: transparent; }}
QMenuBar {{ background: {BG}; }}
QMenuBar::item:selected {{ background: {RAISED}; border-radius: 4px; }}
QMenu {{ background: {PANEL}; border: 1px solid {BORDER}; padding: 4px; }}
QMenu::item {{ padding: 6px 22px; border-radius: 4px; }}
QMenu::item:selected {{ background: {ACCENT}; }}
QToolTip {{ background: {RAISED}; color: {TEXT}; border: 1px solid {BORDER}; padding: 5px 7px; }}

QScrollBar:vertical {{ background: transparent; width: 10px; margin: 2px; }}
QScrollBar::handle:vertical {{ background: {BORDER}; border-radius: 4px; min-height: 24px; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
"""


def apply_theme(app: QApplication) -> None:
    app.setStyle("Fusion")
    palette = QPalette()
    roles = {
        QPalette.ColorRole.Window: BG,
        QPalette.ColorRole.WindowText: TEXT,
        QPalette.ColorRole.Base: BG,
        QPalette.ColorRole.AlternateBase: "#1b1b20",
        QPalette.ColorRole.Text: TEXT,
        QPalette.ColorRole.Button: RAISED,
        QPalette.ColorRole.ButtonText: TEXT,
        QPalette.ColorRole.Highlight: ACCENT,
        QPalette.ColorRole.HighlightedText: "#ffffff",
        QPalette.ColorRole.ToolTipBase: RAISED,
        QPalette.ColorRole.ToolTipText: TEXT,
        QPalette.ColorRole.PlaceholderText: MUTED,
    }
    for role, color in roles.items():
        palette.setColor(role, QColor(color))
    app.setPalette(palette)
    app.setStyleSheet(STYLESHEET)
