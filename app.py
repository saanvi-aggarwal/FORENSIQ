
import streamlit as st
import pandas as pd
import plotly.express as px
import hashlib
import os
import io

from modules.data_loader import load_dataset
from modules.data_profiler import (
    generate_profile,
    get_column_quality
)
from modules.anomaly_detection import detect_anomalies
from modules.visualizations import (
    create_histogram,
    create_boxplot,
    create_correlation_heatmap,
    create_bar_chart,
    calculate_column_statistics,
    generate_statistical_interpretation
)
from modules.column_intelligence import analyse_columns
from modules.investigation_queries import answer_question
from modules.insights import generate_insights
from modules.report_generator import generate_pdf_report

from modules.case_manager import (
    create_case,
    get_case_summary,
    update_case_status,
    export_case_details
)

from modules.ui_components import (
    get_custom_css,
    apply_forensic_theme,
    render_header,
    render_metric_card,
    render_empty_state,
    get_status_badge_html
)


# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="FORENSIQ | Investigation Intelligence",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Master Forensic Intelligence CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)


# =====================================================
# 2. SESSION STATE MANAGEMENT
# =====================================================

defaults = {
    "show_landing": True,
    "landing_show_uploader": False,
    "current_page": "Home",
    "analysis_df": None,
    "analysis_filename": None,
    "analysis_file_hash": None,
    "analysis_profile": None,
    "analysis_results": None,
    "analysis_error": None,
    "analysis_insights": None,
    "last_contamination": 0.10,
    "investigation_cases": [],
    "query_input": "",
    "active_query_text": "",
    "last_answered_query": None,
    "last_query_response": None,
    "generated_pdf_buffer": None
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val


# =====================================================
# 3. HELPER FUNCTIONS
# =====================================================

def process_loaded_dataframe(df, filename, file_hash, contamination):
    """Profile data, run anomaly detection, and generate insights."""
    st.session_state.analysis_df = df
    st.session_state.analysis_filename = filename
    st.session_state.analysis_file_hash = file_hash
    st.session_state.analysis_profile = generate_profile(df)
    
    anomaly_results, anomaly_error = detect_anomalies(df, contamination=contamination)
    st.session_state.analysis_results = anomaly_results
    st.session_state.analysis_error = anomaly_error
    st.session_state.last_contamination = contamination
    
    insights = generate_insights(df, st.session_state.analysis_profile, anomaly_results)
    st.session_state.analysis_insights = insights


def load_demo_evidence(contamination):
    """Load sample fingerprint evidence dataset for testing & demonstration."""
    sample_path = os.path.join(os.path.dirname(__file__), "sample_data", "fingerprint_evidence.csv")
    if os.path.exists(sample_path):
        with open(sample_path, "rb") as f:
            file_bytes = f.read()
        file_hash = hashlib.sha256(file_bytes).hexdigest()
        bio = io.BytesIO(file_bytes)
        bio.name = "fingerprint_evidence.csv"
        df = load_dataset(bio)
        process_loaded_dataframe(df, "fingerprint_evidence.csv", file_hash, contamination)
        st.session_state.show_landing = False
        st.session_state.current_page = "Dashboard"
        st.rerun()


def clear_evidence():
    """Unload dataset and reset analysis states."""
    st.session_state.analysis_df = None
    st.session_state.analysis_filename = None
    st.session_state.analysis_file_hash = None
    st.session_state.analysis_profile = None
    st.session_state.analysis_results = None
    st.session_state.analysis_error = None
    st.session_state.analysis_insights = None
    st.session_state.generated_pdf_buffer = None
    st.session_state.last_query_response = None
    st.rerun()


# =====================================================
# 3B. LANDING PAGE VIEW
# =====================================================

def render_landing_page(contamination):
    """Render clean, professional landing page."""
    # Top Navigation Bar
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 14px 4px 18px 4px; border-bottom: 1px solid #E2E8F0; margin-bottom: 24px;">
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 1.35rem; color: #0F766E;">🔎</span>
            <span style="font-size: 1.3rem; font-weight: 800; letter-spacing: -0.02em; color: #172033;">FORENSIQ</span>
        </div>
        <div style="display: flex; align-items: center; gap: 28px;">
            <a href="#home" style="color: #172033; font-weight: 600; text-decoration: none; font-size: 0.88rem;">Home</a>
            <a href="#about" style="color: #64748B; font-weight: 500; text-decoration: none; font-size: 0.88rem;">About</a>
            <a href="#capabilities" style="color: #64748B; font-weight: 500; text-decoration: none; font-size: 0.88rem;">Capabilities</a>
            <a href="#how-it-works" style="color: #64748B; font-weight: 500; text-decoration: none; font-size: 0.88rem;">How It Works</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Hero Section
    st.markdown('<div id="home"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="forensic-card" style="text-align: center; padding: 48px 24px; margin-bottom: 28px; background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);">
        <div class="brand-badge" style="margin-bottom: 14px;">EVIDENCE ANALYSIS &amp; DATA INTELLIGENCE</div>
        <h1 style="font-size: 2.15rem; font-weight: 800; color: #172033; margin-bottom: 14px; letter-spacing: -0.02em;">
            FORENSIQ — Evidence Analysis &amp; Investigation Intelligence
        </h1>
        <p style="font-size: 1.02rem; color: #64748B; max-width: 780px; margin: 0 auto 28px auto; line-height: 1.65;">
            FORENSIQ is a data-driven investigation analysis platform that helps users examine structured evidence datasets, explore statistical patterns, identify unusual records and generate analytical reports.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Hero CTAs
    hero_c1, hero_c2, hero_c3 = st.columns([1, 2, 1])
    with hero_c2:
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("📤 Upload Evidence", use_container_width=True, key="landing_hero_upload_btn"):
                st.session_state.landing_show_uploader = True
        with btn_col2:
            if st.button("🔍 Explore Platform", use_container_width=True, key="landing_hero_explore_btn"):
                st.session_state.show_landing = False
                st.session_state.current_page = "Dashboard"
                st.rerun()

    # Upload evidence widget on landing page when requested or always cleanly accessible
    if st.session_state.landing_show_uploader:
        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="forensic-card" style="border: 2px dashed #0F766E; background: #FFFFFF; max-width: 780px; margin: 0 auto 24px auto;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <h3 style="margin: 0; font-size: 1.1rem; color: #0F766E;">Upload Evidence Dataset</h3>
                <span class="forensic-badge badge-info">CSV, XLSX, JSON SUPPORTED</span>
            </div>
            <p style="font-size: 0.85rem; color: #64748B; margin-bottom: 14px;">Select your forensic evidence file. Once uploaded, FORENSIQ will immediately profile and transition into your investigation dashboard.</p>
        """, unsafe_allow_html=True)

        landing_file = st.file_uploader(
            "Select evidence dataset",
            type=["csv", "xlsx", "json"],
            key="landing_page_uploader",
            help="Upload forensic datasets in CSV, Excel, or JSON format."
        )

        if landing_file is not None:
            try:
                l_bytes = landing_file.getvalue()
                l_hash = hashlib.sha256(l_bytes).hexdigest()
                landing_file.seek(0)
                l_df = load_dataset(landing_file)
                process_loaded_dataframe(l_df, landing_file.name, l_hash, contamination)
                st.session_state.show_landing = False
                st.session_state.current_page = "Dashboard"
                st.rerun()
            except Exception as e:
                st.error(f"Upload failed: {e}")

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # About Section
    st.markdown('<div id="about"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="forensic-card">
        <div class="forensic-card-header">
            <div>
                <h3 class="forensic-card-title"><span>🛡️</span> About FORENSIQ</h3>
                <p class="forensic-card-desc">Purpose-built structured evidence intelligence and exploratory triage system.</p>
            </div>
        </div>
        <p style="font-size: 0.95rem; color: #172033; line-height: 1.6; margin-bottom: 16px;">
            FORENSIQ helps investigators and data analysts extract transparent, verifiable insights from complex structured data:
        </p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin-top: 10px;">
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px;">
                <strong style="color: #0F766E; font-size: 0.9rem; display: block; margin-bottom: 4px;">📊 Evidence Profiling</strong>
                <span style="font-size: 0.82rem; color: #64748B;">Comprehensive missing value, duplicate, and column health metrics.</span>
            </div>
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px;">
                <strong style="color: #0F766E; font-size: 0.9rem; display: block; margin-bottom: 4px;">📈 Exploratory EDA</strong>
                <span style="font-size: 0.82rem; color: #64748B;">Statistical distributions, outlier boxplots, and feature correlations.</span>
            </div>
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px;">
                <strong style="color: #0F766E; font-size: 0.9rem; display: block; margin-bottom: 4px;">🚨 Anomaly Detection</strong>
                <span style="font-size: 0.82rem; color: #64748B;">Isolation Forest algorithm highlighting unusual multivariate patterns.</span>
            </div>
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px;">
                <strong style="color: #0F766E; font-size: 0.9rem; display: block; margin-bottom: 4px;">💡 Investigation Insights</strong>
                <span style="font-size: 0.82rem; color: #64748B;">Automated data quality and distribution triage observations.</span>
            </div>
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px;">
                <strong style="color: #0F766E; font-size: 0.9rem; display: block; margin-bottom: 4px;">📑 Report Generation</strong>
                <span style="font-size: 0.82rem; color: #64748B;">One-click publication-ready PDF forensic investigation dossiers.</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Capabilities Section
    st.markdown('<div id="capabilities"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="forensic-card">
        <div class="forensic-card-header">
            <div>
                <h3 class="forensic-card-title"><span>⚡</span> Core Platform Capabilities</h3>
                <p class="forensic-card-desc">Advanced analytical capabilities designed for digital and data investigations.</p>
            </div>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px;">
            <div style="padding: 12px 14px; border-left: 3px solid #0F766E; background: #F8FAFC; border-radius: 6px;">
                <strong style="font-size: 0.9rem; color: #172033;">Column Intelligence</strong>
                <p style="font-size: 0.8rem; color: #64748B; margin: 4px 0 0 0;">Automatic heuristic role classification for identifiers, locations, timestamps, and measurements.</p>
            </div>
            <div style="padding: 12px 14px; border-left: 3px solid #2563EB; background: #F8FAFC; border-radius: 6px;">
                <strong style="font-size: 0.9rem; color: #172033;">Investigation Timeline</strong>
                <p style="font-size: 0.8rem; color: #64748B; margin: 4px 0 0 0;">Chronological reconstruction identifying evidence collection cadence and peak intervals.</p>
            </div>
            <div style="padding: 12px 14px; border-left: 3px solid #0F766E; background: #F8FAFC; border-radius: 6px;">
                <strong style="font-size: 0.9rem; color: #172033;">Ask Your Dataset</strong>
                <p style="font-size: 0.8rem; color: #64748B; margin: 4px 0 0 0;">Deterministic query engine delivering answers without hallucinations or external APIs.</p>
            </div>
            <div style="padding: 12px 14px; border-left: 3px solid #15803D; background: #F8FAFC; border-radius: 6px;">
                <strong style="font-size: 0.9rem; color: #172033;">Case Docket Management</strong>
                <p style="font-size: 0.8rem; color: #64748B; margin: 4px 0 0 0;">Chain-of-custody tracking, investigator assignments, and case registry CSV export.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # How It Works Section
    st.markdown('<div id="how-it-works"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="forensic-card">
        <div class="forensic-card-header">
            <div>
                <h3 class="forensic-card-title"><span>🔄</span> How It Works</h3>
                <p class="forensic-card-desc">Four simple steps from raw evidence dataset to forensic report.</p>
            </div>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;">
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 18px 14px; text-align: center;">
                <div style="font-size: 1.4rem; font-weight: 800; color: #0F766E; margin-bottom: 6px;">1</div>
                <strong style="font-size: 0.88rem; color: #172033; display: block; margin-bottom: 6px;">Upload Dataset</strong>
                <span style="font-size: 0.8rem; color: #64748B;">Upload your structured evidence in CSV, XLSX, or JSON format.</span>
            </div>
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 18px 14px; text-align: center;">
                <div style="font-size: 1.4rem; font-weight: 800; color: #0F766E; margin-bottom: 6px;">2</div>
                <strong style="font-size: 0.88rem; color: #172033; display: block; margin-bottom: 6px;">Analyse Dataset</strong>
                <span style="font-size: 0.8rem; color: #64748B;">Automatic data profiling, data hygiene checks, and anomaly scanning.</span>
            </div>
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 18px 14px; text-align: center;">
                <div style="font-size: 1.4rem; font-weight: 800; color: #0F766E; margin-bottom: 6px;">3</div>
                <strong style="font-size: 0.88rem; color: #172033; display: block; margin-bottom: 6px;">Explore Findings</strong>
                <span style="font-size: 0.8rem; color: #64748B;">Inspect distributions, explore correlations, and query specific evidence.</span>
            </div>
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 18px 14px; text-align: center;">
                <div style="font-size: 1.4rem; font-weight: 800; color: #0F766E; margin-bottom: 6px;">4</div>
                <strong style="font-size: 0.88rem; color: #172033; display: block; margin-bottom: 6px;">Generate Report</strong>
                <span style="font-size: 0.8rem; color: #64748B;">Export formal, publication-ready PDF dossiers for your case file.</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="margin-top: 36px; padding: 20px 0; border-top: 1px solid #E2E8F0; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
        <div style="font-size: 0.82rem; color: #172033;">
            <strong>FORENSIQ</strong> — Structured Evidence Analysis &amp; Investigation Intelligence Platform.
        </div>
        <div style="font-size: 0.75rem; color: #94A3B8;">
            Exploratory forensic intelligence. Outputs require independent verification.
        </div>
    </div>
    """, unsafe_allow_html=True)



# =====================================================
# 4. SIDEBAR NAVIGATION & CONTROLS
# =====================================================

# Brand Header
st.sidebar.markdown("""
<div class="sidebar-brand-container">
    <div class="brand-badge">● FORENSIC INTELLIGENCE</div>
    <div class="brand-title">
        <span style="color: #0F766E;">🔎</span> FORENSIQ
    </div>
    <div class="brand-subtitle">INVESTIGATION INTELLIGENCE</div>
</div>
""", unsafe_allow_html=True)

# Navigation Menu
nav_map = {
    "Home":                   "Home",
    "Dashboard":              "Dashboard",
    "Case Management":        "Case Management",
    "Dataset Analysis":       "Dataset Analysis",
    "Column Intelligence":    "Column Intelligence",
    "Investigation Timeline": "Investigation Timeline",
    "Investigation Insights": "Investigation Insights",
    "Ask Your Dataset":       "Ask Your Dataset",
    "Generate Report":        "Generate Report"
}

st.sidebar.markdown('<div style="font-size: 0.72rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px;">Workspace Navigation</div>', unsafe_allow_html=True)

nav_keys = list(nav_map.keys())

# Sync radio key with session state before instantiation if changed programmatically
if "_sidebar_nav_choice" not in st.session_state or st.session_state["_sidebar_nav_choice"] != st.session_state.current_page:
    st.session_state["_sidebar_nav_choice"] = st.session_state.current_page

def on_nav_change():
    """Callback triggered when user selects a radio option."""
    selected = st.session_state["_sidebar_nav_choice"]
    st.session_state.current_page = selected
    st.session_state.show_landing = (selected == "Home")

page = st.sidebar.radio(
    "NAVIGATION",
    nav_keys,
    key="_sidebar_nav_choice",
    on_change=on_nav_change,
    format_func=lambda x: nav_map[x],
    label_visibility="collapsed"
)

# Ensure page variable reflects current active page
page = st.session_state.current_page

st.sidebar.markdown("---")

# Evidence Dataset Upload Section
st.sidebar.markdown('<div style="font-size: 0.72rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;">Evidence Ingestion</div>', unsafe_allow_html=True)

uploaded_file = st.sidebar.file_uploader(
    "Upload evidence dataset",
    type=["csv", "xlsx", "json"],
    help="Upload forensic datasets in CSV, Excel, or JSON format for automated analysis."
)

# Anomaly Sensitivity Engine
st.sidebar.markdown('<div style="font-size: 0.72rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 14px; margin-bottom: 6px;">Anomaly Sensitivity</div>', unsafe_allow_html=True)

contamination = st.sidebar.slider(
    "Contamination rate",
    min_value=0.05,
    max_value=0.30,
    value=float(st.session_state.last_contamination or 0.10),
    step=0.05,
    help="Expected proportion of unusual records evaluated by the Isolation Forest model.",
    label_visibility="collapsed"
)

# =====================================================
# 5. DATASET PROCESSING LOGIC
# =====================================================

if uploaded_file is not None:
    try:
        file_bytes = uploaded_file.getvalue()
        current_file_hash = hashlib.sha256(file_bytes).hexdigest()

        # Genuine change or new file
        if st.session_state.analysis_file_hash != current_file_hash:
            uploaded_file.seek(0)
            df = load_dataset(uploaded_file)
            process_loaded_dataframe(df, uploaded_file.name, current_file_hash, contamination)
            st.session_state.show_landing = False
            st.session_state.current_page = "Dashboard"
            st.rerun()

    except Exception as error:
        st.sidebar.error(f"Ingestion failed: {error}")

# If sensitivity slider changed on existing dataset, re-evaluate anomalies
if st.session_state.analysis_df is not None:
    if st.session_state.last_contamination != contamination or st.session_state.analysis_results is None:
        anomaly_results, anomaly_error = detect_anomalies(
            st.session_state.analysis_df,
            contamination=contamination
        )
        st.session_state.analysis_results = anomaly_results
        st.session_state.analysis_error = anomaly_error
        st.session_state.last_contamination = contamination
        st.session_state.analysis_insights = generate_insights(
            st.session_state.analysis_df,
            st.session_state.analysis_profile,
            anomaly_results
        )

# Display Sidebar Evidence Status
if st.session_state.analysis_df is not None:
    p = st.session_state.analysis_profile
    st.sidebar.markdown(f"""
    <div class="sidebar-evidence-card">
        <div class="sidebar-status-pill status-active">● EVIDENCE VERIFIED</div>
        <div style="font-weight: 700; font-size: 0.85rem; color: #172033; word-break: break-all; margin-bottom: 4px;">{st.session_state.analysis_filename}</div>
        <div style="font-size: 0.74rem; color: #64748B;">{p['total_rows']:,} records &bull; {p['total_columns']} columns</div>
        <div class="mono-pill" style="margin-top: 6px; font-size: 0.68rem; display: block; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
            SHA: {st.session_state.analysis_file_hash[:16]}...
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.sidebar.button("Unload Evidence", use_container_width=True):
        clear_evidence()
else:
    st.sidebar.markdown("""
    <div class="sidebar-evidence-card">
        <div class="sidebar-status-pill status-empty">○ AWAITING DATASET</div>
        <div style="font-size: 0.74rem; color: #64748B; margin-top: 4px;">No evidence file currently ingested into the workspace.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.sidebar.button("Load Demo Evidence", use_container_width=True, help="Load built-in fingerprint evidence dataset for instant demonstration."):
        load_demo_evidence(contamination)

# Sidebar Footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="text-align: center; padding: 4px;">
    <div style="font-size: 0.7rem; font-weight: 700; color: #94A3B8; letter-spacing: 0.05em;">FORENSIQ INTELLIGENCE v2.0</div>
    <div style="font-size: 0.65rem; color: #94A3B8; margin-top: 2px;">Exploratory Forensic System</div>
</div>
""", unsafe_allow_html=True)


# =====================================================
# ACTIVE STATE VARIABLES
# =====================================================

df = st.session_state.analysis_df
profile = st.session_state.analysis_profile
anomaly_results = st.session_state.analysis_results
anomaly_error = st.session_state.analysis_error
insights = st.session_state.analysis_insights
cases = st.session_state.investigation_cases


# =====================================================
# 6. ROUTER & PAGE IMPLEMENTATIONS
# =====================================================

if st.session_state.show_landing or page == "Home":
    render_landing_page(contamination)

# -----------------------------------------------------
# PAGE 1: DASHBOARD
# -----------------------------------------------------
elif page == "Dashboard":
    render_header(
        title="Investigation Overview",
        subtitle="Monitor forensic investigation cases and analyse evidence datasets.",
        badge="OPERATIONAL COMMAND"
    )

    # Top Metric Cards: Cases, Records, Columns, Flagged Records
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric_card(
            label="Investigation Cases",
            value=str(len(cases)),
            subtext="Registered dockets",
            icon="📁",
            border_accent="teal"
        )
    with col2:
        val = f"{profile['total_rows']:,}" if profile else "N/A"
        render_metric_card(
            label="Total Records",
            value=val,
            subtext="Evidence items loaded" if profile else "Awaiting dataset",
            icon="📋",
            border_accent="blue"
        )
    with col3:
        val = str(profile['total_columns']) if profile else "N/A"
        render_metric_card(
            label="Total Columns",
            value=val,
            subtext="Feature dimensions" if profile else "Awaiting dataset",
            icon="📊",
            border_accent="green"
        )
    with col4:
        if anomaly_results is not None:
            flagged_cnt = int((anomaly_results["Anomaly Status"] == "Flagged for Review").sum())
            val = str(flagged_cnt)
            sub = f"Isolation Forest ({int(contamination*100)}% sens.)"
        else:
            val = "0" if profile else "N/A"
            sub = "Anomaly scan pending" if profile else "Awaiting dataset"
        render_metric_card(
            label="Flagged Records",
            value=val,
            subtext=sub,
            icon="🚨",
            border_accent="red" if (val != "0" and val != "N/A") else "teal"
        )

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # If dataset is loaded, show full organized sections A, B, C
    if df is not None:
        # A. Dataset Overview
        st.markdown("""
        <div class="forensic-card">
            <div class="forensic-card-header">
                <div>
                    <h3 class="forensic-card-title"><span>📂</span> Dataset Overview</h3>
                    <p class="forensic-card-desc">Core integrity metrics and forensic evidence custody summary.</p>
                </div>
                <div>
                    <span class="forensic-badge badge-cyan">● VERIFIED DOSSIER</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        ov_col1, ov_col2, ov_col3, ov_col4, ov_col5 = st.columns(5)
        with ov_col1:
            st.metric("Evidence Filename", st.session_state.analysis_filename)
        with ov_col2:
            st.metric("Total Records", f"{profile['total_rows']:,}")
        with ov_col3:
            st.metric("Total Columns", profile['total_columns'])
        with ov_col4:
            st.metric("Missing Cells", profile['missing_cells'])
        with ov_col5:
            st.metric("Duplicate Records", profile['duplicate_rows'])

        st.markdown("</div>", unsafe_allow_html=True)

        # B. Dataset Preview
        st.markdown("""
        <div class="forensic-card">
            <div class="forensic-card-header">
                <div>
                    <h3 class="forensic-card-title"><span>🔍</span> Dataset Preview</h3>
                    <p class="forensic-card-desc">Structured tabular view of ingested evidence entries.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        limit_col, _ = st.columns([2, 6])
        with limit_col:
            preview_rows = st.selectbox("Display Row Limit", [10, 20, 50, 100], index=1, key="dash_preview_rows")

        st.dataframe(
            df.head(preview_rows),
            use_container_width=True,
            hide_index=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # C. Dataset Quality Analysis
        st.markdown("""
        <div class="forensic-card">
            <div class="forensic-card-header">
                <div>
                    <h3 class="forensic-card-title"><span>🛡️</span> Dataset Quality & Attribute Audit</h3>
                    <p class="forensic-card-desc">Data completeness, type integrity, and cardinality assessment per column.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        quality_df = get_column_quality(df)
        st.dataframe(
            quality_df,
            use_container_width=True,
            hide_index=True
        )

        col_q1, col_q2 = st.columns(2)
        with col_q1:
            st.markdown(f"**Numerical Features ({len(profile['numerical_columns'])})**")
            if profile["numerical_columns"]:
                badges = " ".join([f"<span class='mono-pill' style='margin-right: 6px; margin-bottom: 6px; display: inline-block;'>{col}</span>" for col in profile["numerical_columns"]])
                st.markdown(badges, unsafe_allow_html=True)
            else:
                st.caption("No numerical features identified.")
        with col_q2:
            st.markdown(f"**Categorical Features ({len(profile['categorical_columns'])})**")
            if profile["categorical_columns"]:
                badges = " ".join([f"<span class='mono-pill' style='margin-right: 6px; margin-bottom: 6px; display: inline-block;'>{col}</span>" for col in profile["categorical_columns"]])
                st.markdown(badges, unsafe_allow_html=True)
            else:
                st.caption("No categorical features identified.")

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        # Attractive empty state for dataset sections
        render_empty_state(
            icon="🛰️",
            title="Evidence Ingestion Required",
            message="Upload a forensic dataset (.csv, .xlsx, or .json) via the left sidebar, or click the quick demo loader to immediately explore forensic analytics and automated profiling."
        )
        empty_c1, empty_c2, empty_c3 = st.columns([1, 2, 1])
        with empty_c2:
            if st.button("Quick Load Demo Evidence (Fingerprint)", use_container_width=True, key="dash_empty_demo_btn"):
                load_demo_evidence(contamination)

    # D. Recent Investigation Cases (Always displayed!)
    st.markdown("""
    <div class="forensic-card">
        <div class="forensic-card-header">
            <div>
                <h3 class="forensic-card-title"><span>📁</span> Recent Investigation Cases</h3>
                <p class="forensic-card-desc">Active forensic case dockets and investigator assignments.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if cases:
        case_rows = []
        for c in cases[-5:]:
            case_rows.append({
                "Case ID": c["case_id"],
                "Case Title": c["title"],
                "Investigator": c["investigator"],
                "Status": c["status"],
                "Creation Date": c["created_at"]
            })
        cases_df = pd.DataFrame(case_rows)
        st.dataframe(
            cases_df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No investigation cases recorded. Navigate to the Case Management module to register your first investigation docket.")

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------
# PAGE 2: CASE MANAGEMENT
# -----------------------------------------------------
elif page == "Case Management":
    render_header(
        title="Investigation Cases",
        subtitle="Register, update, and manage forensic evidence dockets.",
        badge="DOCKET MANAGEMENT"
    )

    # Top Case Metrics
    c_open = sum(c["status"] == "Open" for c in cases)
    c_review = sum(c["status"] == "Under Review" for c in cases)
    c_closed = sum(c["status"] == "Closed" for c in cases)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric_card("Total Cases", str(len(cases)), "All active & archived dockets", "📁", "teal")
    with col2:
        render_metric_card("Open Cases", str(c_open), "Active investigation underway", "🟢", "green")
    with col3:
        render_metric_card("Under Review", str(c_review), "Peer review / audit stage", "🟡", "amber")
    with col4:
        render_metric_card("Closed Cases", str(c_closed), "Resolved investigation cases", "⚪", "blue")

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # Form: Create New Case
    st.markdown("""
    <div class="forensic-card" style="border-left: 3px solid #0F766E;">
        <div class="forensic-card-header">
            <div>
                <h3 class="forensic-card-title"><span>➕</span> Register New Investigation Case</h3>
                <p class="forensic-card-desc">Initialize a new case docket with chain-of-custody tracking.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    with st.form("create_case_form", clear_on_submit=True):
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            case_title = st.text_input(
                "Investigation Title *",
                placeholder="e.g. Latent Fingerprint Cross-Verification Docket"
            )
        with f_col2:
            investigator = st.text_input(
                "Investigator Name *",
                placeholder="e.g. Det. Sarah Vance / Forensic Unit"
            )
        
        description = st.text_area(
            "Case Scope & Objectives",
            placeholder="Outline incident details, forensic objectives, evidence origin, and analytical scope..."
        )

        submitted = st.form_submit_button("Create Investigation Case", use_container_width=True)
        if submitted:
            if not case_title.strip() or not investigator.strip():
                st.error("Both Investigation Title and Investigator Name are required to initialize a case.")
            else:
                new_case = create_case(
                    title=case_title.strip(),
                    investigator=investigator.strip(),
                    description=description.strip()
                )
                st.session_state.investigation_cases.append(new_case)
                st.success(f"Case successfully initialized. Assigned Docket ID: {new_case['case_id']}")
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Investigation Dockets List
    st.markdown("""
    <div class="forensic-card">
        <div class="forensic-card-header">
            <div>
                <h3 class="forensic-card-title"><span>📑</span> Registered Investigation Dockets</h3>
                <p class="forensic-card-desc">Review, adjust status, and export case summary documentation.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if cases:
        for idx, case in enumerate(cases):
            summary = get_case_summary(case)
            status_badge = get_status_badge_html(case["status"])

            with st.expander(f"{case['case_id']} — {case['title']}  |  {case['status']}", expanded=(idx == len(cases) - 1)):
                d_col1, d_col2 = st.columns([2, 1])
                with d_col1:
                    st.markdown(f"""
                    <div style="margin-bottom: 8px;">
                        <span style="color: #64748B; font-size: 0.8rem; text-transform: uppercase;">Case Docket ID:</span>
                        <span class="mono-pill" style="font-size: 0.85rem; margin-left: 6px;">{case['case_id']}</span>
                    </div>
                    <div style="margin-bottom: 8px;">
                        <span style="color: #64748B; font-size: 0.8rem; text-transform: uppercase;">Lead Investigator:</span>
                        <strong style="color: #172033; margin-left: 6px;">{case['investigator']}</strong>
                    </div>
                    <div style="margin-bottom: 8px;">
                        <span style="color: #64748B; font-size: 0.8rem; text-transform: uppercase;">Creation Date:</span>
                        <span style="color: #172033; margin-left: 6px;">{case['created_at']}</span>
                    </div>
                    <div style="margin-top: 12px;">
                        <span style="color: #64748B; font-size: 0.8rem; text-transform: uppercase; display: block; margin-bottom: 4px;">Investigation Scope:</span>
                        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 10px; font-size: 0.88rem; color: #172033;">
                            {case['description'] if case['description'] else 'No additional scope notes recorded.'}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with d_col2:
                    st.markdown("<span style='color: #64748B; font-size: 0.8rem; text-transform: uppercase;'>Current Status</span>", unsafe_allow_html=True)
                    st.markdown(f"<div style='margin-top: 4px; margin-bottom: 12px;'>{status_badge}</div>", unsafe_allow_html=True)

                    status_options = ["Open", "Under Review", "Closed"]
                    curr_index = status_options.index(case["status"]) if case["status"] in status_options else 0
                    
                    selected_status = st.selectbox(
                        "Update Status",
                        status_options,
                        index=curr_index,
                        key=f"status_select_{case['case_id']}"
                    )

                    if selected_status != case["status"]:
                        update_case_status(case, selected_status)
                        st.success(f"Status updated to '{selected_status}'")
                        st.rerun()

                    csv_data = export_case_details(case)
                    st.download_button(
                        label="Export Case Details (CSV)",
                        data=csv_data,
                        file_name=f"{case['case_id']}_docket.csv",
                        mime="text/csv",
                        key=f"dl_case_{case['case_id']}",
                        use_container_width=True
                    )

        # Batch Export All Cases
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        all_cases_df = pd.DataFrame([get_case_summary(c) for c in cases])
        st.download_button(
            label="Export Master Case Registry (CSV)",
            data=all_cases_df.to_csv(index=False).encode("utf-8"),
            file_name="FORENSIQ_Master_Case_Registry.csv",
            mime="text/csv",
            key="dl_master_registry"
        )
    else:
        st.info("No investigation cases recorded yet. Complete the registration form above to open an investigation docket.")

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------
# PAGE 3: DATASET ANALYSIS (EDA)
# -----------------------------------------------------
elif page == "Dataset Analysis":
    render_header(
        title="Exploratory Data Analysis",
        subtitle="Deep statistical profiling, distributions, and multi-attribute correlation.",
        badge="STATISTICAL PROFILING"
    )

    if df is None:
        render_empty_state(
            icon="📈",
            title="Evidence Dataset Required",
            message="Upload an evidence dataset via the sidebar to unlock statistical feature profiling, distribution analysis, and correlation mapping."
        )
    else:
        # 1. Statistical Summary
        st.markdown("""
        <div class="forensic-card">
            <div class="forensic-card-header">
                <div>
                    <h3 class="forensic-card-title"><span>📊</span> Comprehensive Statistical Summary</h3>
                    <p class="forensic-card-desc">Parametric and non-parametric distribution statistics across all dataset features.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.dataframe(
            profile["summary"],
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # 2. Missing Value Analysis
        st.markdown("""
        <div class="forensic-card">
            <div class="forensic-card-header">
                <div>
                    <h3 class="forensic-card-title"><span>🔍</span> Missing Value Analysis</h3>
                    <p class="forensic-card-desc">Detection of gaps, data truncation, or missing custody attributes.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        missing_series = profile["missing_by_column"]
        missing_filtered = missing_series[missing_series > 0]

        if not missing_filtered.empty:
            m_col1, m_col2 = st.columns([1, 2])
            with m_col1:
                st.metric("Total Missing Cells", profile["missing_cells"])
                st.metric("Affected Attributes", len(missing_filtered))
                st.dataframe(
                    pd.DataFrame({"Column": missing_filtered.index, "Missing Count": missing_filtered.values}),
                    use_container_width=True,
                    hide_index=True
                )
            with m_col2:
                fig_m = px.bar(
                    x=missing_filtered.index,
                    y=missing_filtered.values,
                    labels={"x": "Attribute", "y": "Missing Count"},
                    title="Missing Cell Distribution",
                    color_discrete_sequence=["#E11D48"]
                )
                st.plotly_chart(apply_forensic_theme(fig_m), use_container_width=True)
        else:
            st.success("Data Integrity Verified: Zero missing values detected across all attributes.")

        st.markdown("</div>", unsafe_allow_html=True)

        # 3. Numerical Feature Analysis
        st.markdown("""
        <div class="forensic-card">
            <div class="forensic-card-header">
                <div>
                    <h3 class="forensic-card-title"><span>📐</span> Numerical Feature Analysis</h3>
                    <p class="forensic-card-desc">Statistical distributions, central tendency benchmarks, and outlier dispersion.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        num_cols = profile["numerical_columns"]
        if num_cols:
            sel_num = st.selectbox(
                "Select Numerical Attribute",
                num_cols,
                key="eda_num_col_select"
            )

            # Calculate dynamic statistics for the selected numerical attribute
            col_stats = calculate_column_statistics(df, sel_num)

            if col_stats is not None:
                # 3A. Statistical Summary Cards (KPIs)
                st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
                kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5, kpi_col6 = st.columns(6)
                
                with kpi_col1:
                    render_metric_card(
                        label="Observations",
                        value=f"{col_stats['count']:,}",
                        subtext="Valid numerical records",
                        icon="📋",
                        border_accent="slate"
                    )
                with kpi_col2:
                    render_metric_card(
                        label="Mean (Average)",
                        value=f"{col_stats['mean']:.2f}",
                        subtext=f"Std Dev: {col_stats['std']:.2f}",
                        icon="⚖️",
                        border_accent="blue"
                    )
                with kpi_col3:
                    render_metric_card(
                        label="Median (Q2)",
                        value=f"{col_stats['median']:.2f}",
                        subtext=f"IQR: {col_stats['iqr']:.2f}",
                        icon="🎯",
                        border_accent="teal"
                    )
                with kpi_col4:
                    render_metric_card(
                        label="Std Deviation",
                        value=f"{col_stats['std']:.2f}",
                        subtext=f"Spread around mean",
                        icon="📐",
                        border_accent="amber"
                    )
                with kpi_col5:
                    render_metric_card(
                        label="Min / Max Range",
                        value=f"[{col_stats['min']:.1f}, {col_stats['max']:.1f}]",
                        subtext=f"Span: {col_stats['max'] - col_stats['min']:.2f}",
                        icon="↔️",
                        border_accent="slate"
                    )
                with kpi_col6:
                    outlier_accent = "red" if col_stats["outlier_count"] > 0 else "green"
                    render_metric_card(
                        label="Outliers",
                        value=str(col_stats["outlier_count"]),
                        subtext="Outside 1.5×IQR boundary",
                        icon="🚨",
                        border_accent=outlier_accent
                    )

                # Statistical Concepts Information Strip
                st.markdown("""
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 10px 14px; margin: 14px 0 16px 0; display: flex; flex-wrap: wrap; gap: 16px; font-size: 0.78rem; color: #64748B;">
                    <span><strong>ℹ️ Mean:</strong> Arithmetic average representing overall benchmark.</span>
                    <span><strong>Median:</strong> Middle observation unaffected by extreme values.</span>
                    <span><strong>IQR (Interquartile Range):</strong> Range of middle 50% of data (Q3 − Q1).</span>
                    <span><strong>Outliers:</strong> Points beyond Q1 − 1.5×IQR or Q3 + 1.5×IQR.</span>
                </div>
                """, unsafe_allow_html=True)

                # 3B. High-Definition Charts in 2-column layout
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(
                        create_histogram(df, sel_num),
                        use_container_width=True
                    )
                with col2:
                    st.plotly_chart(
                        create_boxplot(df, sel_num),
                        use_container_width=True
                    )

                # 3C. Automatic Statistical Interpretation ("What This Data Tells Us")
                st.markdown("""
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-left: 3px solid #0F766E; border-radius: 8px; padding: 16px 20px; margin-top: 16px; margin-bottom: 20px;">
                    <div style="font-size: 0.72rem; font-weight: 700; color: #0F766E; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;">
                        INVESTIGATIVE INTERPRETATION
                    </div>
                    <h4 style="margin: 0 0 10px 0; color: #172033; font-size: 1.05rem;">What This Data Tells Us</h4>
                """, unsafe_allow_html=True)

                interpretations = generate_statistical_interpretation(col_stats, sel_num)
                for topic, observation in interpretations:
                    st.markdown(f"""
                    <div style="margin-bottom: 8px; font-size: 0.85rem; line-height: 1.55; color: #172033;">
                        <strong style="color: #0F766E;">&bull; {topic}:</strong> {observation}
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

            else:
                st.info(f"Insufficient numerical records available in attribute '{sel_num}' to compute statistics.")

            # Correlation Heatmap
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            st.markdown("#### Multivariate Correlation Matrix")
            corr_fig = create_correlation_heatmap(df)
            if corr_fig is not None:
                st.plotly_chart(corr_fig, use_container_width=True)
            else:
                st.info("Multivariate correlation requires at least 2 numerical features.")
        else:
            st.warning("No numerical attributes detected in the uploaded evidence dataset.")

        st.markdown("</div>", unsafe_allow_html=True)

        # 4. Categorical Feature Analysis
        st.markdown("""
        <div class="forensic-card">
            <div class="forensic-card-header">
                <div>
                    <h3 class="forensic-card-title"><span>🏷️</span> Categorical Feature Analysis</h3>
                    <p class="forensic-card-desc">Frequency distribution across discrete investigation factors and categories.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        cat_cols = profile["categorical_columns"]
        if cat_cols:
            sel_cat = st.selectbox(
                "Select Categorical Attribute",
                cat_cols,
                key="eda_cat_col_select"
            )
            st.plotly_chart(
                create_bar_chart(df, sel_cat),
                use_container_width=True
            )
        else:
            st.info("No categorical attributes detected in the uploaded evidence dataset.")

        st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------
# PAGE 4: COLUMN INTELLIGENCE
# -----------------------------------------------------
elif page == "Column Intelligence":
    render_header(
        title="Column Intelligence",
        subtitle="Automatic heuristic classification of evidence attributes into forensic roles.",
        badge="SEMANTIC CLASSIFICATION"
    )

    if df is None:
        render_empty_state(
            icon="🧠",
            title="Evidence Dataset Required",
            message="Upload an evidence dataset via the sidebar to initiate heuristic column classification and semantic attribute mapping."
        )
    else:
        # Explanation card
        st.markdown("""
        <div class="forensic-card" style="border-left: 3px solid #0F766E;">
            <div class="forensic-card-header">
                <div>
                    <h3 class="forensic-card-title"><span>ℹ️</span> Heuristic Semantic Classification</h3>
                    <p class="forensic-card-desc">How FORENSIQ audits and categorizes evidence data attributes.</p>
                </div>
            </div>
            <p style="font-size: 0.88rem; color: #64748B; line-height: 1.6; margin: 0;">
                FORENSIQ inspects naming conventions, cardinality, null density, and data types to classify each attribute into a forensic role:
                <strong>Identifier</strong> (evidence IDs, reference tokens), 
                <strong>Location</strong> (physical sites, coordinates, geographic tags), 
                <strong>Time / Date</strong> (temporal timestamps for sequencing), 
                <strong>Categorical</strong> (discrete classes, examiners, types), or 
                <strong>Numerical Measurement</strong> (quantitative scores, metrics, measurements).
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Analysis Table
        col_report = analyse_columns(df)

        st.markdown("""
        <div class="forensic-card">
            <div class="forensic-card-header">
                <div>
                    <h3 class="forensic-card-title"><span>📋</span> Attribute Classification Registry</h3>
                    <p class="forensic-card-desc">Detected semantic roles, uniqueness counts, and missing rate audits.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.dataframe(
            col_report,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            label="Download Column Intelligence Report (CSV)",
            data=col_report.to_csv(index=False).encode("utf-8"),
            file_name="FORENSIQ_Column_Intelligence.csv",
            mime="text/csv",
            key="dl_col_intel"
        )

        st.markdown("""
        <p style="font-size: 0.75rem; color: #94A3B8; margin-top: 14px; margin-bottom: 0;">
            Note: Column classifications are heuristic inferences intended to accelerate evidence profiling and should be verified by the lead investigator.
        </p>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------
# PAGE 5: INVESTIGATION TIMELINE
# -----------------------------------------------------
elif page == "Investigation Timeline":
    render_header(
        title="Investigation Timeline",
        subtitle="Temporal distribution of evidence records and chronological sequence analysis.",
        badge="TEMPORAL RECONSTRUCTION"
    )

    if df is None:
        render_empty_state(
            icon="⏱️",
            title="Evidence Dataset Required",
            message="Upload an evidence dataset via the sidebar to analyze evidence collection sequences across dates and chronological timestamps."
        )
    else:
        # Identify timeline columns
        time_columns = [
            col for col in df.columns
            if any(term in col.lower() for term in ["date", "time", "timestamp", "day", "month", "year"])
        ]

        if time_columns:
            st.markdown("""
            <div class="forensic-card">
                <div class="forensic-card-header">
                    <div>
                        <h3 class="forensic-card-title"><span>⏳</span> Evidence Chronology</h3>
                        <p class="forensic-card-desc">Chronological density and collection cadence across the selected temporal index.</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            sel_col_wrap, _ = st.columns([2, 2])
            with sel_col_wrap:
                selected_time = st.selectbox(
                    "Select Timeline Attribute",
                    time_columns,
                    key="timeline_col_select"
                )

            # Build timeline series
            timeline_data = df.copy()
            if pd.api.types.is_numeric_dtype(timeline_data[selected_time]):
                timeline_data = timeline_data.dropna(subset=[selected_time])
            else:
                timeline_data[selected_time] = pd.to_datetime(timeline_data[selected_time], errors="coerce")
                timeline_data = timeline_data.dropna(subset=[selected_time])

            timeline = (
                timeline_data
                .groupby(selected_time)
                .size()
                .reset_index(name="Record Count")
            )

            if not timeline.empty:
                # Summary metrics
                t_total = int(timeline["Record Count"].sum())
                t_peak_idx = timeline["Record Count"].idxmax()
                t_peak_val = timeline.iloc[t_peak_idx][selected_time]
                t_peak_cnt = timeline.iloc[t_peak_idx]["Record Count"]

                tm_col1, tm_col2, tm_col3 = st.columns(3)
                with tm_col1:
                    render_metric_card("Indexed Records", f"{t_total:,}", "Chronologically mapped", "📋", "teal")
                with tm_col2:
                    render_metric_card("Distinct Intervals", str(len(timeline)), "Unique date / step bins", "⏱️", "blue")
                with tm_col3:
                    render_metric_card("Peak Interval", str(t_peak_val), f"{t_peak_cnt} evidence records", "📈", "green")

                st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

                # Line chart
                fig_time = px.line(
                    timeline,
                    x=selected_time,
                    y="Record Count",
                    markers=True,
                    title="Chronological Evidence Frequency",
                    color_discrete_sequence=["#0F766E"]
                )
                fig_time.update_traces(
                    line=dict(width=3),
                    marker=dict(size=8, color="#0F766E", line=dict(width=2, color="#FFFFFF"))
                )
                st.plotly_chart(apply_forensic_theme(fig_time), use_container_width=True)

                # Supporting Data Table
                st.markdown("#### Chronological Distribution Table")
                st.dataframe(
                    timeline,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.warning("No valid timestamps or non-null values found in the selected attribute.")

            st.markdown("</div>", unsafe_allow_html=True)
        else:
            render_empty_state(
                icon="📅",
                title="No Temporal Attributes Detected",
                message="No date, time, timestamp, or day-related columns were automatically identified in this evidence dataset."
            )


# -----------------------------------------------------
# PAGE 6: INVESTIGATION INSIGHTS
# -----------------------------------------------------
elif page == "Investigation Insights":
    render_header(
        title="Investigation Insights & Anomaly Intelligence",
        subtitle="Automated statistical debriefs and unsupervised multivariate anomaly detection.",
        badge="ANOMALY INTELLIGENCE"
    )

    if df is None:
        render_empty_state(
            icon="💡",
            title="Evidence Dataset Required",
            message="Upload an evidence dataset via the sidebar to generate automated statistical observations and run machine learning anomaly detection."
        )
    else:
        # Automated Observations Section
        st.markdown("""
        <div class="forensic-card">
            <div class="forensic-card-header">
                <div>
                    <h3 class="forensic-card-title"><span>💡</span> Automated Forensic Observations</h3>
                    <p class="forensic-card-desc">Machine-generated analytical findings derived from dataset distributions.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if insights:
            for idx, insight in enumerate(insights, start=1):
                st.markdown(f"""
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-left: 3px solid #0F766E; border-radius: 8px; padding: 12px 16px; margin-bottom: 8px; font-size: 0.88rem; color: #172033;">
                    <strong style="color: #0F766E; margin-right: 6px;">[OBS-{idx:02d}]</strong> {insight}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No automated observations available.")

        st.markdown("</div>", unsafe_allow_html=True)

        # Anomaly Detection Section
        st.markdown("""
        <div class="forensic-card">
            <div class="forensic-card-header">
                <div>
                    <h3 class="forensic-card-title"><span>🚨</span> Multivariate Anomaly Detection</h3>
                    <p class="forensic-card-desc">Isolation Forest algorithm flagging multivariate deviations for investigator review.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if anomaly_results is not None:
            flagged = anomaly_results[anomaly_results["Anomaly Status"] == "Flagged for Review"]
            flagged_cnt = len(flagged)
            total_cnt = len(df)
            flag_rate = (flagged_cnt / total_cnt * 100) if total_cnt > 0 else 0.0

            an_c1, an_c2, an_c3 = st.columns(3)
            with an_c1:
                render_metric_card("Flagged Records", str(flagged_cnt), f"{flag_rate:.1f}% of evidence dataset", "🚨", "red" if flagged_cnt > 0 else "teal")
            with an_c2:
                render_metric_card("Total Evaluated", f"{total_cnt:,}", "Evidence entries scanned", "📋", "teal")
            with an_c3:
                render_metric_card("Sensitivity Rate", f"{int(contamination * 100)}%", "Configured contamination", "⚙️", "blue")

            # Forensic distinction alert
            st.markdown("""
            <div style="background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 8px; padding: 14px 18px; margin: 18px 0; font-size: 0.82rem; color: #92400E; line-height: 1.5;">
                <strong>FORENSIC INTEGRITY NOTICE:</strong> The records below are identified via statistical multivariate deviations from normative distributions. They represent mathematical outliers flagged for investigative triage and prioritization — they do not by themselves constitute evidence of culpability, tampering, or confirmed illicit activity.
            </div>
            """, unsafe_allow_html=True)

            if not flagged.empty:
                st.markdown("#### Flagged Records for Review")
                st.dataframe(
                    flagged,
                    use_container_width=True,
                    hide_index=True
                )

                st.download_button(
                    label="Download Flagged Records (CSV)",
                    data=flagged.to_csv(index=False).encode("utf-8"),
                    file_name="FORENSIQ_Flagged_Anomalies.csv",
                    mime="text/csv",
                    key="dl_flagged_csv"
                )
            else:
                st.success("No anomalous records detected under the current sensitivity configuration.")
        else:
            st.warning(anomaly_error or "Anomaly detection could not be executed on the current dataset.")

        st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------
# PAGE 7: ASK YOUR DATASET
# -----------------------------------------------------
elif page == "Ask Your Dataset":
    render_header(
        title="Ask Your Dataset",
        subtitle="Natural language rule-based query engine for conversational evidence interrogation.",
        badge="INVESTIGATION ASSISTANT"
    )

    if df is None:
        render_empty_state(
            icon="💬",
            title="Evidence Dataset Required",
            message="Upload an evidence dataset via the sidebar to interrogate evidence records using ordinary English questions."
        )
    else:
        st.markdown("""
        <div class="forensic-card">
            <div class="forensic-card-header">
                <div>
                    <h3 class="forensic-card-title"><span>🔎</span> Evidence Query Interface</h3>
                    <p class="forensic-card-desc">Type an investigation query or click one of the suggested forensic questions below.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Suggested Questions
        st.markdown("<span style='font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase;'>Suggested Investigation Questions:</span>", unsafe_allow_html=True)
        
        sample_queries = [
            "How many total records are there?",
            "Which location has the most evidence records?",
            "What is the average Quality_Score?",
            "Show records with the lowest Quality_Score.",
            "How many anomalies were flagged?",
            "Are there any missing values?",
            "How many duplicate records exist?"
        ]

        q_cols = st.columns(len(sample_queries))
        clicked_query = None
        for i, sq in enumerate(sample_queries):
            short_label = sq.replace("How many ", "").replace("Which ", "").replace("Are there any ", "").replace("?", "")
            if len(short_label) > 22:
                short_label = short_label[:20] + "..."
            if q_cols[i].button(short_label, key=f"sq_btn_{i}", help=sq, use_container_width=True):
                clicked_query = sq

        if clicked_query:
            st.session_state.query_input = clicked_query
            st.session_state["active_query_text"] = clicked_query
            eval_df = anomaly_results if anomaly_results is not None else df
            st.session_state.last_answered_query = clicked_query
            st.session_state.last_query_response = answer_question(eval_df, clicked_query)

        # Input box
        query_text = st.text_input(
            "Investigation Question",
            placeholder="e.g. Which location has the most evidence records? or What is the average Quality_Score?",
            key="active_query_text"
        )

        btn_c1, btn_c2 = st.columns([1, 4])
        with btn_c1:
            run_query = st.button("Analyse Question", use_container_width=True)

        if run_query and query_text.strip():
            st.session_state.last_answered_query = query_text.strip()
            eval_df = anomaly_results if anomaly_results is not None else df
            st.session_state.last_query_response = answer_question(eval_df, query_text.strip())

        # Response Presentation
        if st.session_state.last_query_response is not None:
            ans, chart, *extra = st.session_state.last_query_response

            st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style="background: #E6F4F1; border: 1px solid #A7F3D0; border-radius: 10px; padding: 16px 20px;">
                <div style="font-size: 0.72rem; font-weight: 700; color: #0F766E; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px;">
                    QUERY: "{st.session_state.last_answered_query}"
                </div>
                <div style="font-size: 1.05rem; font-weight: 600; color: #172033; line-height: 1.5;">
                    {ans}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if chart is not None:
                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
                st.plotly_chart(apply_forensic_theme(chart), use_container_width=True)

            if extra and extra[0] is not None:
                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
                st.markdown("#### Matched Evidence Records")
                st.dataframe(
                    extra[0],
                    use_container_width=True,
                    hide_index=True
                )

        st.markdown("""
        <p style="font-size: 0.75rem; color: #94A3B8; margin-top: 18px; margin-bottom: 0;">
            FORENSIQ uses a deterministic rule-based query parser to extract statistical evidence without generative hallucinations.
        </p>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------
# PAGE 8: GENERATE REPORT
# -----------------------------------------------------
elif page == "Generate Report":
    render_header(
        title="Investigation Analysis Report",
        subtitle="Compile formal forensic analysis dossier and export publication-ready PDF.",
        badge="REPORT COMPILATION"
    )

    if df is None:
        render_empty_state(
            icon="📑",
            title="Evidence Dataset Required",
            message="Upload an evidence dataset via the sidebar to generate a formal investigation PDF analysis dossier."
        )
    else:
        st.markdown("""
        <div class="forensic-card">
            <div class="forensic-card-header">
                <div>
                    <h3 class="forensic-card-title"><span>📄</span> Forensic Dossier Summary Preview</h3>
                    <p class="forensic-card-desc">The metrics and automated findings below will be synthesized into the PDF report.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        rep_c1, rep_c2, rep_c3, rep_c4 = st.columns(4)
        with rep_c1:
            st.metric("Total Records", f"{profile['total_rows']:,}")
        with rep_c2:
            st.metric("Total Columns", profile['total_columns'])
        with rep_c3:
            st.metric("Missing Cells", profile['missing_cells'])
        with rep_c4:
            st.metric("Duplicate Rows", profile['duplicate_rows'])

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        st.markdown("#### Included Observations")
        for idx, insight in enumerate(insights, start=1):
            st.markdown(f"&bull; **[OBS-{idx:02d}]** {insight}")

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        gen_c1, gen_c2 = st.columns([1, 2])
        with gen_c1:
            if st.button("Generate PDF Report", use_container_width=True, key="gen_pdf_btn"):
                try:
                    pdf_buffer = generate_pdf_report(profile, insights)
                    st.session_state.generated_pdf_buffer = pdf_buffer
                    st.success("PDF dossier successfully compiled.")
                except Exception as ex:
                    st.error(f"Report compilation failed: {ex}")

        if st.session_state.generated_pdf_buffer is not None:
            st.download_button(
                label="Download Investigation Report (PDF)",
                data=st.session_state.generated_pdf_buffer,
                file_name="FORENSIQ_Investigation_Report.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="dl_compiled_pdf"
            )

        st.markdown("</div>", unsafe_allow_html=True)


# =====================================================
# 7. GLOBAL FOOTER
# =====================================================

st.markdown("""
<div style="margin-top: 40px; padding-top: 16px; border-top: 1px solid #E2E8F0; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
    <div style="font-size: 0.76rem; color: #64748B;">
        <strong style="color: #172033;">FORENSIQ</strong> &bull; Investigation Data Intelligence Platform
    </div>
    <div style="font-size: 0.72rem; color: #94A3B8;">
        Exploratory analytics only. Outputs require independent forensic verification.
    </div>
</div>
""", unsafe_allow_html=True)
