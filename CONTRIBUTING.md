# Contributing to STViewer

Thanks for contributing to STViewer.

## Development Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
pip install pytest
```

## Run Locally

```bash
stviewer
```

Or:

```bash
python3 -m streamlit run src/stviewer/app.py --server.port 8501
```

## Run Tests

```bash
python3 -m unittest discover -s tests
```

## Contribution Notes

- Keep the project lightweight and easy to run on Linux
- Prefer clear CSV-based workflows
- Avoid introducing heavy dependencies unless necessary
