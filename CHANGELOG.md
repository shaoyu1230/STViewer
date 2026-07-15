# Changelog

All notable changes to STViewer will be documented in this file.

## 0.1.0

First public project version of STViewer.

### Added

- Created a standalone `STViewer` repository structure
- Added Python packaging with `pyproject.toml`
- Added a CLI entry point with `stviewer`
- Added `scripts/start.sh` for local startup
- Added `scripts/install_linux.sh` for Linux launcher and desktop entry installation
- Added GitHub Actions CI for installation and test checks
- Added example input data in `examples/example_spatial.csv`
- Added screenshots under `docs/assets/`

### Core Features

- CSV-based spatial transcriptomics visualization
- Required spatial columns: `x` and `y`
- User-selectable cell ID column, default preferring `X_index`
- Automatic removal of rowname-like columns such as `Unnamed: 0`
- Real `x:y` aspect ratio plotting
- Metadata-based cell coloring
- Automatic categorical and continuous color mode detection
- Interactive category color editing
- Lasso and box selection
- Multiple saved regions within one label group
- Export of current selection and all saved regions as CSV
- Saved region preview plot
- Built-in example data loading from the sidebar

### UI and UX

- Added dataset summary metrics
- Simplified large selection display into a lighter selection summary
- Added preview table for selected cells on demand
- Added saved-region preview controls
- Updated Streamlit layout API usage to remove deprecated parameters

### Documentation

- Expanded `README.md` into a cleaner project homepage
- Split detailed usage information into `docs/tutorial.md`
- Added a short quick-start page in `docs/usage.md`
- Added GitHub preparation notes in `docs/github_prep.md`

### Validation

- Added unit tests for parsing and region-label core logic
- Verified Python syntax with `py_compile`
