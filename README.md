# STViewer

STViewer is a lightweight spatial transcriptomics viewer built with Streamlit.

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

## Local Run

```bash
cd /Users/angela/Documents/00_annoroad/06_Development/STHub/STViewer
pip install -r requirements.txt
python3 -m streamlit run src/stviewer/app.py --server.port 8501
```

Then open:

- [http://localhost:8501](http://localhost:8501)

## Linux-Friendly Script

You can also use:

```bash
bash scripts/start.sh
```

## Future Package Run

After packaging or editable install:

```bash
pip install -e .
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

## Suggested GitHub Release Checklist

1. Replace placeholder GitHub URLs in `pyproject.toml`
2. Add real screenshots to the repository
3. Verify startup on a Linux machine
4. Decide the first public version scope
5. Initialize a dedicated git repository and push to GitHub
