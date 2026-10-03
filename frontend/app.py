import streamlit as st
import subprocess
import tempfile
import os
import re
from pathlib import Path
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

SEQUENTIAL = ROOT / "sequential"
PARALLEL = ROOT / "parallel"

BENCHMARK_THREADS = [1, 2, 4, 8]


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CorpusLens · Text Analytics Engine",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# GLOBAL STYLING
# ============================================================

def inject_theme():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

        :root {
            --obsidian-0:  #0a0a0c;
            --obsidian-1:  #0f1013;
            --obsidian-2:  #14161a;
            --obsidian-3:  #1c1f25;
            --hairline:    rgba(255,255,255,0.06);
            --hairline-2:  rgba(255,255,255,0.10);
            --ink-100:     #f4f2ee;
            --ink-200:     #c9c6c0;
            --ink-300:     #8a8880;
            --ink-400:     #5c5b57;
            --amber:       #e8a24a;
            --amber-soft:  #f0b96a;
            --copper:      #c9764a;
        }

        /* ---------- base ---------- */
        html, body, [class*="css"], .stApp {
            background: var(--obsidian-0) !important;
            color: var(--ink-100);
            font-family: 'Inter', -apple-system, sans-serif;
        }

        .stApp {
            background:
                radial-gradient(1200px 600px at 85% -10%, rgba(232,162,74,0.06), transparent 60%),
                radial-gradient(900px 500px at -10% 30%, rgba(201,118,74,0.05), transparent 55%),
                var(--obsidian-0) !important;
        }

        /* DO NOT TOUCH header[data-testid="stHeader"] — Streamlit's
           sidebar toggle lives inside it. Leave it fully intact. */

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1400px;
        }

        /* ---------- typography ---------- */
        h1, h2, h3, h4 {
            font-family: 'Fraunces', Georgia, serif;
            color: var(--ink-100) !important;
            letter-spacing: -0.02em;
            font-weight: 600;
        }
        h1 { font-size: 2.6rem !important; line-height: 1.05; }
        h2 { font-size: 1.55rem !important; }
        h3 { font-size: 1.15rem !important; }

        p, span, label, div { color: var(--ink-200); }

        code, pre, .stCode, [data-testid="stCode"] {
            font-family: 'JetBrains Mono', ui-monospace, monospace !important;
        }

        a { color: var(--amber-soft) !important; text-decoration: none; }

        /* ---------- sidebar ---------- */
        section[data-testid="stSidebar"] {
            background: var(--obsidian-1) !important;
            border-right: 1px solid var(--hairline);
        }
        section[data-testid="stSidebar"] > div { padding-top: 1.2rem; }
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            letter-spacing: 0.02em;
        }
        section[data-testid="stSidebar"] .stMarkdown p {
            color: var(--ink-300);
            font-size: 0.82rem;
        }

        /* sidebar radio as segmented control */
        section[data-testid="stSidebar"] div[role="radiogroup"] {
            display: flex;
            gap: 6px;
            background: var(--obsidian-2);
            padding: 4px;
            border-radius: 10px;
            border: 1px solid var(--hairline);
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label {
            flex: 1;
            justify-content: center;
            padding: 7px 10px;
            border-radius: 7px;
            cursor: pointer;
            transition: all 0.2s ease;
            background: transparent;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
            background: rgba(232,162,74,0.08);
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"],
        section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
            background: linear-gradient(180deg, rgba(232,162,74,0.20), rgba(232,162,74,0.08));
            border: 1px solid rgba(232,162,74,0.35);
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label p {
            color: var(--ink-100) !important;
            font-weight: 500;
            font-size: 0.85rem;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {
            display: none;
        }

        /* ---------- buttons ---------- */
        .stButton > button {
            background: var(--obsidian-3);
            color: var(--ink-100);
            border: 1px solid var(--hairline-2);
            border-radius: 10px;
            padding: 0.55rem 1rem;
            font-weight: 500;
            font-family: 'Inter', sans-serif;
            transition: all 0.2s ease;
        }
        .stButton > button:hover {
            border-color: rgba(232,162,74,0.5);
            background: var(--obsidian-2);
            color: var(--amber-soft);
            transform: translateY(-1px);
        }
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, var(--amber) 0%, var(--copper) 100%);
            color: #1a1206;
            border: none;
            font-weight: 600;
            box-shadow: 0 6px 18px -8px rgba(232,162,74,0.55);
        }
        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, var(--amber-soft) 0%, var(--amber) 100%);
            color: #1a1206;
            transform: translateY(-1px);
            box-shadow: 0 10px 24px -8px rgba(232,162,74,0.7);
        }

        .stDownloadButton > button {
            background: var(--obsidian-3);
            color: var(--ink-100);
            border: 1px solid var(--hairline-2);
            border-radius: 10px;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        .stDownloadButton > button:hover {
            border-color: rgba(232,162,74,0.5);
            color: var(--amber-soft);
        }

        /* ---------- inputs ---------- */
        .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb],
        div[data-baseweb="input"], div[data-baseweb="select"] > div {
            background: var(--obsidian-2) !important;
            border: 1px solid var(--hairline-2) !important;
            border-radius: 10px !important;
            color: var(--ink-100) !important;
        }

        /* file uploader */
        section[data-testid="stFileUploaderDropzone"],
        section[data-testid="stFileUploaderDropzone"] > div {
            background: var(--obsidian-2) !important;
            border: 1.5px dashed rgba(232,162,74,0.25) !important;
            border-radius: 12px !important;
            transition: all 0.2s ease;
        }
        section[data-testid="stFileUploaderDropzone"]:hover {
            border-color: rgba(232,162,74,0.55) !important;
            background: var(--obsidian-3) !important;
        }
        section[data-testid="stFileUploaderDropzone"] button {
            background: linear-gradient(135deg, var(--amber) 0%, var(--copper) 100%) !important;
            color: #1a1206 !important;
            border: none !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
        }
        section[data-testid="stFileUploaderDropzone"] small,
        section[data-testid="stFileUploaderDropzone"] span {
            color: var(--ink-300) !important;
        }

        /* slider */
        div[data-baseweb="slider"] div[role="slider"] {
            background: var(--amber) !important;
            border: 3px solid var(--obsidian-0) !important;
            box-shadow: 0 0 0 1px var(--amber);
        }
        div[data-baseweb="slider"] > div > div > div {
            background: linear-gradient(90deg, var(--amber), var(--copper)) !important;
        }

        /* ---------- metric cards ---------- */
        div[data-testid="stMetric"] {
            background: linear-gradient(160deg, var(--obsidian-2) 0%, var(--obsidian-1) 100%);
            border: 1px solid var(--hairline);
            border-radius: 14px;
            padding: 18px 20px 16px;
            position: relative;
            overflow: hidden;
            transition: all 0.25s ease;
        }
        div[data-testid="stMetric"]::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, var(--amber), var(--copper), transparent);
            opacity: 0.7;
        }
        div[data-testid="stMetric"]:hover {
            border-color: var(--hairline-2);
            transform: translateY(-2px);
            box-shadow: 0 14px 30px -18px rgba(0,0,0,0.8);
        }
        div[data-testid="stMetric"] label {
            color: var(--ink-300) !important;
            font-size: 0.72rem !important;
            text-transform: uppercase;
            letter-spacing: 0.10em;
            font-weight: 500;
        }
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            color: var(--ink-100) !important;
            font-family: 'JetBrains Mono', monospace !important;
            font-weight: 600;
            font-size: 1.5rem !important;
            letter-spacing: -0.02em;
        }

        /* ---------- tabs ---------- */
        div[data-baseweb="tab-list"] {
            gap: 6px;
            background: var(--obsidian-1);
            border: 1px solid var(--hairline);
            border-radius: 12px;
            padding: 6px;
            margin-bottom: 1.4rem;
        }
        button[data-baseweb="tab"] {
            background: transparent !important;
            color: var(--ink-300) !important;
            border-radius: 8px !important;
            padding: 9px 18px !important;
            font-weight: 500 !important;
            font-family: 'Inter', sans-serif !important;
            transition: all 0.2s ease;
        }
        button[data-baseweb="tab"]:hover {
            color: var(--ink-100) !important;
            background: rgba(232,162,74,0.06) !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            background: linear-gradient(180deg, rgba(232,162,74,0.18), rgba(232,162,74,0.06)) !important;
            color: var(--amber-soft) !important;
            border: 1px solid rgba(232,162,74,0.30) !important;
        }
        div[data-baseweb="tab-highlight"] { display: none; }
        div[data-baseweb="tab-border"]    { display: none; }

        /* ---------- dataframe ---------- */
        div[data-testid="stDataFrame"] {
            border: 1px solid var(--hairline);
            border-radius: 12px;
            overflow: hidden;
            background: var(--obsidian-1);
        }
        div[data-testid="stDataFrame"] * {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 0.82rem !important;
        }

        /* ---------- alerts ---------- */
        div[data-testid="stAlert"] {
            background: var(--obsidian-2) !important;
            border: 1px solid var(--hairline-2) !important;
            border-left: 3px solid var(--amber) !important;
            border-radius: 12px !important;
            color: var(--ink-200) !important;
        }
        div[data-testid="stAlert"] svg { fill: var(--amber) !important; }

        /* spinner */
        .stSpinner > div {
            border-top-color: var(--amber) !important;
            border-right-color: var(--amber) !important;
        }

        /* expander */
        details[data-testid="stExpander"] {
            background: var(--obsidian-1);
            border: 1px solid var(--hairline);
            border-radius: 12px;
            overflow: hidden;
        }
        details[data-testid="stExpander"] summary {
            color: var(--ink-200);
            font-weight: 500;
            padding: 12px 16px;
        }
        details[data-testid="stExpander"] summary:hover {
            color: var(--amber-soft);
        }

        /* chart containers */
        div[data-testid="stArrowVegaLiteChart"],
        div[data-testid="stVegaLiteChart"],
        div[data-testid="stLineChart"],
        div[data-testid="stBarChart"] {
            background: var(--obsidian-1);
            border: 1px solid var(--hairline);
            border-radius: 14px;
            padding: 14px;
        }

        /* divider */
        hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--hairline-2), transparent);
            margin: 1.6rem 0;
        }

        /* ---------- custom components ---------- */
        .cl-hero {
            position: relative;
            padding: 34px 38px 30px;
            border-radius: 20px;
            background:
                radial-gradient(600px 200px at 100% 0%, rgba(232,162,74,0.12), transparent 65%),
                radial-gradient(500px 220px at 0% 100%, rgba(201,118,74,0.10), transparent 60%),
                linear-gradient(150deg, var(--obsidian-2) 0%, var(--obsidian-1) 100%);
            border: 1px solid var(--hairline-2);
            margin-bottom: 1.6rem;
            overflow: hidden;
        }
        .cl-hero::after {
            content: "";
            position: absolute;
            inset: 0;
            background-image:
                linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px);
            background-size: 32px 32px;
            pointer-events: none;
            mask-image: radial-gradient(circle at 30% 40%, black, transparent 75%);
        }
        .cl-hero-title {
            font-family: 'Fraunces', serif;
            font-size: 2.55rem;
            font-weight: 600;
            letter-spacing: -0.025em;
            color: var(--ink-100);
            line-height: 1.05;
            margin: 0 0 10px 0;
            display: flex;
            align-items: center;
            gap: 14px;
        }
        .cl-hero-title .mark {
            width: 40px; height: 40px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, var(--amber), var(--copper));
            border-radius: 11px;
            color: #1a1206;
            font-size: 1.25rem;
            font-weight: 700;
            box-shadow: 0 10px 24px -10px rgba(232,162,74,0.6);
        }
        .cl-hero-sub {
            color: var(--ink-300);
            font-size: 0.98rem;
            max-width: 720px;
            line-height: 1.55;
            margin: 0;
        }
        .cl-hero-tag {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 5px 12px;
            border-radius: 100px;
            background: rgba(232,162,74,0.08);
            border: 1px solid rgba(232,162,74,0.25);
            color: var(--amber-soft);
            font-size: 0.72rem;
            font-weight: 500;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 16px;
        }
        .cl-hero-tag .dot {
            width: 6px; height: 6px; border-radius: 50%;
            background: var(--amber);
            box-shadow: 0 0 8px var(--amber);
            animation: cl-pulse 2s ease-in-out infinite;
        }
        @keyframes cl-pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.4; }
        }

        .cl-section-label {
            display: flex;
            align-items: center;
            gap: 12px;
            margin: 4px 0 18px 0;
        }
        .cl-section-label .num {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
            color: var(--amber);
            letter-spacing: 0.12em;
            padding: 3px 8px;
            border: 1px solid rgba(232,162,74,0.3);
            border-radius: 6px;
            background: rgba(232,162,74,0.06);
        }
        .cl-section-label .txt {
            font-family: 'Fraunces', serif;
            font-size: 1.35rem;
            font-weight: 600;
            color: var(--ink-100);
            letter-spacing: -0.02em;
        }
        .cl-section-label .line {
            flex: 1;
            height: 1px;
            background: linear-gradient(90deg, var(--hairline-2), transparent);
        }

        .cl-feature {
            background: linear-gradient(160deg, var(--obsidian-2) 0%, var(--obsidian-1) 100%);
            border: 1px solid var(--hairline);
            border-radius: 16px;
            padding: 24px 22px;
            height: 100%;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        .cl-feature:hover {
            transform: translateY(-3px);
            border-color: rgba(232,162,74,0.25);
            box-shadow: 0 20px 40px -22px rgba(0,0,0,0.9);
        }
        .cl-feature .icon {
            width: 40px; height: 40px;
            border-radius: 11px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(232,162,74,0.10);
            border: 1px solid rgba(232,162,74,0.25);
            color: var(--amber);
            margin-bottom: 16px;
        }
        .cl-feature .icon svg { width: 20px; height: 20px; }
        .cl-feature h4 {
            font-family: 'Fraunces', serif;
            font-size: 1.05rem;
            margin: 0 0 12px 0;
            color: var(--ink-100);
            font-weight: 600;
        }
        .cl-feature ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        .cl-feature li {
            color: var(--ink-300);
            font-size: 0.86rem;
            padding: 6px 0 6px 18px;
            position: relative;
            line-height: 1.5;
        }
        .cl-feature li::before {
            content: "";
            position: absolute;
            left: 0; top: 13px;
            width: 6px; height: 6px;
            border-radius: 50%;
            background: var(--amber);
            opacity: 0.55;
        }

        .cl-stat-strip {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 18px;
        }
        .cl-chip {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 12px;
            border-radius: 8px;
            background: var(--obsidian-2);
            border: 1px solid var(--hairline);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            color: var(--ink-200);
        }
        .cl-chip .k { color: var(--ink-400); }
        .cl-chip .v { color: var(--amber-soft); }

        .cl-footer {
            text-align: center;
            padding: 32px 0 8px;
            color: var(--ink-400);
            font-size: 0.78rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }
        .cl-footer .sep {
            margin: 0 10px;
            color: var(--amber);
            opacity: 0.6;
        }

        .cl-empty-state {
            text-align: center;
            padding: 60px 20px;
            border: 1px dashed var(--hairline-2);
            border-radius: 18px;
            background: linear-gradient(160deg, var(--obsidian-2) 0%, var(--obsidian-1) 100%);
        }
        .cl-empty-state .glyph {
            font-family: 'Fraunces', serif;
            font-size: 3rem;
            color: var(--amber);
            opacity: 0.9;
            margin-bottom: 12px;
        }

        @keyframes cl-fade {
            from { opacity: 0; transform: translateY(6px); }
            to   { opacity: 1; transform: translateY(0); }
        }
        .block-container > div { animation: cl-fade 0.4s ease; }
        </style>
        """,
        unsafe_allow_html=True
    )


inject_theme()


# ============================================================
# SVG ICON LIBRARY
# ============================================================

ICON = {
    "chart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M7 14l3-3 3 3 5-6"/></svg>',
    "list":  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><circle cx="3.5" cy="6" r="1"/><circle cx="3.5" cy="12" r="1"/><circle cx="3.5" cy="18" r="1"/></svg>',
    "bolt":  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
    "doc":   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>',
    "cpu":   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/></svg>',
}


def section_label(number, text):
    st.markdown(
        f"""
        <div class="cl-section-label">
            <span class="num">{number}</span>
            <span class="txt">{text}</span>
            <span class="line"></span>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SESSION STATE
# ============================================================

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "analysis_output" not in st.session_state:
    st.session_state.analysis_output = None

if "analysis_stats" not in st.session_state:
    st.session_state.analysis_stats = {}

if "analysis_top_words" not in st.session_state:
    st.session_state.analysis_top_words = []

if "benchmark_df" not in st.session_state:
    st.session_state.benchmark_df = pd.DataFrame()

if "benchmark_errors" not in st.session_state:
    st.session_state.benchmark_errors = []

if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None

if "uploaded_file_signature" not in st.session_state:
    st.session_state.uploaded_file_signature = None
if "analysis_mode" not in st.session_state:
    st.session_state.analysis_mode = None

if "correctness_done" not in st.session_state:
    st.session_state.correctness_done = False

if "correctness_passed" not in st.session_state:
    st.session_state.correctness_passed = False

if "correctness_details" not in st.session_state:
    st.session_state.correctness_details = []

if "correctness_error" not in st.session_state:
    st.session_state.correctness_error = None
    
# ============================================================
# HELPER FUNCTIONS
# ============================================================

def reset_results():
    st.session_state.analysis_done = False
    st.session_state.analysis_output = None
    st.session_state.analysis_stats = {}
    st.session_state.analysis_top_words = []

    st.session_state.benchmark_df = pd.DataFrame()
    st.session_state.benchmark_errors = []

    st.session_state.correctness_done = False
    st.session_state.correctness_passed = False
    st.session_state.correctness_details = []
    st.session_state.correctness_error = None

    st.session_state.uploaded_filename = None
    st.session_state.analysis_mode = None

def parse_output(output):
    stats = {}
    top_words = []

    patterns = {
        "total_lines": r"Total lines\s*:\s*([\d.]+)",
        "total_paragraphs": r"Total paragraphs\s*:\s*([\d.]+)",
        "total_words": r"Total words\s*:\s*([\d.]+)",
        "unique_words": r"Unique words\s*:\s*([\d.]+)",
        "total_characters": r"Total characters\s*:\s*([\d.]+)",
        "total_sentences": r"Total sentences\s*:\s*([\d.]+)",
        "avg_words_line": r"Average words/line\s*:\s*([\d.]+)",
        "avg_words_sentence": r"Average words/sentence\s*:\s*([\d.]+)",
        "avg_characters_line": r"Average characters/line\s*:\s*([\d.]+)",
        "threads": r"Threads\s*:\s*(\d+)",
        "execution_time": r"Execution time\s*:\s*([\d.]+)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, output)
        if not match:
            continue
        value = match.group(1)
        if key in {"avg_words_line","avg_words_sentence","avg_characters_line","execution_time"}:
            stats[key] = float(value)
        else:
            stats[key] = int(float(value))

    in_top_words = False
    for line in output.splitlines():
        if "TOP FREQUENT WORDS" in line:
            in_top_words = True
            continue
        if in_top_words:
            match = re.match(r"\s*(\d+)\s+(\S+)\s+(\d+)", line)
            if match:
                top_words.append({
                    "Rank": int(match.group(1)),
                    "Word": match.group(2),
                    "Frequency": int(match.group(3))
                })

    return stats, top_words


def run_engine(input_file, mode, threads=4):
    try:
        if mode == "Sequential":
            executable = SEQUENTIAL
            command = [str(SEQUENTIAL), str(input_file)]
        else:
            executable = PARALLEL
            command = [str(PARALLEL), str(input_file), str(threads)]

        if not executable.exists():
            return (
                "ERROR:\n\n"
                f"Executable not found: {executable}\n\n"
                "Please compile the C++ project before running CorpusLens."
            )

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=str(ROOT)
        )

        if result.returncode != 0:
            return (
                "ERROR:\n\n"
                f"Return code: {result.returncode}\n\n"
                "STDERR:\n"
                f"{result.stderr}\n\n"
                "STDOUT:\n"
                f"{result.stdout}"
            )

        return result.stdout

    except Exception as error:
        return f"ERROR: {error}"


def save_uploaded_file(uploaded_file):
    suffix = Path(uploaded_file.name).suffix
    if suffix == "":
        suffix = ".txt"

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp_file.write(uploaded_file.getbuffer())
    temp_file.close()

    return Path(temp_file.name)


def benchmark_uploaded_file(input_file):
    results = []
    errors = []

    sequential_output = run_engine(input_file, "Sequential")

    if sequential_output.startswith("ERROR"):
        errors.append("Sequential benchmark failed:\n" + sequential_output)
    else:
        sequential_stats, _ = parse_output(sequential_output)
        sequential_time = sequential_stats.get("execution_time")
        if sequential_time is not None:
            results.append({
                "Mode": "Sequential",
                "Threads": 1,
                "Execution Time": sequential_time
            })
        else:
            errors.append(
                "Sequential benchmark completed, "
                "but execution time could not be parsed."
            )

    for thread_count in BENCHMARK_THREADS:
        parallel_output = run_engine(input_file, "Parallel", thread_count)

        if parallel_output.startswith("ERROR"):
            errors.append(
                f"Parallel benchmark failed for {thread_count} thread(s):\n"
                f"{parallel_output}"
            )
            continue

        parallel_stats, _ = parse_output(parallel_output)
        parallel_time = parallel_stats.get("execution_time")

        if parallel_time is not None:
            results.append({
                "Mode": "Parallel",
                "Threads": thread_count,
                "Execution Time": parallel_time
            })
        else:
            errors.append(
                f"Parallel benchmark completed for {thread_count} thread(s), "
                "but execution time could not be parsed."
            )

    return pd.DataFrame(results), errors

def verify_correctness(input_file, thread_count):
    """
    Compare sequential and parallel results for the same input corpus.

    Execution time and thread count are intentionally NOT compared.
    We compare corpus statistics and Top-K frequencies.
    """

    sequential_output = run_engine(
        input_file,
        "Sequential"
    )

    if sequential_output.startswith("ERROR"):
        return {
            "passed": False,
            "details": [],
            "error": (
                "Sequential execution failed:\n"
                + sequential_output
            )
        }

    parallel_output = run_engine(
        input_file,
        "Parallel",
        thread_count
    )

    if parallel_output.startswith("ERROR"):
        return {
            "passed": False,
            "details": [],
            "error": (
                "Parallel execution failed:\n"
                + parallel_output
            )
        }

    sequential_stats, sequential_top = parse_output(
        sequential_output
    )

    parallel_stats, parallel_top = parse_output(
        parallel_output
    )

    details = []

    statistics_to_compare = [
        ("Total lines", "total_lines"),
        ("Total paragraphs", "total_paragraphs"),
        ("Total words", "total_words"),
        ("Unique words", "unique_words"),
        ("Total characters", "total_characters"),
        ("Total sentences", "total_sentences"),
        ("Average words/line", "avg_words_line"),
        ("Average words/sentence", "avg_words_sentence"),
        ("Average characters/line", "avg_characters_line"),
    ]

    all_passed = True

    for label, key in statistics_to_compare:

        seq_value = sequential_stats.get(key)
        par_value = parallel_stats.get(key)

        passed = seq_value == par_value

        if not passed:
            all_passed = False

        details.append({
            "Check": label,
            "Sequential": seq_value,
            "Parallel": par_value,
            "Status": "PASS" if passed else "FAIL"
        })

    # Compare Top-K
    seq_top_normalized = [
        (
            item["Rank"],
            item["Word"],
            item["Frequency"]
        )
        for item in sequential_top
    ]

    par_top_normalized = [
        (
            item["Rank"],
            item["Word"],
            item["Frequency"]
        )
        for item in parallel_top
    ]

    top_k_passed = (
        seq_top_normalized == par_top_normalized
    )

    if not top_k_passed:
        all_passed = False

    details.append({
        "Check": "Top-K frequencies",
        "Sequential": "Match" if top_k_passed else "Different",
        "Parallel": "Match" if top_k_passed else "Different",
        "Status": "PASS" if top_k_passed else "FAIL"
    })

    return {
        "passed": all_passed,
        "details": details,
        "error": None
    }

def build_performance_dataframe(benchmark_df):
    if benchmark_df is None or benchmark_df.empty:
        return pd.DataFrame()

    df = benchmark_df.copy()
    df["Execution Time"] = pd.to_numeric(df["Execution Time"], errors="coerce")
    df["Threads"] = pd.to_numeric(df["Threads"], errors="coerce")
    df = df.dropna(subset=["Execution Time", "Threads"])

    if df.empty:
        return pd.DataFrame()

    sequential_rows = df[df["Mode"] == "Sequential"]
    if sequential_rows.empty:
        return pd.DataFrame()

    sequential_time = float(sequential_rows.iloc[0]["Execution Time"])
    if sequential_time <= 0:
        return pd.DataFrame()

    parallel_df = df[df["Mode"] == "Parallel"].copy()
    if parallel_df.empty:
        return pd.DataFrame()

    parallel_df = parallel_df[parallel_df["Execution Time"] > 0].copy()
    if parallel_df.empty:
        return pd.DataFrame()

    parallel_df["Speedup"] = sequential_time / parallel_df["Execution Time"]
    parallel_df["Efficiency (%)"] = (
        parallel_df["Speedup"] / parallel_df["Threads"] * 100
    )

    return parallel_df.sort_values("Threads").reset_index(drop=True)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="cl-hero">
        <div class="cl-hero-tag">
            <span class="dot"></span>
            Design &amp; Analysis of Algorithms · Course Project
        </div>
        <div class="cl-hero-title">
            <span class="mark">◈</span>
            CorpusLens
        </div>
        <p class="cl-hero-sub">
            A C++ text analytics engine with an OpenMP parallel backend.
            Upload a corpus to measure lexical statistics, identify
            high-frequency terms, and evaluate thread-scaling performance
            against a sequential baseline.
        </p>
        <div class="cl-stat-strip">
            <span class="cl-chip"><span class="k">engine</span><span class="v">C++ / OpenMP</span></span>
            <span class="cl-chip"><span class="k">benchmark</span><span class="v">1 · 2 · 4 · 8 threads</span></span>
            <span class="cl-chip"><span class="k">metrics</span><span class="v">speedup · efficiency</span></span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <div style="display:flex;align-items:center;gap:10px;padding:6px 4px 18px;">
        <span style="width:34px;height:34px;display:inline-flex;align-items:center;justify-content:center;
                     background:linear-gradient(135deg,#e8a24a,#c9764a);border-radius:9px;
                     color:#1a1206;font-family:'Fraunces',serif;font-weight:700;font-size:1.1rem;">◈</span>
        <div>
            <div style="font-family:'Fraunces',serif;font-size:1.15rem;font-weight:600;
                        color:#f4f2ee;letter-spacing:-0.01em;line-height:1.1;">CorpusLens</div>
            <div style="font-size:0.68rem;letter-spacing:0.14em;text-transform:uppercase;
                        color:#8a8880;margin-top:2px;">Control Panel</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    "<div style='font-size:0.72rem;letter-spacing:0.12em;text-transform:uppercase;"
    "color:#8a8880;margin:8px 0 6px;'>01 — Corpus Input</div>",
    unsafe_allow_html=True
)

uploaded_file = st.sidebar.file_uploader(
    "Upload a text corpus",
    type=["txt"],
    label_visibility="collapsed"
)

if uploaded_file is not None:
    current_signature = (uploaded_file.name, uploaded_file.size)
    previous_signature = st.session_state.uploaded_file_signature

    if previous_signature is not None and current_signature != previous_signature:
        reset_results()

    st.session_state.uploaded_file_signature = current_signature

st.sidebar.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

st.sidebar.markdown(
    "<div style='font-size:0.72rem;letter-spacing:0.12em;text-transform:uppercase;"
    "color:#8a8880;margin:8px 0 6px;'>02 — Execution Mode</div>",
    unsafe_allow_html=True
)

mode = st.sidebar.radio(
    "Execution Mode",
    ["Parallel", "Sequential"],
    label_visibility="collapsed"
)

threads = 4
if mode == "Parallel":
    st.sidebar.markdown(
        "<div style='font-size:0.72rem;letter-spacing:0.12em;text-transform:uppercase;"
        "color:#8a8880;margin:14px 0 6px;'>03 — Thread Count</div>",
        unsafe_allow_html=True
    )
    threads = st.sidebar.slider(
        "Number of Threads",
        min_value=1,
        max_value=16,
        value=4,
        step=1,
        label_visibility="collapsed"
    )

st.sidebar.caption(
    "Performance benchmarking compares the sequential baseline "
    "with OpenMP runs using 1, 2, 4 and 8 threads."
)

st.sidebar.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

run_analysis = st.sidebar.button(
    "▶  Run Corpus Analysis",
    type="primary",
    use_container_width=True
)

run_benchmark = st.sidebar.button(
    "⚡ Run Performance Benchmark",
    use_container_width=True
)

run_correctness = st.sidebar.button(
    "✓ Run Correctness Check",
    use_container_width=True
)

clear_results = st.sidebar.button(
    "Clear Results",
    use_container_width=True
)

if clear_results:
    reset_results()
    st.session_state.uploaded_file_signature = None
    st.rerun()


# ============================================================
# NO FILE
# ============================================================

if uploaded_file is None:

    st.markdown(
        """
        <div class="cl-empty-state">
            <div class="glyph">◈</div>
            <div style="font-family:'Fraunces',serif;font-size:1.4rem;color:#f4f2ee;
                        margin-bottom:8px;">No corpus loaded</div>
            <div style="color:#8a8880;font-size:0.92rem;">
                Upload a <code style="color:#f0b96a;">.txt</code> file from the control panel to begin analysis.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

    section_label("MODULES", "What CorpusLens Provides")

    info1, info2, info3 = st.columns(3, gap="medium")

    with info1:
        st.markdown(
            f"""
            <div class="cl-feature">
                <div class="icon">{ICON["chart"]}</div>
                <h4>Corpus Analysis</h4>
                <ul>
                    <li>Total lines &amp; paragraphs</li>
                    <li>Total and unique words</li>
                    <li>Character and sentence counts</li>
                    <li>Average words per line / sentence</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    with info2:
        st.markdown(
            f"""
            <div class="cl-feature">
                <div class="icon">{ICON["list"]}</div>
                <h4>Frequency Analysis</h4>
                <ul>
                    <li>Top frequent words</li>
                    <li>Ranked frequency table</li>
                    <li>Distribution visualization</li>
                    <li>CSV export</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    with info3:
        st.markdown(
            f"""
            <div class="cl-feature">
                <div class="icon">{ICON["bolt"]}</div>
                <h4>Performance</h4>
                <ul>
                    <li>Sequential baseline</li>
                    <li>OpenMP parallel execution</li>
                    <li>Speedup &amp; parallel efficiency</li>
                    <li>Thread-scaling curves</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class="cl-footer">
            CorpusLens <span class="sep">◆</span> C++ Text Analysis
            <span class="sep">◆</span> OpenMP Parallel Processing
        </div>
        """,
        unsafe_allow_html=True
    )
    st.stop()


# ============================================================
# FILE INFORMATION
# ============================================================

file_size_mb = uploaded_file.size / (1024 * 1024)

st.markdown(
    f"""
    <div style="display:flex;align-items:center;gap:10px;padding:14px 18px;
                background:linear-gradient(90deg,rgba(232,162,74,0.10),rgba(232,162,74,0.02));
                border:1px solid rgba(232,162,74,0.22);border-radius:12px;margin-bottom:18px;">
        <span style="width:8px;height:8px;border-radius:50%;background:#e8a24a;
                     box-shadow:0 0 10px #e8a24a;"></span>
        <span style="color:#f4f2ee;font-weight:500;">Corpus loaded</span>
        <span style="color:#8a8880;">·</span>
        <span style="color:#f0b96a;font-family:'JetBrains Mono',monospace;font-size:0.85rem;">
            {uploaded_file.name}
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

f1, f2, f3 = st.columns(3, gap="medium")

f1.metric("File Name", uploaded_file.name)
f2.metric("File Size", f"{file_size_mb:.2f} MB")
f3.metric("Active Mode", mode)

# ============================================================
# RUN SELECTED CORPUS ANALYSIS
# ============================================================

if run_analysis:

    if uploaded_file is None:

        st.warning("Please upload a .txt corpus first.")

    else:

        temp_path = None

        try:
            temp_path = save_uploaded_file(uploaded_file)

            with st.spinner(
                f"Running {mode.lower()} corpus analysis..."
            ):
                output = run_engine(
                    temp_path,
                    mode,
                    threads
                )

            if output.startswith("ERROR"):

                st.error(
                    "The CorpusLens C++ engine returned an error."
                )

                st.code(
                    output,
                    language="text"
                )

            else:

                stats, top_words = parse_output(output)

                st.session_state.analysis_done = True

                st.session_state.analysis_output = output

                st.session_state.analysis_stats = stats

                st.session_state.analysis_top_words = top_words

                st.session_state.uploaded_filename = uploaded_file.name

                st.session_state.analysis_mode = mode

                # Clear old benchmark/correctness results because
                # a new analysis has been performed.
                st.session_state.benchmark_df = pd.DataFrame()

                st.session_state.benchmark_errors = []

                st.session_state.correctness_done = False
                st.session_state.correctness_passed = False
                st.session_state.correctness_details = []
                st.session_state.correctness_error = None

                st.success(
                    f"{mode} analysis completed successfully."
                )

        finally:

            if temp_path is not None:

                try:
                    os.unlink(temp_path)

                except Exception:
                    pass

if run_benchmark:

    if uploaded_file is None:

        st.warning("Please upload a .txt corpus first.")

    else:

        temp_path = None

        try:

            temp_path = save_uploaded_file(uploaded_file)

            with st.spinner(
                "Running sequential baseline and OpenMP "
                "thread-scaling benchmark..."
            ):

                benchmark_df, benchmark_errors = (
                    benchmark_uploaded_file(temp_path)
                )

            st.session_state.benchmark_df = benchmark_df

            st.session_state.benchmark_errors = benchmark_errors

            st.session_state.uploaded_filename = uploaded_file.name

            if benchmark_df.empty:

                st.error(
                    "No valid benchmark results were produced."
                )

            else:

                st.success(
                    "Performance benchmark completed successfully."
                )

        finally:

            if temp_path is not None:

                try:
                    os.unlink(temp_path)

                except Exception:
                    pass

# ============================================================
# RUN CORRECTNESS CHECK
# ============================================================

if run_correctness:

    if uploaded_file is None:

        st.warning("Please upload a .txt corpus first.")

    else:

        temp_path = None

        try:

            temp_path = save_uploaded_file(uploaded_file)

            with st.spinner(
                "Comparing sequential and parallel results..."
            ):

                correctness_result = verify_correctness(
                    temp_path,
                    threads
                )

            st.session_state.correctness_done = True

            st.session_state.correctness_passed = (
                correctness_result["passed"]
            )

            st.session_state.correctness_details = (
                correctness_result["details"]
            )

            st.session_state.correctness_error = (
                correctness_result["error"]
            )

            st.session_state.uploaded_filename = (
                uploaded_file.name
            )

        finally:

            if temp_path is not None:

                try:
                    os.unlink(temp_path)

                except Exception:
                    pass
# ============================================================
# DISPLAY RESULTS
# ============================================================

if st.session_state.analysis_done:

    stats = st.session_state.analysis_stats
    top_words = st.session_state.analysis_top_words
    benchmark_df = st.session_state.benchmark_df
    benchmark_errors = st.session_state.benchmark_errors

    tab1, tab2, tab3, tab4 = st.tabs(
    [
        "  Corpus Analysis",
        "  Word Frequency",
        "  Performance",
        "  Correctness"
    ]
    )

    with tab1:

        section_label("01", "Corpus Statistics")

        st.caption(
            f"Analysis results for **{st.session_state.uploaded_filename}**"
        )

        c1, c2, c3, c4 = st.columns(4, gap="medium")

        c1.metric("Total Lines", f"{stats.get('total_lines', 0):,}")
        c2.metric("Total Paragraphs", f"{stats.get('total_paragraphs', 0):,}")
        c3.metric("Total Words", f"{stats.get('total_words', 0):,}")
        c4.metric("Unique Words", f"{stats.get('unique_words', 0):,}")

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        c5, c6, c7, c8 = st.columns(4, gap="medium")

        c5.metric("Characters", f"{stats.get('total_characters', 0):,}")
        c6.metric("Sentences", f"{stats.get('total_sentences', 0):,}")
        c7.metric("Words / Line", f"{stats.get('avg_words_line', 0):.2f}")
        c8.metric("Words / Sentence", f"{stats.get('avg_words_sentence', 0):.2f}")

        st.divider()

        section_label("02", "Derived Statistics")

        additional_stats = pd.DataFrame(
            {
                "Metric": [
                    "Average words per line",
                    "Average words per sentence",
                    "Average characters per line"
                ],
                "Value": [
                    stats.get("avg_words_line", 0),
                    stats.get("avg_words_sentence", 0),
                    stats.get("avg_characters_line", 0)
                ]
            }
        )

        st.dataframe(additional_stats, use_container_width=True, hide_index=True)

        st.divider()

        section_label("03", "Selected Execution")

        execution_time = stats.get("execution_time")

        e1, e2 = st.columns(2, gap="medium")

        if execution_time is not None:
            e1.metric("Execution Time", f"{execution_time:.6f} s")

        if mode == "Parallel":
            e2.metric("Threads Used", stats.get("threads", threads))
        else:
            e2.metric("Execution Type", "Sequential")

    with tab2:

        section_label("01", "Word Frequency Analysis")

        st.caption(
            f"Top frequent words from **{st.session_state.uploaded_filename}**."
        )

        if top_words:

            top_df = pd.DataFrame(top_words)

            left, right = st.columns([1, 1], gap="large")

            with left:
                st.markdown(
                    "<div style='font-size:0.72rem;letter-spacing:0.12em;"
                    "text-transform:uppercase;color:#8a8880;margin-bottom:10px;'>"
                    "Ranked Terms</div>",
                    unsafe_allow_html=True
                )
                st.dataframe(top_df, use_container_width=True, hide_index=True)

            with right:
                st.markdown(
                    "<div style='font-size:0.72rem;letter-spacing:0.12em;"
                    "text-transform:uppercase;color:#8a8880;margin-bottom:10px;'>"
                    "Frequency Distribution</div>",
                    unsafe_allow_html=True
                )
                chart_data = top_df.set_index("Word")["Frequency"]
                st.bar_chart(chart_data, use_container_width=True)

            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

            st.download_button(
                "Download Word Frequencies",
                data=top_df.to_csv(index=False),
                file_name="corpuslens_top_words.csv",
                mime="text/csv",
                use_container_width=True
            )

        else:
            st.info("No top-word information was returned by the C++ engine.")

    with tab3:

        section_label("01", "Performance Benchmark")

        st.caption(
            f"Performance results for **{st.session_state.uploaded_filename}**."
        )

        st.info(
            "The sequential result is used as the baseline for calculating "
            "parallel speedup. The parallel scaling experiment measures "
            "1, 2, 4 and 8 threads."
        )

        if benchmark_errors:
            with st.expander("Benchmark diagnostics"):
                for error in benchmark_errors:
                    st.warning(error)

        if benchmark_df.empty:

            st.warning("No benchmark results are available.")
            st.info(
                "For meaningful timing results, use a reasonably large "
                "corpus such as test.txt."
            )

        else:

            performance_df = build_performance_dataframe(benchmark_df)

            sequential_rows = benchmark_df[
                benchmark_df["Mode"] == "Sequential"
            ]

            if not sequential_rows.empty and not performance_df.empty:

                sequential_time = float(
                    sequential_rows.iloc[0]["Execution Time"]
                )

                fastest_index = performance_df["Execution Time"].idxmin()
                fastest_row = performance_df.loc[fastest_index]

                fastest_time = float(fastest_row["Execution Time"])
                fastest_threads = int(fastest_row["Threads"])
                fastest_speedup = float(fastest_row["Speedup"])

                section_label("02", "Performance Summary")

                p1, p2, p3, p4 = st.columns(4, gap="medium")

                p1.metric("Sequential Baseline", f"{sequential_time:.6f} s")
                p2.metric("Fastest Parallel", f"{fastest_time:.6f} s")
                p3.metric("Best Thread Count", fastest_threads)
                p4.metric("Maximum Speedup", f"{fastest_speedup:.2f}×")

                st.divider()

                section_label("03", "Thread Benchmark")

                display_df = benchmark_df.copy()
                display_df["Execution Time"] = display_df["Execution Time"].map(
                    lambda x: f"{x:.6f} s"
                )

                st.dataframe(display_df, use_container_width=True, hide_index=True)

                st.caption(
                    "Sequential is the baseline. Parallel results show "
                    "thread scaling for the current corpus."
                )

                st.divider()

                section_label("04", "Execution Time vs Threads")

                time_chart = (
                    performance_df[["Threads", "Execution Time"]]
                    .sort_values("Threads")
                    .set_index("Threads")
                )
                st.line_chart(time_chart, use_container_width=True)
                st.caption("Lower execution time indicates faster processing.")

                st.divider()

                section_label("05", "Speedup vs Threads")

                speedup_chart = (
                    performance_df[["Threads", "Speedup"]]
                    .sort_values("Threads")
                    .set_index("Threads")
                )
                st.line_chart(speedup_chart, use_container_width=True)
                st.caption("Speedup = Sequential Time / Parallel Time.")

                st.divider()

                section_label("06", "Parallel Efficiency vs Threads")

                efficiency_chart = (
                    performance_df[["Threads", "Efficiency (%)"]]
                    .sort_values("Threads")
                    .set_index("Threads")
                )
                st.line_chart(efficiency_chart, use_container_width=True)
                st.caption("Efficiency = Speedup / Number of Threads × 100.")

                st.divider()

                section_label("07", "Detailed Performance Metrics")

                metrics_df = performance_df[
                    ["Threads", "Execution Time", "Speedup", "Efficiency (%)"]
                ].copy()

                metrics_df["Execution Time"] = metrics_df["Execution Time"].round(6)
                metrics_df["Speedup"] = metrics_df["Speedup"].round(3)
                metrics_df["Efficiency (%)"] = metrics_df["Efficiency (%)"].round(2)

                st.dataframe(metrics_df, use_container_width=True, hide_index=True)

                download_df = performance_df.copy()

                st.download_button(
                    "Download Performance Results",
                    data=download_df.to_csv(index=False),
                    file_name="corpuslens_performance.csv",
                    mime="text/csv",
                    use_container_width=True
                )

                st.divider()

                section_label("08", "Performance Interpretation")

                st.markdown(
                    f"""
                    <div style="background:linear-gradient(160deg,#14161a,#0f1013);
                                border:1px solid rgba(255,255,255,0.06);
                                border-radius:14px;padding:22px 24px;
                                border-left:3px solid #e8a24a;">
                        <p style="margin:0 0 12px 0;color:#c9c6c0;line-height:1.65;">
                            The uploaded corpus required
                            <span style="color:#f0b96a;font-family:'JetBrains Mono',monospace;font-weight:600;">
                                {sequential_time:.6f} seconds
                            </span>
                            using the sequential implementation.
                        </p>
                        <p style="margin:0 0 12px 0;color:#c9c6c0;line-height:1.65;">
                            The fastest measured parallel execution was
                            <span style="color:#f0b96a;font-family:'JetBrains Mono',monospace;font-weight:600;">
                                {fastest_time:.6f} seconds
                            </span>
                            using
                            <span style="color:#f0b96a;font-family:'JetBrains Mono',monospace;font-weight:600;">
                                {fastest_threads} threads
                            </span>.
                        </p>
                        <p style="margin:0;color:#c9c6c0;line-height:1.65;">
                            The measured speedup relative to the sequential
                            baseline was
                            <span style="color:#f0b96a;font-family:'JetBrains Mono',monospace;font-weight:600;">
                                {fastest_speedup:.2f}×
                            </span>.
                            The benchmark shows how execution time, speedup
                            and parallel efficiency change as the number of
                            OpenMP threads increases.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.warning(
                    "The corpus was analyzed, but there is insufficient "
                    "timing data to calculate speedup and efficiency."
                )
                st.info(
                    "This commonly happens with very small files where "
                    "execution time is measured as 0.00 seconds. "
                    "Try a larger corpus such as test.txt."
                )

        st.divider()

    with tab4:

        section_label(
            "01",
            "Sequential vs Parallel Correctness"
        )

        st.caption(
            f"Verification results for "
            f"**{st.session_state.uploaded_filename}**."
        )

        st.info(
            "The same corpus is processed by the sequential "
            "and OpenMP parallel implementations. Statistical "
            "results and Top-K frequencies are compared."
        )

        c1, c2, c3 = st.columns(3, gap="medium")

        c1.metric(
            "Input Corpus",
            st.session_state.uploaded_filename
        )

        c2.metric(
            "Parallel Threads",
            threads
        )

        if st.session_state.correctness_done:

            if st.session_state.correctness_passed:

                c3.metric(
                    "Result",
                    "PASS"
                )

                st.success(
                    "✓ Sequential and parallel implementations "
                    "produced matching results."
                )

            else:

                c3.metric(
                    "Result",
                    "FAIL"
                )

                st.error(
                    "✗ Sequential and parallel results do not match."
                )

            if st.session_state.correctness_error:

                st.error(
                    st.session_state.correctness_error
                )

            if st.session_state.correctness_details:

                st.divider()

                section_label(
                    "02",
                    "Verification Details"
                )

                correctness_df = pd.DataFrame(
                    st.session_state.correctness_details
                )

                st.dataframe(
                    correctness_df,
                    use_container_width=True,
                    hide_index=True
                )

        else:

            st.warning(
                "Correctness verification has not been run yet."
            )

            st.markdown(
                """
                <div style="
                    padding:20px;
                    border:1px dashed rgba(232,162,74,0.30);
                    border-radius:12px;
                    margin-top:12px;
                ">
                    <strong>What will be checked?</strong>
                    <ul>
                        <li>Total lines</li>
                        <li>Total paragraphs</li>
                        <li>Total words</li>
                        <li>Unique words</li>
                        <li>Total characters</li>
                        <li>Total sentences</li>
                        <li>Average statistics</li>
                        <li>Top-K frequencies</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )
        with st.expander("View Raw C++ Output"):
            st.code(st.session_state.analysis_output, language="text")


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="cl-footer">
        CorpusLens <span class="sep">◆</span> C++ Text Analysis
        <span class="sep">◆</span> OpenMP Parallel Processing
    </div>
    """,
    unsafe_allow_html=True
)