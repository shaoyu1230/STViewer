# STViewer Usage

## Input Format

Required columns:

- `x`
- `y`

Recommended columns:

- `X_index` or another cell identifier column
- metadata columns such as `CellType`, `Cluster`, `Score`

## Basic Workflow

1. Start STViewer
2. Upload a CSV file
3. Choose the cell ID column
4. Choose a metadata column for coloring
5. Adjust point size and filters if needed
6. Select a region on the plot
7. Save the region with `Label group` and `Region name`
8. Export selected regions as CSV

## Notes

- Rowname-like columns such as `Unnamed: 0` are ignored
- Numeric metadata columns are shown with continuous color scales
- Categorical metadata columns are shown with discrete colors
