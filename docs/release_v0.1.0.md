# STViewer v0.1.0 Release Notes

## Summary

STViewer `v0.1.0` is the first public version of the project.

This release provides a lightweight local tool for spatial transcriptomics CSV visualization, metadata coloring, manual region selection, and region export.

## Highlights

- CSV input with only `x` and `y` required
- User-selectable cell ID column, default preferring `X_index`
- Support for both categorical and continuous metadata coloring
- Lasso and box selection for manual region annotation
- Multiple saved regions within one label group, such as `Tumor1`, `Tumor2`, `Tumor3`
- Export of selected cells and all saved regions as CSV
- Built-in example data loading for quick testing
- Linux-friendly startup scripts and desktop launcher installation

## Included in This Release

### Application

- Streamlit-based interactive viewer
- `stviewer` command-line launcher
- `scripts/start.sh` local run script
- `scripts/install_linux.sh` Linux desktop integration helper

### Documentation

- project overview in `README.md`
- full tutorial in `docs/tutorial.md`
- quick-start page in `docs/usage.md`
- screenshots in `docs/assets/`

### Quality Checks

- GitHub Actions CI
- unit tests for core logic
- syntax validation with `py_compile`

## Recommended Use Cases

- inspect spatial transcriptomics CSV coordinates quickly
- color cells by cell type, cluster, score, or other metadata
- manually define spatial regions for downstream analysis
- export region-labeled cell IDs for later pipelines

## Known Current Scope

This version focuses on lightweight local usage and does not yet include:

- histology image overlay
- packaged native desktop binaries
- persistent project storage
- multi-file project management

## Suggested GitHub Release Title

```text
STViewer v0.1.0 - First public release
```

## Suggested GitHub Release Description

```markdown
STViewer v0.1.0 is the first public release of a lightweight local viewer for spatial transcriptomics CSV data.

Highlights:

- CSV input with `x` and `y` as required columns
- user-selectable cell ID column
- metadata coloring for categorical and continuous variables
- lasso and box selection for manual region annotation
- export of selected cells and saved regions as CSV
- built-in example data for quick testing
- Linux-friendly launcher scripts and documentation

Main docs:

- README: project overview and installation
- docs/tutorial.md: full input, workflow, and output tutorial
```
