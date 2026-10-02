"""Entry point used for running from source and for PyInstaller builds."""

from vj_bridge.__main__ import main

if __name__ == "__main__":
    raise SystemExit(main())
