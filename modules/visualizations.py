import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from modules.ui_components import apply_forensic_theme


def calculate_column_statistics(df, column):
    """
    Safely calculate consistent parametric, non-parametric,
    and IQR-based outlier statistics for a given numerical column.
    """
    if column not in df.columns:
        return None

    series = pd.to_numeric(df[column], errors="coerce").dropna()
    total_valid = len(series)

    if total_valid == 0:
        return None

    mean_val = float(series.mean())
    std_val = float(series.std(ddof=1)) if total_valid > 1 else 0.0
    median_val = float(series.median())
    min_val = float(series.min())
    max_val = float(series.max())

    # Quartiles and standard 1.5 x IQR rule
    q1_val = float(series.quantile(0.25))
    q3_val = float(series.quantile(0.75))
    iqr_val = q3_val - q1_val
    lower_bound = q1_val - 1.5 * iqr_val
    upper_bound = q3_val + 1.5 * iqr_val

    outliers = series[(series < lower_bound) | (series > upper_bound)]
    outlier_count = len(outliers)

    skewness = float(series.skew()) if total_valid > 2 else 0.0

    return {
        "series": series,
        "count": total_valid,
        "mean": mean_val,
        "std": std_val,
        "median": median_val,
        "min": min_val,
        "max": max_val,
        "q1": q1_val,
        "q3": q3_val,
        "iqr": iqr_val,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound,
        "outlier_count": outlier_count,
        "outliers": outliers.tolist(),
        "skewness": skewness
    }


def create_histogram(df, column):
    """
    Enhanced distribution histogram:
    - Vertical reference lines for Mean and Median with distinct colours & legend items.
    - Counts displayed above bars or on hover.
    - Dynamic Freedman-Diaconis / Sturges binning.
    - Comprehensive hover tooltips showing ranges and counts.
    - Clear axis titles and labels.
    """
    stats = calculate_column_statistics(df, column)
    if stats is None:
        fig = go.Figure()
        fig.add_annotation(text="Insufficient numerical observations", showarrow=False)
        return apply_forensic_theme(fig)

    series = stats["series"]
    n = stats["count"]

    # Dynamic bin sizing (Freedman-Diaconis rule if IQR > 0, otherwise Sturges)
    if stats["iqr"] > 0 and n > 1:
        bin_width = 2.0 * stats["iqr"] * (n ** (-1/3))
        nbins = int(np.clip(np.ceil((stats["max"] - stats["min"]) / bin_width), 5, 40)) if bin_width > 0 else 10
    else:
        nbins = int(np.clip(np.ceil(np.log2(n) + 1), 5, 25))

    fig = go.Figure()

    # Histogram trace
    fig.add_trace(go.Histogram(
        x=series,
        nbinsx=nbins,
        name="Observations",
        marker=dict(
            color="#0F766E",
            line=dict(color="#FFFFFF", width=1)
        ),
        hovertemplate=(
            "<b>Interval:</b> %{x}<br>"
            "<b>Count:</b> %{y} records<br>"
            "<extra></extra>"
        ),
        opacity=0.9
    ))

    # Reference line for Mean (Electric Blue)
    fig.add_vline(
        x=stats["mean"],
        line_width=2.5,
        line_dash="dash",
        line_color="#2563EB"
    )

    # Reference line for Median (Amber/Orange)
    fig.add_vline(
        x=stats["median"],
        line_width=2.5,
        line_dash="dot",
        line_color="#D97706"
    )

    # Traces to provide clean legend items without colliding text
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode="lines",
        line=dict(color="#2563EB", width=2.5, dash="dash"),
        name=f"Mean: {stats['mean']:.2f}"
    ))
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode="lines",
        line=dict(color="#D97706", width=2.5, dash="dot"),
        name=f"Median: {stats['median']:.2f}"
    ))

    fig.update_layout(
        title=dict(
            text=f"Distribution Analysis: {column}",
            x=0.02,
            y=0.98,
            xanchor="left",
            yanchor="top"
        ),
        xaxis_title=f"{column} (Values)",
        yaxis_title="Record Frequency (Count)",
        bargap=0.08,
        margin=dict(l=50, r=30, t=80, b=45),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=0.90,
            xanchor="left",
            x=0.02,
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="#E2E8F0",
            borderwidth=1,
            font=dict(size=11, color="#172033")
        )
    )

    return apply_forensic_theme(fig)


