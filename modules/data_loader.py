import pandas as pd
import json


def load_dataset(uploaded_file):
    """Load supported datasets into a Pandas DataFrame."""

    filename = uploaded_file.name.lower()

    if filename.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    elif filename.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)

    elif filename.endswith(".json"):
        data = json.load(uploaded_file)
        df = pd.json_normalize(data)

    else:
        raise ValueError("Unsupported file format.")

    if df.empty:
        raise ValueError("The uploaded dataset is empty.")

    if len(df.columns) == 0:
        raise ValueError("No columns found in the dataset.")

    return df
