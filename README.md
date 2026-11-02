# FORENSIQ — Investigation Intelligence Platform

**FORENSIQ** is a structured-data forensic investigation and evidence intelligence platform engineered for digital investigators, forensic analysts, and compliance auditors. Built with Python, Streamlit, Scikit-Learn, Plotly, and ReportLab, it turns raw, structured forensic datasets into verifiable exploratory intelligence, statistical profiles, multivariate anomaly flags, and publication-ready PDF reports.

---

## Visual Identity & Design System

Built on a restrained, data-focused enterprise analytics design system:

- **Background (Deep Navy / Charcoal)**: `#0B1220`
- **Main Surfaces**: `#111B2B`
- **Secondary Surfaces**: `#172337`
- **Primary Text**: `#E8EEF5`
- **Secondary Text (Muted Slate)**: `#94A3B8`
- **Accent (Muted Teal)**: `#2DD4BF`
- **Secondary Accent (Electric Blue)**: `#3B82F6`
- **Subtle Borders**: `#263449`
- **Warning**: Muted Amber (`#F59E0B`)
- **Error**: Restrained Red (`#EF4444`)

---

## Architecture & Workflows

### 1. Dedicated Homepage / Landing Page
- **Navigation Bar**: Minimal, functional top navigation containing the FORENSIQ wordmark, Home, Capabilities, How It Works, About, and a prominent Upload Evidence CTA.
- **Hero Section**: Main heading *"Turn Evidence Data Into Structured Investigative Insights."* paired with an analytical visual showing real telemetry and parser details.
- **Platform Capabilities**: 8 structured capability overviews for profiling, EDA, anomaly detection, column intelligence, timelines, insights, query assistant, and PDF reporting.
- **How It Works**: 4-step sequence (01 Upload Evidence, 02 Analyse Dataset, 03 Explore Findings, 04 Generate Report).
- **Upload Evidence Area**: Unified drag-and-drop file uploader supporting CSV, Excel, and JSON, file size guidance, validation feedback, in-memory local privacy notice, and 1-click sample demo dataset loader.
- **Footer**: Product summary, supported formats, and responsible forensic limitations disclaimer.

### 2. Analysis Workspace
- **Navigation**: Clean, structured sidebar navigation without emojis:
  - **Overview**: Real dataset dimensions, completeness rate, duplicate count, memory footprint, SHA-256 custody digest, dataset preview, and transparent heuristic quality index with documented formula.
  - **Dataset Analysis**: Comprehensive statistical summaries, missingness audits with distribution charts, 2-column numerical histograms and boxplots, multivariate correlation heatmap, and categorical frequency distributions.
  - **Column Intelligence**: Multi-dimensional classification combining dtypes, parseability, cardinality, and naming into 7 forensic semantic roles with confidence ratings.
  - **Investigation Timeline**: Temporal reconstruction with day/week/month grouping, event density charts, and summary metrics.
  - **Anomaly Detection (Dedicated View)**: Unsupervised Isolation Forest model with configurable contamination, normalized anomaly scores, MAD robust feature deviations, and responsible triage notices.
  - **Investigation Insights**: Mathematically traceable findings categorized into `[VOLUME]`, `[INTEGRITY]`, `[DUPLICATION]`, `[DISTRIBUTION]`, `[CONCENTRATION]`, `[CHRONOLOGY]`, and `[ANOMALY]`.
  - **Ask Your Dataset**: Natural language rule-based query engine supporting counts, nulls, duplicates, averages, medians, extremes, distributions, dates, and filtering with dynamic clickable suggestions.
  - **Case Management**: Chain-of-custody case tracking with Open, Under Review, and Closed status lifecycles, and CSV docket/registry exports.
  - **Generate Report**: Publication-ready ReportLab PDF dossier compiling file custody hash, quality audits, anomaly summaries, and forensic disclaimers.

---

## Analytical Logic & Integrity Safeguards

- **Multi-Encoding Parser**: Automatic fallback across UTF-8, UTF-8-SIG, Latin1, CP1252, and ISO-8859-1 for resilient CSV ingestion.
- **Column Deduplication**: Automatically deduplicates colliding column headers with deterministic suffixes and records ingestion warnings.
- **Cryptographic Hash**: Immediate calculation of SHA-256 digest on raw evidence bytes to document original file integrity.
- **Clean Imputation**: Non-finite numbers (`Inf`, `-Inf`) converted to `NaN` and imputed via robust medians prior to model execution.
- **Constant Column Elimination**: Constant numerical features automatically excluded to prevent matrix singularities.
- **Traceable Observations**: Zero speculative or causal conclusions; all debrief points are directly linked to dataset metrics.
- **Deterministic Querying**: Transparent rule-based queries with zero hallucinated outputs.

---

## Installation & Execution

### 1. Prerequisites
Ensure Python 3.10+ is available on your workstation.

### 2. Launch Application

```bash
# Windows
.\venv\Scripts\streamlit.exe run app.py

# Or with virtual environment active:
streamlit run app.py
```

Access the interface in your browser at `http://localhost:8501`.

---

## Responsible Forensic Disclaimer
*FORENSIQ provides exploratory statistical analysis and unsupervised anomaly detection across structured datasets. Analytical observations, metrics, and anomaly review flags are mathematically derived heuristic findings intended to support human investigative triage. They do not establish legal guilt, culpability, causation, or verified forensic conclusions.*
