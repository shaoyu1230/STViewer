# GitHub Preparation Notes

## What You Can Do First

### 1. Decide repository identity

- Repository name: `STViewer`
- One-line description:
  `A lightweight viewer for spatial transcriptomics CSV data`

### 2. Prepare open-source basics

- Choose a license
- Decide whether sample data can be shared publicly
- Decide whether screenshots can be shown publicly

### 3. Prepare a first public release scope

Keep the first version small:

- CSV import
- Cell ID column selection
- Metadata coloring
- Region selection
- Region export

### 4. Prepare documentation

At minimum:

- installation
- input format
- startup command
- example workflow
- known limitations
- cell ID column selection rules
- screenshot or short demo GIF

### 5. Prepare repository hygiene

- remove temporary files
- add `.gitignore`
- add `README.md`
- add `LICENSE`
- add version number

## Recommended Release Order

1. Make project structure stable
2. Verify startup on Linux
3. Add example data
4. Add screenshots
5. Initialize git repo or create new GitHub repo
6. Push first public commit

## Suggested Public Release Checklist

- confirm `README.md` matches the real startup command
- confirm `requirements.txt` and `pyproject.toml` are consistent
- verify `stviewer` launches in a clean virtual environment
- verify Linux launcher script works on another machine
- add a repository topic list such as `streamlit`, `spatial-transcriptomics`, `bioinformatics`
