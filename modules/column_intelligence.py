import pandas as pd


def identify_column_type(series, column_name):

    name = column_name.lower().replace(" ", "_")

    # Identifier detection
    identifier_keywords = [
        "id", "identifier", "case_number",
        "reference_number", "record_number"
    ]

    if (
        name in identifier_keywords
        or name.endswith("_id")
    ):
        return "Identifier"

    # Location detection
    location_keywords = [
        "location", "address", "city",
        "place", "region", "latitude",
        "longitude", "coordinates"
    ]

    if any(word in name for word in location_keywords):
        return "Location"

    # Date and time detection
    time_keywords = [
        "date", "time", "timestamp",
        "day", "year", "month"
    ]

    if any(word in name for word in time_keywords):
        return "Time / Date"

    # Category detection
    category_keywords = [
        "type", "category", "status",
        "gender", "classification"
    ]

    if any(word in name for word in category_keywords):
        return "Categorical"

    if pd.api.types.is_datetime64_any_dtype(series):
        return "Time / Date"

    if pd.api.types.is_numeric_dtype(series):
        return "Numerical Measurement"

    if series.nunique(dropna=True) < 30:
        return "Categorical"

    return "Text"


def analyse_columns(df):

    results = []

    for column in df.columns:

        detected_type = identify_column_type(
            df[column],
            column
        )

        results.append({
            "Column Name": column,
            "Detected Type": detected_type,
            "Unique Values": df[column].nunique(),
            "Missing Values": df[column].isnull().sum()
        })

    return pd.DataFrame(results)
