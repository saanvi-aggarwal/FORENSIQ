import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer


def detect_anomalies(df, contamination=0.10):

    numerical_data = df.select_dtypes(include="number")

    if len(df) < 10 or numerical_data.empty:
        return None, "Insufficient numerical data for analysis."

    # Remove constant columns
    numerical_data = numerical_data.loc[
        :, numerical_data.nunique(dropna=True) > 1
    ]

    if numerical_data.empty:
        return None, "No varying numerical features found."

    # Fill missing values
    imputer = SimpleImputer(strategy="median")

    cleaned_data = imputer.fit_transform(numerical_data)

    # Train Isolation Forest
    model = IsolationForest(
        contamination=contamination,
        random_state=42,
        n_estimators=150
    )

    predictions = model.fit_predict(cleaned_data)

    # Lower decision scores indicate more unusual observations
    decision_scores = model.decision_function(cleaned_data)

    results = df.copy()

    results["Anomaly Status"] = [
        "Flagged for Review" if value == -1 else "Normal Pattern"
        for value in predictions
    ]

    results["Anomaly Score"] = np.round(
        -decision_scores, 4
    )

    # Identify numerical features contributing to unusualness
    median_values = numerical_data.median()
    mad_values = (
        numerical_data.sub(median_values)
        .abs()
        .median()
        .replace(0, np.nan)
    )

    robust_deviation = (
        numerical_data.sub(median_values)
        .abs()
        .div(mad_values)
    )

    explanations = []

    for index in range(len(results)):

        if predictions[index] == -1:

            deviations = robust_deviation.iloc[index].dropna()

            if not deviations.empty:
                unusual_features = deviations.nlargest(2).index.tolist()
                explanation = (
                    "Unusual values in: "
                    + ", ".join(unusual_features)
                )
            else:
                explanation = "Unusual multivariate numerical pattern."

        else:
            explanation = "No anomaly flagged by the selected model."

        explanations.append(explanation)

    results["Review Explanation"] = explanations

    return results, None
