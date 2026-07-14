from __future__ import annotations

import hashlib
from io import BytesIO

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="STViewer",
    page_icon="ST",
    layout="wide",
)


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


@st.cache_data(show_spinner=False)
def load_csv(file_bytes: bytes) -> pd.DataFrame:
    return pd.read_csv(BytesIO(file_bytes), index_col=False)


def init_session() -> None:
    st.session_state.setdefault("file_signature", None)
    st.session_state.setdefault(
        "saved_regions",
        pd.DataFrame(columns=["cellid", "label_group", "region_name"]),
    )
    st.session_state.setdefault("category_colors", {})


def reset_state_for_new_file(file_signature: str) -> None:
    if st.session_state["file_signature"] != file_signature:
        st.session_state["file_signature"] = file_signature
        st.session_state["saved_regions"] = pd.DataFrame(columns=["cellid", "label_group", "region_name"])
        st.session_state["category_colors"] = {}


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


def metadata_columns(df: pd.DataFrame) -> list[str]:
    return [col for col in df.columns if col not in {"x", "y", "cellid", "row_id"}]


def is_continuous_series(series: pd.Series) -> bool:
    numeric = pd.to_numeric(series, errors="coerce")
    return numeric.notna().any() and numeric.notna().sum() == series.notna().sum()


def build_hover_data(df: pd.DataFrame) -> dict[str, object]:
    hover_data: dict[str, object] = {"x": ":.2f", "y": ":.2f", "cellid": True}
    for col in metadata_columns(df):
        hover_data[col] = True
    return hover_data


def infer_color_mode(series: pd.Series) -> str:
    return "continuous" if is_continuous_series(series) else "categorical"


def build_hover_template(color_by: str | None) -> str:
    lines = [
        "cellid=%{customdata[1]}",
        "x=%{x:.2f}",
        "y=%{y:.2f}",
    ]
    if color_by:
        lines.append(f"{color_by}=%{{customdata[2]}}")
    return "<br>".join(lines) + "<extra></extra>"


def default_region_name(label_group: str, saved_regions: pd.DataFrame) -> str:
    label_group = label_group.strip()
    if not label_group:
        return ""
    group_rows = saved_regions[saved_regions["label_group"] == label_group]
    return f"{label_group}{len(group_rows['region_name'].unique()) + 1}"


def default_palette() -> list[str]:
    return [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf",
        "#264653",
        "#e76f51",
        "#2a9d8f",
        "#f4a261",
        "#457b9d",
    ]


def get_category_color_map(file_signature: str, color_by: str, categories: list[str]) -> dict[str, str]:
    color_store = st.session_state["category_colors"]
    store_key = f"{file_signature}:{color_by}"
    existing = color_store.get(store_key, {})
    palette = default_palette()
    updated = {}

    for idx, category in enumerate(categories):
        updated[category] = existing.get(category, palette[idx % len(palette)])

    color_store[store_key] = updated
    st.session_state["category_colors"] = color_store
    return updated


def render_category_color_editor(file_signature: str, color_by: str, categories: list[str]) -> dict[str, str]:
    color_map = get_category_color_map(file_signature, color_by, categories)
    updated_map = dict(color_map)
    with st.sidebar.expander(f"{color_by} colors", expanded=False):
        st.caption("Pick a color or type a hex code like `#E64B35`.")
        for category in categories:
            picker_key = f"picker:{file_signature}:{color_by}:{category}"
            text_key = f"text:{file_signature}:{color_by}:{category}"

            if picker_key not in st.session_state:
                st.session_state[picker_key] = color_map[category]
            if text_key not in st.session_state:
                st.session_state[text_key] = color_map[category]

            col1, col2 = st.columns([1, 1.4])
            with col1:
                picked = st.color_picker(
                    label=str(category),
                    value=st.session_state[picker_key],
                    key=picker_key,
                    label_visibility="collapsed",
                )
            with col2:
                typed = st.text_input(
                    label=f"{category} hex",
                    value=st.session_state[text_key],
                    key=text_key,
                    label_visibility="collapsed",
                ).strip()

            chosen = typed if typed.startswith("#") and len(typed) in {4, 7} else picked
            updated_map[category] = chosen

    color_store = st.session_state["category_colors"]
    color_store[f"{file_signature}:{color_by}"] = updated_map
    st.session_state["category_colors"] = color_store
    return updated_map


def build_saved_region_view(df: pd.DataFrame, saved_regions: pd.DataFrame) -> pd.DataFrame:
    if saved_regions.empty:
        return df.iloc[0:0].copy()
    merged = df.merge(saved_regions, on="cellid", how="inner")
    merged["region_label"] = merged["label_group"] + " / " + merged["region_name"]
    return merged


