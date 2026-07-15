# STViewer

[![CI](https://github.com/shaoyu1230/STViewer/actions/workflows/ci.yml/badge.svg)](https://github.com/shaoyu1230/STViewer/actions/workflows/ci.yml)

STViewer is a lightweight local viewer for spatial transcriptomics CSV data. It focuses on three things:

- displaying cells by real `x` and `y` spatial coordinates
- coloring cells by metadata columns
- interactively selecting regions and exporting region labels as CSV

It is designed for Linux and macOS and runs locally through Streamlit.

## Main Features

- Load CSV files directly without database conversion
- Load bundled example data for quick testing
- Require only `x` and `y` as mandatory spatial columns
- Let the user choose the cell ID column after upload
- Ignore rowname-like columns such as `Unnamed: 0`
- Visualize cells with true `x:y` aspect ratio
- Color cells by any metadata column
- Automatically distinguish categorical and continuous columns
- Support interactive color editing for categorical labels
- Support lasso and box selection
- Save multiple regions under one label group, such as `Tumor1`, `Tumor2`, `Tumor3`
- Export the current selection or all saved regions as CSV
- Preview saved regions on a second plot

## Tutorial

Detailed documentation is now separated into a tutorial page:

- `docs/tutorial.md`

It includes:

- input file description
- cell ID column rules
- metadata column usage
- visualization functions
- region selection workflow
- output file description
- example input and output

## Screenshots

Home screen:

![STViewer home](docs/assets/stviewer-home.png)

Loaded example data:

![STViewer example](docs/assets/stviewer-example-detail.png)

## Python Environment

Recommended environment:

- Python `3.9` to `3.12`
- `pip`

Core dependencies:

- `streamlit>=1.35`
- `pandas>=2.0`
- `plotly>=5.20`

System recommendation:

- Linux or macOS
- modern browser such as Chrome, Edge, or Safari

## Installation

### Option 1: Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Option 2: Editable Install Only

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Run STViewer

### Local Run

```bash
git clone git@github.com:shaoyu1230/STViewer.git
cd STViewer
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
stviewer
```

Then open:

- [http://localhost:8501](http://localhost:8501)

If you just want to try the interface first, click `Load example data` in the sidebar.

### Run with Project Script

```bash
bash scripts/start.sh
```

Change port if needed:

```bash
STVIEWER_PORT=8502 bash scripts/start.sh
```

### Run with CLI

```bash
stviewer
```

Or:

```bash
stviewer --port 8502 --address 127.0.0.1
```

## Linux Desktop Integration

To install a local Linux launcher and desktop entry:

```bash
bash scripts/install_linux.sh
```

This creates:

- `~/.local/bin/stviewer`
- `~/.local/share/applications/stviewer.desktop`

## Project Layout

- `src/stviewer/`: main application source code
- `scripts/`: startup and helper scripts
- `docs/`: supporting documentation
- `examples/`: demo input files
- `tests/`: lightweight unit tests

## Documentation

- Tutorial: `docs/tutorial.md`
- Usage guide: `docs/usage.md`
- Release notes draft: `docs/release_v0.1.0.md`
- GitHub prep notes: `docs/github_prep.md`
- Change log: `CHANGELOG.md`
- Contribution guide: `CONTRIBUTING.md`

## Current Scope

This repository currently focuses on:

- lightweight local visualization
- CSV-based spatial transcriptomics annotation
- manual region labeling and export

It does not yet include:

- image overlay
- persistent project database
- multi-file batch management
- packaged native desktop binaries

## Suggested Next Improvements

1. Add screenshots or a short demo GIF
2. Add image overlay support for histology or tissue masks
3. Expand automated tests beyond core parsing logic
4. Validate startup on more Linux desktop environments
