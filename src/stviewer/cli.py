from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="stviewer",
        description="Launch the STViewer Streamlit application.",
    )
    parser.add_argument(
        "--port",
        default=os.environ.get("STVIEWER_PORT", "8501"),
        help="Port for the local Streamlit server. Default: 8501",
    )
    parser.add_argument(
        "--address",
        default=os.environ.get("STVIEWER_ADDRESS", "127.0.0.1"),
        help="Bind address for the local Streamlit server. Default: 127.0.0.1",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    app_path = Path(__file__).with_name("app.py")
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(app_path),
        "--server.address",
        args.address,
        "--server.port",
        str(args.port),
    ]
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
