from __future__ import annotations

import unittest

import pandas as pd

from stviewer.core import (
    build_column_mapping,
    clean_input_columns,
    default_region_name,
    infer_color_mode,
    merge_saved_regions,
    normalize_name,
    standardize_dataframe,
)


class TestCore(unittest.TestCase):
    def test_normalize_name(self):
        self.assertEqual(normalize_name(" Cell-Type "), "cell_type")

    def test_clean_input_columns_removes_unnamed(self):
        df = pd.DataFrame({"Unnamed: 0": [1], "x": [1], "y": [2], "X_index": ["c1"]})
        cleaned = clean_input_columns(df)
        self.assertNotIn("Unnamed: 0", cleaned.columns)

    def test_build_column_mapping_supports_x_index_alias(self):
        df = pd.DataFrame({"x": [1], "y": [2], "X_index": ["c1"]})
        mapping = build_column_mapping(df)
        self.assertEqual(mapping["cellid"], "X_index")

    def test_standardize_dataframe_keeps_valid_rows(self):
        df = pd.DataFrame(
            {
                "x": [1, "bad", 3],
                "y": [2, 4, 5],
                "X_index": ["c1", "c2", "c3"],
                "CellType": ["A", "B", "C"],
            }
        )
        standardized = standardize_dataframe(df)
        self.assertEqual(list(standardized["cellid"]), ["c1", "c3"])
        self.assertIn("row_id", standardized.columns)

    def test_infer_color_mode(self):
        self.assertEqual(infer_color_mode(pd.Series([1, 2, 3])), "continuous")
        self.assertEqual(infer_color_mode(pd.Series(["A", "B"])), "categorical")

    def test_merge_saved_regions_replaces_same_region_name(self):
        saved = pd.DataFrame(
            {
                "cellid": ["c1"],
                "label_group": ["Tumor"],
                "region_name": ["Tumor1"],
            }
        )
        selected = pd.DataFrame({"cellid": ["c2", "c3"]})
        merged = merge_saved_regions(saved, selected, "Tumor", "Tumor1")
        self.assertEqual(list(merged["cellid"]), ["c2", "c3"])

    def test_default_region_name_counts_existing_regions(self):
        saved = pd.DataFrame(
            {
                "cellid": ["c1", "c2"],
                "label_group": ["Tumor", "Tumor"],
                "region_name": ["Tumor1", "Tumor2"],
            }
        )
        self.assertEqual(default_region_name("Tumor", saved), "Tumor3")


if __name__ == "__main__":
    unittest.main()
