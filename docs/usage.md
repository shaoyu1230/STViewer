# STViewer Usage

## Input Format

Required columns:

- `x`
- `y`

Recommended columns:

- `X_index` or another cell identifier column
- metadata columns such as `CellType`, `Cluster`, `Score`

Notes:

- CSV row names such as `Unnamed: 0` are ignored automatically
- The cell ID column is user-selectable after upload
- If `X_index` exists, it is selected by default
- Any extra column can be used for coloring if it is present in the CSV

## Basic Workflow

1. Start STViewer
2. Upload a CSV file
3. Choose the cell ID column
4. Choose a metadata column for coloring
5. Adjust point size and filters if needed
6. Select a region on the plot
7. Save the region with `Label group` and `Region name`
8. Export selected regions as CSV

## Color Display

- If no color column is selected, cells are shown in gray
- Numeric columns are displayed with a continuous color scale
- Categorical columns are displayed with discrete colors
- Category colors can be adjusted interactively

## Region Annotation

- A label group can contain multiple regions, for example `Tumor1`, `Tumor2`, `Tumor3`
- Saving a region records `cellid`, `label_group`, and `region_name`
- All saved regions can be downloaded together as one CSV file

## Startup Methods

Editable install:

```bash
stviewer
```

Project script:

```bash
bash scripts/start.sh
```

Direct Streamlit run:

```bash
python3 -m streamlit run src/stviewer/app.py --server.port 8501
```

## Notes

- The app is intended for local use on Linux or macOS
- Very large CSV files may need additional optimization in future releases
