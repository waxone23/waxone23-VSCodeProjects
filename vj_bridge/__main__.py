from __future__ import annotations

import sys

from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from .config import load_settings
from .resources import asset_path
from .theme import apply_theme
from .ui import MainWindow


def main() -> int:
    if sys.platform == "win32":
        # Own taskbar identity so Windows shows our icon instead of python.exe's.
        try:
            import ctypes

            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("com.vjbridge.app")
        except Exception:
            pass

    app = QApplication(sys.argv)
    app.setApplicationName("VJ Bridge")
    app.setOrganizationName("VJBridge")
    app.setWindowIcon(QIcon(asset_path("icon.png")))
    apply_theme(app)

    window = MainWindow(load_settings())
    window.show()
    QTimer.singleShot(400, window.maybe_show_first_run)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
