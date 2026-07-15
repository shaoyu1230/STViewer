# STViewer

[![CI](https://github.com/shaoyu1230/STViewer/actions/workflows/ci.yml/badge.svg)](https://github.com/shaoyu1230/STViewer/actions/workflows/ci.yml)

STViewer is a lightweight local viewer for spatial transcriptomics CSV data. It focuses on three things:

- displaying cells by real `x` and `y` spatial coordinates
- coloring cells by metadata columns
- interactively selecting regions and exporting region labels as CSV

It is designed for Linux and macOS and runs locally through Streamlit.

## Main Features

- Load CSV files directly without database conversion
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

## Input File

STViewer currently accepts:

- `.csv`

### Required Columns

- `x`: cell or spot x coordinate
- `y`: cell or spot y coordinate

### Cell ID Column

The cell ID column is not fixed anymore.

- After loading the CSV, STViewer asks the user to choose one column as `cellid`
- If `X_index` exists, it is selected by default
- Other common choices can also be used, such as `cellid`, `CellID`, `barcode`, or any custom column

### Optional Columns

Any additional column can be used as metadata, for example:

- `CellType`
- `Cluster`
- `MajorType`
- `sample`
- `Score`
- `abundance`
- custom clinical or annotation columns

### Input Rules

- CSV row names will be ignored automatically if they appear as `Unnamed: 0`
- `x` and `y` are converted to numeric values
- rows with invalid `x` or `y` are dropped automatically
- metadata column names do not need to be fixed
- both categorical and continuous variables are supported

### Example Input

```csv
x,y,X_index,CellType,Cluster,Score
102.5,88.1,cell_001,T_cell,C1,0.82
110.2,92.4,cell_002,T_cell,C1,0.76
95.8,101.9,cell_003,B_cell,C2,0.31
120.7,115.2,cell_004,Fibroblast,C3,0.55
```

You can also test the built-in example file:

```text
examples/example_spatial.csv
```

## Visualization Functions

### Main Spatial View

The main plot shows all visible cells using the real coordinate proportion of `x` and `y`.

You can:

- zoom and pan
- lasso select cells
- box select cells
- hover to inspect `cellid`, coordinates, and current color value
- adjust point size
- invert the y-axis if needed

### Color Modes

If no color column is selected:

- cells are displayed in gray

If the selected column is categorical:

- cells are shown with discrete colors
- each category can be recolored interactively
- hex color values such as `#E64B35` are supported

If the selected column is continuous:

- cells are shown with a continuous color scale

### Filtering

You can filter visible cells by one categorical metadata column at a time.

This is useful when you want to:

- display only one sample
- focus on one major lineage
- simplify dense datasets before selecting regions

## Region Annotation Workflow

### Select Cells

Use lasso or box selection on the main plot.

The app records:

- how many cells are currently selected
- top categories among selected cells for the current color column

### Save Region

To save the selection:

1. Enter a `Label group`, such as `Tumor`
2. Enter a `Region name`, such as `Tumor1`
3. Click `Save selected cells`

One label group can contain multiple regions, for example:

- `Tumor1`
- `Tumor2`
- `Tumor3`

### Saved Region Preview

Saved regions are displayed in a second plot and can be recolored by:

- `region_label`
- `label_group`
- `region_name`

This is helpful for checking whether multiple manually selected regions look correct after saving.

## Output Files

STViewer supports two CSV exports.

### 1. Current Selection Export

File name:

- `selected_cells.csv`

Columns:

- `cellid`
- `label_group`
- `region_name`

This export contains only the cells in the current selection.

### 2. All Saved Regions Export

File name:

- `annotated_regions.csv`

Columns:

- `cellid`
- `label_group`
- `region_name`

This export contains all saved regions in the current session.

### Output Example

```csv
cellid,label_group,region_name
cell_001,Tumor,Tumor1
cell_002,Tumor,Tumor1
cell_010,Tumor,Tumor2
```

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

- Usage guide: `docs/usage.md`
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