def create_boxplot(df, column):
    """
    Enhanced Box Plot / Outlier Analysis:
    - Standard 1.5 x IQR rule for statistical outlier detection.
    - Identified individual outlier points displayed.
    - Hover info detailing Min, Q1, Median, Q3, Max, and IQR.
    - Whisker limits properly differentiated from absolute Min/Max.
    """
    stats = calculate_column_statistics(df, column)
    if stats is None:
        fig = go.Figure()
        fig.add_annotation(text="Insufficient numerical observations", showarrow=False)
        return apply_forensic_theme(fig)

    series = stats["series"]

    fig = go.Figure()

    fig.add_trace(go.Box(
        y=series,
        name=column,
        boxpoints="outliers",  # Standard 1.5 x IQR rule
        jitter=0.2,
        pointpos=-1.6,
        marker=dict(
            color="#E11D48",  # Outlier markers
            size=6,
            outliercolor="#E11D48",
            line=dict(color="#9F1239", width=1)
        ),
        line=dict(color="#0F766E", width=2),
        fillcolor="rgba(15, 118, 110, 0.12)",
        hoverinfo="y",
        hovertemplate=(
            f"<b>{column}</b><br>"
            "<b>Value:</b> %{y:.2f}<br>"
            f"<b>IQR:</b> {stats['iqr']:.2f}<br>"
            f"<b>Lower Fence (Q1 - 1.5×IQR):</b> {stats['lower_bound']:.2f}<br>"
            f"<b>Upper Fence (Q3 + 1.5×IQR):</b> {stats['upper_bound']:.2f}<br>"
            "<extra></extra>"
        )
    ))

    # Add descriptive annotations explaining Key Quartiles & IQR
    outlier_status_text = (
        f"IQR: {stats['iqr']:.2f} | Outliers: {stats['outlier_count']}"
        if stats["outlier_count"] > 0
        else f"IQR: {stats['iqr']:.2f} | Outliers: 0 (No outliers outside 1.5×IQR)"
    )

    fig.update_layout(
        title=dict(
            text=f"Box Plot & Outlier Analysis: {column}",
            x=0.02,
            y=0.98,
            xanchor="left",
            yanchor="top"
        ),
        yaxis_title=f"{column} (Measurement Values)",
        xaxis=dict(showticklabels=False),
        margin=dict(l=50, r=30, t=80, b=45),
        annotations=[
            dict(
                text=outlier_status_text,
                xref="paper", yref="paper",
                x=0.02, y=0.03,
                showarrow=False,
                bgcolor="rgba(248, 250, 252, 0.9)",
                bordercolor="#E2E8F0",
                borderwidth=1,
                font=dict(size=11, color="#172033", family="Inter, sans-serif")
            )
        ]
    )

    return apply_forensic_theme(fig)


def generate_statistical_interpretation(stats, column_name):
    """
    Generate automatic, dynamic forensic observations derived
    directly from verified mathematical calculations.
    """
    if stats is None or stats["count"] == 0:
        return [("Data Availability", "Insufficient numerical records available to compute statistical observations.")]

    observations = []

    # 1. Central Tendency & Skewness
    mean_val = stats["mean"]
    median_val = stats["median"]
    std_val = stats["std"]
    skew = stats["skewness"]

    diff_ratio = abs(mean_val - median_val) / (std_val if std_val > 0 else 1.0)

    if diff_ratio < 0.15:
        skew_desc = f"The distribution is approximately symmetric. The mean ({mean_val:.2f}) and median ({median_val:.2f}) align closely."
    elif mean_val > median_val:
        skew_desc = f"The distribution exhibits a rightward (positive) skew (skewness = {skew:.2f}). The mean ({mean_val:.2f}) is pulled above the median ({median_val:.2f}) by higher-value records."
    else:
        skew_desc = f"The distribution exhibits a leftward (negative) skew (skewness = {skew:.2f}). The mean ({mean_val:.2f}) is below the median ({median_val:.2f}) due to low-value records."

    observations.append(("Central Tendency & Symmetry", skew_desc))

    # 2. Dispersion & Spread
    cv = (std_val / abs(mean_val) * 100) if mean_val != 0 else 0
    if cv < 20:
        spread_desc = f"Values show low variability (Std Dev = {std_val:.2f}, CV = {cv:.1f}%), indicating high consistency across evidence records."
    elif cv < 50:
        spread_desc = f"Values demonstrate moderate dispersion (Std Dev = {std_val:.2f}, CV = {cv:.1f}%), spanning from {stats['min']:.2f} to {stats['max']:.2f}."
    else:
        spread_desc = f"Values demonstrate substantial dispersion (Std Dev = {std_val:.2f}, CV = {cv:.1f}%), indicating high variability across the measured cases."

    observations.append(("Data Spread & Dispersion", spread_desc))

    # 3. Middle 50% Concentration (IQR)
    iqr_desc = f"The middle 50% of records (interquartile range) lie between Q1 ({stats['q1']:.2f}) and Q3 ({stats['q3']:.2f}), representing an IQR span of {stats['iqr']:.2f} units."
    observations.append(("Interquartile Range Concentration", iqr_desc))

    # 4. Outlier Assessment (1.5 x IQR Rule)
    outlier_count = stats["outlier_count"]
    total = stats["count"]
    if outlier_count > 0:
        pct = (outlier_count / total) * 100
        outlier_desc = (
            f"Detected {outlier_count} statistical outlier{'s' if outlier_count > 1 else ''} ({pct:.1f}% of total) "
            f"falling outside the valid 1.5×IQR boundary (below {stats['lower_bound']:.2f} or above {stats['upper_bound']:.2f}). "
            f"These specific records require investigative verification for anomalous recording or distinct evidence patterns."
        )
    else:
        outlier_desc = (
            f"Zero statistical outliers detected under the standard 1.5×IQR fence. All {total} observations "
            f"fall comfortably within the expected statistical bounds ({stats['lower_bound']:.2f} to {stats['upper_bound']:.2f})."
        )
    observations.append(("Outlier & Anomaly Triaging", outlier_desc))

    return observations


def create_correlation_heatmap(df):
    numerical_data = df.select_dtypes(include="number")

    if numerical_data.shape[1] < 2:
        return None

    correlation = numerical_data.corr()

    fig = px.imshow(
        correlation,
        text_auto=".2f",
        color_continuous_scale=[
            [0.0, "#FEF2F2"],
            [0.5, "#F1F5F9"],
            [1.0, "#0F766E"]
        ],
        title="Numerical Feature Correlation Matrix"
    )

    return apply_forensic_theme(fig)


def create_bar_chart(df, column):
    counts = (
        df[column]
        .astype(str)
        .value_counts()
        .reset_index()
    )

    counts.columns = [column, "Count"]

    fig = px.bar(
        counts.head(15),
        x=column,
        y="Count",
        title=f"Category Frequency: {column}",
        color_discrete_sequence=["#0F766E"]
    )

    return apply_forensic_theme(fig)
