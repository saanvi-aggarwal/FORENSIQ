import streamlit as st
import plotly.graph_objects as go


def get_custom_css():
    """Return the FORENSIQ light-theme CSS stylesheet (original structure, light palette)."""
    return """
<style>
/* ========================================================
   FORENSIQ DESIGN SYSTEM — LIGHT THEME
   Palette:
   - Main Background:    #F5F7FA
   - Sidebar:            #FFFFFF
   - Cards:              #FFFFFF
   - Border:             #E2E8F0
   - Primary Accent:     #0F766E (Teal)
   - Secondary Accent:   #2563EB (Blue)
   - Primary Text:       #172033
   - Secondary Text:     #64748B
   - Muted Text:         #94A3B8
   - Success:            #15803D
   - Warning:            #B45309
   - Error:              #B91C1C
======================================================== */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* --- Root Variables --- */
:root {
    --bg-main:        #F5F7FA;
    --bg-sidebar:     #FFFFFF;
    --bg-card:        #FFFFFF;
    --border-color:   #E2E8F0;
    --border-accent:  rgba(15, 118, 110, 0.25);
    --accent-teal:    #0F766E;
    --accent-blue:    #2563EB;
    --text-primary:   #172033;
    --text-secondary: #64748B;
    --text-muted:     #94A3B8;
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: var(--text-primary);
}

.stApp {
    background-color: var(--bg-main) !important;
    color: var(--text-primary) !important;
}

/* --- Container Spacing & Layout --- */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 1380px !important;
}

/* --- Typography --- */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', sans-serif !important;
    letter-spacing: -0.01em;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
}

h1 {
    font-size: 1.9rem !important;
    font-weight: 800 !important;
    margin-bottom: 0.25rem !important;
}

h2 {
    font-size: 1.4rem !important;
    margin-top: 1rem !important;
    margin-bottom: 0.5rem !important;
}

h3 {
    font-size: 1.15rem !important;
    color: var(--text-primary) !important;
}

p, span, label, div {
    color: var(--text-primary);
}

/* --- Sidebar Styling --- */
[data-testid="stSidebar"] {
    background-color: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border-color) !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: var(--text-primary) !important;
}

/* Sidebar Brand Header */
.sidebar-brand-container {
    padding: 12px 6px 16px 6px;
    border-bottom: 1px solid var(--border-color);
    margin-bottom: 16px;
}

.brand-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--accent-teal);
    background: rgba(15, 118, 110, 0.08);
    border: 1px solid rgba(15, 118, 110, 0.2);
    padding: 3px 8px;
    border-radius: 9999px;
    margin-bottom: 8px;
}

.brand-title {
    font-size: 1.45rem;
    font-weight: 800;
    letter-spacing: 0.05em;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 0;
}

.brand-subtitle {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--text-secondary);
    margin-top: 2px;
}

/* Sidebar Navigation (Radio restyled) */
[data-testid="stSidebar"] [data-testid="stRadio"] > div {
    gap: 4px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background-color: transparent !important;
    border: 1px solid transparent !important;
    padding: 8px 12px !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
    display: flex !important;
    align-items: center !important;
    margin-bottom: 2px !important;
    color: var(--text-secondary) !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background-color: rgba(15, 118, 110, 0.06) !important;
    border-color: rgba(15, 118, 110, 0.15) !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"],
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: rgba(15, 118, 110, 0.08) !important;
    border-left: 3px solid var(--accent-teal) !important;
    border-top: 1px solid rgba(15, 118, 110, 0.2) !important;
    border-right: 1px solid rgba(15, 118, 110, 0.2) !important;
    border-bottom: 1px solid rgba(15, 118, 110, 0.2) !important;
    color: var(--accent-teal) !important;
    font-weight: 600 !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] input[type="radio"] {
    accent-color: var(--accent-teal);
}

/* Evidence section in sidebar */
.sidebar-evidence-card {
    background: #F8FAFC;
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 12px;
    margin-top: 8px;
    margin-bottom: 12px;
}

.sidebar-status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 3px 8px;
    border-radius: 6px;
    margin-bottom: 6px;
}

.status-active {
    background: #DCFCE7;
    color: #15803D;
    border: 1px solid #BBF7D0;
}

.status-empty {
    background: #FEF9C3;
    color: #B45309;
    border: 1px solid #FDE68A;
}

/* --- Metric Cards --- */
[data-testid="stMetric"] {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    padding: 18px 20px !important;
    border-radius: 12px !important;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06) !important;
    transition: all 0.2s ease !important;
}

[data-testid="stMetric"]:hover {
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.1) !important;
}

[data-testid="stMetricLabel"] {
    color: var(--text-secondary) !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

[data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-size: 1.85rem !important;
    font-weight: 700 !important;
}

/* Custom HTML Metric Card */
.forensic-metric-card {
    background-color: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 18px 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 110px;
    position: relative;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
    transition: all 0.2s ease;
    overflow: hidden;
}

.forensic-metric-card:hover {
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.1);
}

.f-metric-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
}

.f-metric-label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-secondary);
}

.f-metric-icon {
    font-size: 1.05rem;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    background: rgba(15, 118, 110, 0.08);
    border: 1px solid rgba(15, 118, 110, 0.15);
}

.f-metric-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.1;
    margin-bottom: 4px;
}

.f-metric-subtext {
    font-size: 0.72rem;
    color: var(--text-muted);
}

/* --- Section Cards & Containers --- */
.forensic-card {
    background-color: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 22px;
    margin-bottom: 20px;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
}

.forensic-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 12px;
    margin-bottom: 16px;
}

.forensic-card-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 0;
}

.forensic-card-desc {
    font-size: 0.8rem;
    color: var(--text-secondary);
    margin-top: 4px;
    margin-bottom: 0;
}

/* --- Buttons --- */
.stButton > button {
    background-color: var(--accent-teal) !important;
    color: #FFFFFF !important;
    border: 1px solid var(--accent-teal) !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.2rem !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.01em !important;
    box-shadow: 0 1px 3px rgba(15, 118, 110, 0.2) !important;
    transition: all 0.15s ease !important;
}

.stButton > button:hover {
    background-color: #115E59 !important;
    box-shadow: 0 4px 12px rgba(15, 118, 110, 0.3) !important;
    transform: translateY(-1px);
}

.stButton > button:active {
    transform: translateY(0);
}

/* Download buttons */
.stDownloadButton > button {
    background: #F8FAFC !important;
    color: var(--accent-teal) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.2rem !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    transition: all 0.15s ease !important;
}

.stDownloadButton > button:hover {
    background: rgba(15, 118, 110, 0.06) !important;
    border-color: var(--accent-teal) !important;
    box-shadow: 0 2px 8px rgba(15, 118, 110, 0.15) !important;
    transform: translateY(-1px);
}

/* --- Form Inputs, TextAreas, Selectboxes --- */
div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div,
div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}

div[data-baseweb="input"]:focus-within > div,
div[data-baseweb="textarea"]:focus-within > div,
div[data-baseweb="select"]:focus-within > div {
    border-color: var(--accent-teal) !important;
    box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.12) !important;
}

input, textarea {
    color: var(--text-primary) !important;
}

/* --- Dataframes & Tables --- */
[data-testid="stDataFrame"] {
    background-color: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    overflow: hidden;
}

/* --- Expanders --- */
[data-testid="stExpander"] {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 10px !important;
    margin-bottom: 12px !important;
}

[data-testid="stExpander"] details summary {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

[data-testid="stExpander"] details summary:hover {
    color: var(--accent-teal) !important;
}

/* --- Alert Boxes --- */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    border-width: 1px !important;
}

/* --- Sliders --- */
[data-testid="stSlider"] div[role="slider"] {
    background-color: var(--accent-teal) !important;
    border-color: var(--accent-teal) !important;
}

/* --- File Uploader --- */
[data-testid="stFileUploader"] section {
    background-color: #F8FAFC !important;
    border: 1px dashed var(--border-color) !important;
    border-radius: 10px !important;
    padding: 18px !important;
}

[data-testid="stFileUploader"] section:hover {
    border-color: var(--accent-teal) !important;
    background-color: rgba(15, 118, 110, 0.04) !important;
}

/* --- Badges & Indicators --- */
.forensic-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 6px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.badge-open {
    background: #DCFCE7;
    color: #15803D;
    border: 1px solid #BBF7D0;
}

.badge-review {
    background: #FEF9C3;
    color: #B45309;
    border: 1px solid #FDE68A;
}

.badge-closed {
    background: #F1F5F9;
    color: #64748B;
    border: 1px solid #E2E8F0;
}

.badge-flagged {
    background: #FEF2F2;
    color: #B91C1C;
    border: 1px solid #FECACA;
}

.badge-info {
    background: rgba(15, 118, 110, 0.08);
    color: var(--accent-teal);
    border: 1px solid rgba(15, 118, 110, 0.2);
}

.badge-cyan {
    background: rgba(37, 99, 235, 0.08);
    color: var(--accent-blue);
    border: 1px solid rgba(37, 99, 235, 0.2);
}

/* Empty State Card */
.empty-state-box {
    background: #FFFFFF;
    border: 1.5px dashed var(--border-color);
    border-radius: 14px;
    padding: 38px 24px;
    text-align: center;
    margin: 20px 0;
}

.empty-state-icon {
    font-size: 2.5rem;
    margin-bottom: 12px;
    display: inline-block;
    opacity: 0.6;
}

.empty-state-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 8px;
}

.empty-state-text {
    font-size: 0.88rem;
    color: var(--text-secondary);
    max-width: 520px;
    margin: 0 auto 16px auto;
    line-height: 1.6;
}

/* Monospace Pill */
.mono-pill {
    font-family: 'SFMono-Regular', Consolas, monospace;
    font-size: 0.78rem;
    background: #F1F5F9;
    border: 1px solid var(--border-color);
    padding: 2px 7px;
    border-radius: 5px;
    color: var(--accent-teal);
}

/* Dividers */
hr {
    border-color: var(--border-color) !important;
    margin: 1.5rem 0 !important;
}

/* Header Banner */
.forensic-header {
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 16px;
    margin-bottom: 24px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    flex-wrap: wrap;
    gap: 12px;
}

.forensic-header-left {
    flex: 1;
}

.forensic-header-right {
    display: flex;
    align-items: center;
    gap: 10px;
}

/* Custom Scrollbars */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #F8FAFC; }
::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-teal); }

/* Hide Streamlit default footer / menu, but keep sidebar collapse/expand trigger fully visible and functional */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

/* Ensure Streamlit top header is transparent and allows the sidebar collapse/expand toggle button to be clicked */
header[data-testid="stHeader"] {
    background: transparent !important;
    color: var(--text-primary) !important;
}

/* Style the collapse and expand sidebar chevron buttons for clean visibility */
button[data-testid="stSidebarCollapseButton"],
button[data-testid="stSidebarHeaderCollapseButton"],
button[data-testid="stSidebarExpandButton"],
[data-testid="collapsedControl"] {
    color: var(--accent-teal) !important;
    background-color: #FFFFFF !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.08) !important;
    transition: all 0.2s ease !important;
    visibility: visible !important;
    display: inline-flex !important;
}

button[data-testid="stSidebarCollapseButton"]:hover,
button[data-testid="stSidebarHeaderCollapseButton"]:hover,
button[data-testid="stSidebarExpandButton"]:hover,
[data-testid="collapsedControl"]:hover {
    background-color: rgba(15, 118, 110, 0.08) !important;
    border-color: var(--accent-teal) !important;
    color: #115E59 !important;
}

[data-testid="collapsedControl"] button {
    color: var(--accent-teal) !important;
}
</style>
"""


