def generate_insights(df, profile, anomaly_results=None):

    insights = []

    insights.append(
        f"The dataset contains {profile['total_rows']} records "
        f"and {profile['total_columns']} columns."
    )

    if profile["missing_cells"] > 0:
        insights.append(
            f"There are {profile['missing_cells']} missing cells "
            "that may require data cleaning."
        )
    else:
        insights.append(
            "No missing values were detected."
        )

    if profile["duplicate_rows"] > 0:
        insights.append(
            f"{profile['duplicate_rows']} duplicate rows were detected."
        )
    else:
        insights.append("No duplicate rows were detected.")

    for column in profile["numerical_columns"]:

        if df[column].notna().any():

            mean_value = df[column].mean()
            median_value = df[column].median()

            insights.append(
                f"{column}: Mean = {mean_value:.2f}, "
                f"Median = {median_value:.2f}."
            )

    if anomaly_results is not None:

        flagged = (
            anomaly_results["Anomaly Status"]
            == "Flagged for Review"
        ).sum()

        insights.append(
            f"{flagged} records were flagged by the "
            "anomaly detection algorithm for further review."
        )

    return insights