def render_plot(
    df: pd.DataFrame,
    color_by: str | None,
    invert_y: bool,
    point_size: int,
    category_color_map: dict[str, str] | None = None,
):
    fig = go.Figure()
    hover_template = build_hover_template(color_by)

    if color_by is None:
        customdata = df[["row_id", "cellid"]].to_numpy()
        fig.add_trace(
            go.Scattergl(
                x=df["x"],
                y=df["y"],
                mode="markers",
                name="Cells",
                customdata=customdata,
                hovertemplate=hover_template,
                marker={"size": point_size, "color": "#9aa3ab", "opacity": 0.8},
            )
        )
    elif infer_color_mode(df[color_by]) == "continuous":
        values = pd.to_numeric(df[color_by], errors="coerce")
        label_values = df[color_by].astype(str).fillna("NA")
        customdata = pd.DataFrame(
            {"row_id": df["row_id"], "cellid": df["cellid"], "label": label_values}
        ).to_numpy()
        fig.add_trace(
            go.Scattergl(
                x=df["x"],
                y=df["y"],
                mode="markers",
                name=color_by,
                customdata=customdata,
                hovertemplate=hover_template,
                marker={
                    "size": point_size,
                    "color": values,
                    "colorscale": "Viridis",
                    "opacity": 0.8,
                    "colorbar": {"title": color_by},
                },
            )
        )
    else:
        value_series = df[color_by].fillna("NA").astype(str)
        categories = value_series.unique().tolist()
        for idx, category in enumerate(categories):
            subset = df[value_series == category]
            customdata = pd.DataFrame(
                {
                    "row_id": subset["row_id"],
                    "cellid": subset["cellid"],
                    "label": value_series[value_series == category],
                }
            ).to_numpy()
            fig.add_trace(
                go.Scattergl(
                    x=subset["x"],
                    y=subset["y"],
                    mode="markers",
                    name=str(category),
                    customdata=customdata,
                    hovertemplate=hover_template,
                    marker={
                        "size": point_size,
                        "color": (
                            category_color_map.get(str(category), default_palette()[idx % len(default_palette())])
                            if category_color_map
                            else default_palette()[idx % len(default_palette())]
                        ),
                        "opacity": 0.8,
                    },
                )
            )

    fig.update_layout(
        dragmode="lasso",
        legend_title_text=(color_by if color_by else "Color"),
        margin={"l": 20, "r": 20, "t": 20, "b": 20},
        plot_bgcolor="#faf7f0",
        paper_bgcolor="#fffdf8",
        uirevision="spatial-plot",
    )
    fig.update_xaxes(title="x", zeroline=False, constrain="domain")
    fig.update_yaxes(
        title="y",
        zeroline=False,
        autorange="reversed" if invert_y else True,
        scaleanchor="x",
        scaleratio=1,
    )
    return fig


