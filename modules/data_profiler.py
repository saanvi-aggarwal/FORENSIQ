import pandas as pd


def generate_profile(df):

    profile = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_cells": int(df.isnull().sum().sum()),

        "numerical_columns": list(
            df.select_dtypes(include="number").columns
        ),

        "categorical_columns": list(
            df.select_dtypes(
                include=["object", "category"]
            ).columns
        ),

        "missing_by_column": df.isnull().sum(),

        "data_types": df.dtypes.astype(str),

        "summary": df.describe(include="all").T
    }

    return profile


def get_column_quality(df):

    quality = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Missing Values": df.isnull().sum().values,

        "Missing Percentage": (
            df.isnull().mean().values * 100
        ).round(2),

        "Unique Values": df.nunique().values
    })

    return quality
