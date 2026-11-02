import pandas as pd
import plotly.express as px


def answer_question(df, question):

    q = question.lower().strip()
    columns = list(df.columns)

    # 1. Total records
    if any(term in q for term in [
        "total records", "how many records",
        "number of records", "total entries"
    ]):

        return (
            f"The dataset contains {len(df)} records.",
            None
        )

    # 2. Missing values
    if "missing" in q or "null" in q:

        missing = df.isnull().sum()

        missing = missing[missing > 0]

        if missing.empty:
            return "No missing values were found.", None

        fig = px.bar(
            x=missing.index,
            y=missing.values,
            labels={"x": "Column", "y": "Missing Values"},
            title="Missing Values by Column"
        )

        return missing.to_string(), fig

    # 3. Duplicate records
    if "duplicate" in q:

        count = int(df.duplicated().sum())

        return f"The dataset contains {count} duplicate records.", None

    # 4. Flagged anomalies
    if "anomal" in q or "flagged" in q:

        if "Anomaly Status" not in df.columns:
            return (
                "Run anomaly detection first to answer this question.",
                None
            )

        flagged = (
            df["Anomaly Status"] == "Flagged for Review"
        ).sum()

        return (
            f"{flagged} records are flagged for review.",
            None
        )

    # 5. Detect average / mean questions
    if "average" in q or "mean" in q:

        for column in columns:

            if column.lower() in q and pd.api.types.is_numeric_dtype(df[column]):

                value = df[column].mean()

                return (
                    f"The average {column} is {value:.2f}.",
                    None
                )

    # 6. Highest frequency by category
    if any(term in q for term in [
        "most", "highest count", "maximum count",
        "most common", "occur most", "occur most frequently"
    ]):

        for column in columns:

            if (
                column.lower() in q
                and not pd.api.types.is_numeric_dtype(df[column])
            ):

                counts = (
                    df[column]
                    .value_counts()
                    .head(15)
                )

                if counts.empty:
                    return "No category data available.", None

                fig = px.bar(
                    x=counts.index.astype(str),
                    y=counts.values,
                    title=f"Frequency by {column}",
                    labels={
                        "x": column,
                        "y": "Number of Records"
                    }
                )

                return (
                    f"Most frequent {column}: "
                    f"{counts.index[0]} ({counts.iloc[0]} records).",
                    fig
                )

    # 7. Lowest numerical values
    if any(term in q for term in [
        "lowest", "minimum", "smallest"
    ]):

        for column in columns:

            if column.lower() in q and pd.api.types.is_numeric_dtype(df[column]):

                lowest = df.nsmallest(5, column)

                return (
                    f"Five records with the lowest {column}:",
                    None,
                    lowest
                )

    return (
        "I could not interpret that question. Try asking about "
        "record counts, missing values, duplicates, averages, "
        "anomalies or the most frequent category.",
        None
    )