def apply_forensic_theme(fig):
    """Apply the FORENSIQ light theme to a Plotly figure."""
    if fig is None:
        return None

    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(
            family="Inter, -apple-system, sans-serif",
            size=12,
            color="#172033"
        ),
        title=dict(
            font=dict(
                family="Inter, sans-serif",
                size=14,
                color="#172033"
            ),
            x=0.02,
            y=0.98,
            xanchor="left",
            yanchor="top"
        ),
        margin=dict(l=50, r=30, t=75, b=45),
        xaxis=dict(
            gridcolor="#F1F5F9",
            zerolinecolor="#E2E8F0",
            tickfont=dict(color="#64748B", size=10),
            title_font=dict(color="#64748B", size=11)
        ),
        yaxis=dict(
            gridcolor="#F1F5F9",
            zerolinecolor="#E2E8F0",
            tickfont=dict(color="#64748B", size=10),
            title_font=dict(color="#64748B", size=11)
        ),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor="#E2E8F0",
            font=dict(
                family="Inter, sans-serif",
                size=12,
                color="#172033"
            )
        )
    )

    return fig


def render_header(title, subtitle=None, badge=None):
    """Render a consistent forensic intelligence page header."""
    badge_html = f'<div class="brand-badge">{badge}</div>' if badge else ""
    subtitle_html = f'<div class="forensic-card-desc" style="font-size: 0.9rem; margin-top: 4px;">{subtitle}</div>' if subtitle else ""

    st.markdown(f"""
    <div class="forensic-header">
        <div class="forensic-header-left">
            {badge_html}
            <h1 style="margin: 0; padding: 0;">{title}</h1>
            {subtitle_html}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(label, value, subtext="", icon="📊", border_accent="teal"):
    """Render an HTML forensic metric card with light theme styling."""
    accent_map = {
        "teal":  ("#0F766E", "rgba(15, 118, 110, 0.08)",  "rgba(15, 118, 110, 0.2)"),
        "blue":  ("#2563EB", "rgba(37, 99, 235, 0.08)",   "rgba(37, 99, 235, 0.2)"),
        "green": ("#15803D", "rgba(21, 128, 61, 0.08)",   "rgba(21, 128, 61, 0.2)"),
        "amber": ("#B45309", "rgba(180, 83, 9, 0.08)",    "rgba(180, 83, 9, 0.2)"),
        "red":   ("#B91C1C", "rgba(185, 28, 28, 0.08)",   "rgba(185, 28, 28, 0.2)"),
        "slate": ("#475569", "rgba(71, 85, 105, 0.08)",   "rgba(71, 85, 105, 0.2)"),
        "cyan":  ("#0E7490", "rgba(14, 116, 144, 0.08)",  "rgba(14, 116, 144, 0.2)"),
    }
    color, bg, border = accent_map.get(border_accent, accent_map["teal"])

    st.markdown(f"""
    <div class="forensic-metric-card" style="border-top: 3px solid {color};">
        <div class="f-metric-top">
            <span class="f-metric-label">{label}</span>
            <span class="f-metric-icon" style="background: {bg}; border-color: {border};">{icon}</span>
        </div>
        <div class="f-metric-value">{value}</div>
        <div class="f-metric-subtext">{subtext}</div>
    </div>
    """, unsafe_allow_html=True)


def render_empty_state(icon="🔍", title="No Evidence Dataset Loaded",
                       message="Upload an evidence dataset (.csv, .xlsx, or .json) via the sidebar to initialize forensic analysis."):
    """Render a styled empty state container."""
    st.markdown(f"""
    <div class="empty-state-box">
        <div class="empty-state-icon">{icon}</div>
        <div class="empty-state-title">{title}</div>
        <div class="empty-state-text">{message}</div>
    </div>
    """, unsafe_allow_html=True)


def get_status_badge_html(status):
    """Return HTML for case status badges."""
    status_lower = str(status).lower()
    if "open" in status_lower:
        return '<span class="forensic-badge badge-open">● OPEN</span>'
    elif "review" in status_lower:
        return '<span class="forensic-badge badge-review">▲ UNDER REVIEW</span>'
    elif "closed" in status_lower:
        return '<span class="forensic-badge badge-closed">■ CLOSED</span>'
    return f'<span class="forensic-badge badge-info">{status}</span>'
