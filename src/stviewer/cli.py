from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    app_path = Path(__file__).with_name("app.py")
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(app_path),
        "--server.port",
        os.environ.get("STVIEWER_PORT", "8501"),
    ]
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