def main() -> None:
    init_session()

    st.title("STViewer")
    st.caption("CSV visualization, lasso selection, and custom region export for spatial transcriptomics.")

    with st.sidebar:
        st.header("Input")
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
        st.markdown(
            "Required columns: `x`, `y`, `X_index`\n\n"
            "Optional columns: any metadata columns, such as `CellType`, `Cluster`, score, or abundance"
        )

    if uploaded_file is None:
        st.info("Upload a CSV file to start.")
        st.code("x,y,X_index,CellType,Cluster,Score", language="text")
        return

    file_bytes = uploaded_file.getvalue()
    file_signature = hashlib.md5(file_bytes).hexdigest()
    reset_state_for_new_file(file_signature)

    try:
        raw_df = load_csv(file_bytes)
        df = standardize_dataframe(raw_df)
    except Exception as exc:
        st.error(f"Failed to read CSV: {exc}")
        return

    if df.empty:
        st.error("No valid rows found after parsing `x` and `y`.")
        return

    meta_cols = metadata_columns(df)

    with st.sidebar:
        st.header("Display")
        color_options = ["None"] + meta_cols
        color_label = st.selectbox("Color by", color_options)
        color_by = None if color_label == "None" else color_label
        invert_y = st.checkbox("Invert y-axis", value=True)
        point_size = st.slider("Main point size", min_value=1, max_value=12, value=3)

        st.header("Filter")
        filtered_df = df.copy()
        filterable_cols = [col for col in meta_cols if not is_continuous_series(df[col])]
        selected_filter_col = st.selectbox("Filter column", ["None"] + filterable_cols)
        if selected_filter_col != "None":
            filter_choices = sorted(df[selected_filter_col].fillna("NA").astype(str).unique().tolist())
            selected_values = st.multiselect(selected_filter_col, filter_choices, default=filter_choices)
            filtered_df = filtered_df[
                filtered_df[selected_filter_col].fillna("NA").astype(str).isin(selected_values)
            ].copy()

    if filtered_df.empty:
        st.warning("No cells remain after filtering.")
        return

    category_color_map = None
    if color_by and infer_color_mode(filtered_df[color_by]) == "categorical":
        categories = filtered_df[color_by].fillna("NA").astype(str).unique().tolist()
        category_color_map = render_category_color_editor(file_signature, color_by, categories)

    overview_col, export_col = st.columns([3, 1])
    with overview_col:
        st.metric("Visible cells", f"{len(filtered_df):,}")
    with export_col:
        st.metric("Saved annotations", f"{len(st.session_state['saved_regions']):,}")

    fig = render_plot(
        filtered_df,
        color_by=color_by,
        invert_y=invert_y,
        point_size=point_size,
        category_color_map=category_color_map,
    )
    event = st.plotly_chart(
        fig,
        use_container_width=True,
        key="spatial_plot",
        on_select="rerun",
        selection_mode=("lasso", "box"),
    )

    selected_points = event.selection.get("points", []) if event else []
    selected_row_ids = [point["customdata"][0] for point in selected_points if "customdata" in point]
    selected_df = selection_to_dataframe(selected_row_ids, filtered_df)

    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.subheader("Selected Cells")
        if selected_df.empty:
            st.info("Use lasso or box select on the plot to capture cells.")
        else:
            preview_cols = ["cellid"] + metadata_columns(selected_df)
            st.dataframe(selected_df[preview_cols], use_container_width=True, height=280)

    with right_col:
        st.subheader("Save Region")
        label_group = st.text_input("Label group", placeholder="Tumor")
        suggested_region_name = default_region_name(label_group, st.session_state["saved_regions"])
        region_name = st.text_input(
            "Region name",
            value=suggested_region_name,
            placeholder="Tumor1",
        )
        if st.button("Save selected cells", use_container_width=True):
            if selected_df.empty:
                st.warning("No selected cells to save.")
            elif not label_group.strip():
                st.warning("Please enter a label group.")
            elif not region_name.strip():
                st.warning("Please enter a region name.")
            else:
                st.session_state["saved_regions"] = merge_saved_regions(
                    st.session_state["saved_regions"],
                    selected_df,
                    label_group.strip(),
                    region_name.strip(),
                )
                st.success(
                    f"Saved {len(selected_df)} cells into `{label_group.strip()} / {region_name.strip()}`."
                )

        current_export = selected_df[["cellid"]].copy() if not selected_df.empty else pd.DataFrame(columns=["cellid"])
        if not current_export.empty and label_group.strip() and region_name.strip():
            current_export["label_group"] = label_group.strip()
            current_export["region_name"] = region_name.strip()

        st.download_button(
            "Download current selection",
            data=current_export.to_csv(index=False).encode("utf-8"),
            file_name="selected_cells.csv",
            mime="text/csv",
            use_container_width=True,
            disabled=current_export.empty or not label_group.strip() or not region_name.strip(),
        )

    st.subheader("Saved Region Table")
    saved_regions = st.session_state["saved_regions"]
    if saved_regions.empty:
        st.info("Saved groups will appear here.")
    else:
        st.dataframe(saved_regions, use_container_width=True, height=260)
        st.download_button(
            "Download all saved groups",
            data=saved_regions.to_csv(index=False).encode("utf-8"),
            file_name="annotated_regions.csv",
            mime="text/csv",
        )

        st.subheader("Saved Region Preview")
        region_view_df = build_saved_region_view(df, saved_regions)
        preview_color = st.selectbox(
            "Saved region color by",
            ["region_label", "label_group", "region_name"],
            key="saved_region_color_by",
        )
        preview_point_size = st.slider(
            "Saved region point size",
            min_value=1,
            max_value=12,
            value=4,
            key="saved_region_point_size",
        )
        region_fig = render_plot(
            region_view_df,
            color_by=preview_color,
            invert_y=invert_y,
            point_size=preview_point_size,
        )
        st.plotly_chart(
            region_fig,
            use_container_width=True,
            key="saved_region_plot",
        )

    with st.expander("Dataset preview"):
        st.dataframe(raw_df.head(20), use_container_width=True)


if __name__ == "__main__":
    main()
