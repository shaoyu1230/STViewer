#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
BIN_DIR="${HOME}/.local/bin"
APP_DIR="${HOME}/.local/share/applications"
LAUNCHER_PATH="${BIN_DIR}/stviewer"
DESKTOP_PATH="${APP_DIR}/stviewer.desktop"

mkdir -p "${BIN_DIR}" "${APP_DIR}"

cat > "${LAUNCHER_PATH}" <<EOF
#!/usr/bin/env bash
set -e
PROJECT_DIR="${PROJECT_DIR}"
if [[ -x "\${PROJECT_DIR}/.venv/bin/python" ]]; then
  PYTHON_BIN="\${PROJECT_DIR}/.venv/bin/python"
else
  PYTHON_BIN="\${PYTHON_BIN:-python3}"
fi
exec "\${PYTHON_BIN}" -m stviewer --port "\${STVIEWER_PORT:-8501}" --address "\${STVIEWER_ADDRESS:-127.0.0.1}"
EOF

chmod +x "${LAUNCHER_PATH}"

cat > "${DESKTOP_PATH}" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=STViewer
Comment=Spatial transcriptomics CSV viewer
Exec=${LAUNCHER_PATH}
Terminal=false
Categories=Science;DataVisualization;
StartupNotify=true
EOF

echo "Installed launcher: ${LAUNCHER_PATH}"
echo "Installed desktop entry: ${DESKTOP_PATH}"
echo "If ${BIN_DIR} is not on PATH, add this line to your shell profile:"
echo "export PATH=\"${BIN_DIR}:\$PATH\""
