# STViewer

STViewer is a lightweight spatial transcriptomics viewer built with Streamlit.

## Python Environment

Recommended environment:

- Python `3.9` to `3.12`
- `pip` for dependency installation

Core Python dependencies:

- `streamlit>=1.35`
- `pandas>=2.0`
- `plotly>=5.20`

## Project Layout

The project is organized as:

- `src/stviewer/`: application source code
- `scripts/`: launcher or helper scripts
- `docs/`: user and developer documentation
- `examples/`: demo input files

## Features

- Load CSV with spatial coordinates
- Let the user choose the cell ID column
- Visualize cells by metadata columns
- Choose color columns dynamically
- Support region selection and region export
- Support both categorical and continuous metadata coloring

## Installation

### Option 1: Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Option 2: Install as an editable package

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Local Run

```bash
git clone git@github.com:shaoyu1230/STViewer.git
cd STViewer
pip install -r requirements.txt
python3 -m streamlit run src/stviewer/app.py --server.port 8501
```

Then open:

- [http://localhost:8501](http://localhost:8501)

## Linux-Friendly Script

After installing dependencies, you can also use:

```bash
bash scripts/start.sh
```

## Command-Line Run

After editable install:

```bash
stviewer
```

## Example Data

Try:

```text
examples/example_spatial.csv
```

## Documentation

- Usage guide: `docs/usage.md`
- GitHub prep notes: `docs/github_prep.md`
- Change log: `CHANGELOG.md`

## Notes

- This repository currently targets lightweight local usage.
- Input data is expected to be CSV-based.
- Rowname-like columns such as `Unnamed: 0` are ignored during import.

## Suggested Next Improvements

1. Add screenshots or a short demo GIF
2. Verify startup on Linux desktop environments
3. Add automated tests and GitHub Actions
4. Expand documentation for region-selection workflow
