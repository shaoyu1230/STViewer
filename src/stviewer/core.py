from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = {
    "x": {"x"},
    "y": {"y"},
    "cellid": {"x_index", "cellid", "cell_id", "cell", "barcode"},
}


def normalize_name(name: str) -> str:
    return name.strip().lower().replace(" ", "").replace("-", "_")


def clean_input_columns(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.loc[:, ~df.columns.astype(str).str.match(r"^Unnamed", case=False)].copy()
    empty_named = [col for col in cleaned.columns if not str(col).strip()]
    if empty_named:
        cleaned = cleaned.drop(columns=empty_named)
    return cleaned


def build_column_mapping(df: pd.DataFrame) -> dict[str, str]:
    normalized = {normalize_name(col): col for col in df.columns}
    mapping: dict[str, str] = {}

    for target, aliases in REQUIRED_COLUMNS.items():
        matched = next((normalized[alias] for alias in aliases if alias in normalized), None)
        if matched is None:
            raise ValueError(f"Missing required column for `{target}`")
        mapping[target] = matched

    return mapping


def standardize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = clean_input_columns(df)
    mapping = build_column_mapping(df)
    renamed = df.rename(
        columns={
            mapping["x"]: "x",
            mapping["y"]: "y",
            mapping["cellid"]: "cellid",
        }
    ).copy()

    renamed["x"] = pd.to_numeric(renamed["x"], errors="coerce")
    renamed["y"] = pd.to_numeric(renamed["y"], errors="coerce")
    renamed["cellid"] = renamed["cellid"].astype(str)

    renamed = renamed.dropna(subset=["x", "y"]).reset_index(drop=True)
    renamed["row_id"] = renamed.index.astype(int)
    return renamed


def metadata_columns(df: pd.DataFrame) -> list[str]:
    return [col for col in df.columns if col not in {"x", "y", "cellid", "row_id"}]


def is_continuous_series(series: pd.Series) -> bool:
    numeric = pd.to_numeric(series, errors="coerce")
    return numeric.notna().any() and numeric.notna().sum() == series.notna().sum()


def selection_to_dataframe(selected_row_ids: list[int], df: pd.DataFrame) -> pd.DataFrame:
    if not selected_row_ids:
        preview_columns = [col for col in ["cellid"] + metadata_columns(df) if col in df.columns]
        return df.iloc[0:0][preview_columns]
    return df[df["row_id"].isin(selected_row_ids)].copy()


def merge_saved_regions(saved: pd.DataFrame, selected: pd.DataFrame, label_group: str, region_name: str) -> pd.DataFrame:
    new_rows = selected[["cellid"]].copy()
    new_rows["label_group"] = label_group
    new_rows["region_name"] = region_name

    without_same_group = saved[saved["region_name"] != region_name]
    merged = pd.concat([without_same_group, new_rows], ignore_index=True)
    return merged.drop_duplicates(subset=["cellid", "label_group", "region_name"]).sort_values(
        by=["label_group", "region_name", "cellid"]
    ).reset_index(drop=True)


def default_region_name(label_group: str, saved_regions: pd.DataFrame) -> str:
    label_group = label_group.strip()
    if not label_group:
        return ""
    group_rows = saved_regions[saved_regions["label_group"] == label_group]
    return f"{label_group}{len(group_rows['region_name'].unique()) + 1}"


def infer_color_mode(series: pd.Series) -> str:
    return "continuous" if is_continuous_series(series) else "categorical"
