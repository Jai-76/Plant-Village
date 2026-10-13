"""
Smart Plant Disease Identification System — Web UI
Run: streamlit run app.py
"""

import base64
import io
import time
from pathlib import Path
import streamlit as st
from PIL import Image
from datetime import datetime

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PlantGuard AI · Disease Identification",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Session state init ──────────────────────────────────────────────────────
if "scan_history" not in st.session_state:
    st.session_state.scan_history = []
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "scan"
if "use_demo" not in st.session_state:
    st.session_state.use_demo = False

# ─── Inject Custom CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
/* ══════════════════════════════════════════════════════════════════════════
   FONTS
   ══════════════════════════════════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ══════════════════════════════════════════════════════════════════════════
   GLOBAL / RESET
   ══════════════════════════════════════════════════════════════════════════ */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}
.stApp {
    background: linear-gradient(160deg, #050d1a 0%, #0a1929 30%, #071a12 70%, #050d1a 100%);
    min-height: 100vh;
}
#MainMenu, footer, header { visibility: hidden; }

/* Remove default padding */
.block-container { padding-top: 1.5rem !important; }

/* ══════════════════════════════════════════════════════════════════════════
   ANIMATED BACKGROUND PARTICLES
   ══════════════════════════════════════════════════════════════════════════ */
.bg-glow {
    position: fixed;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.08;
    pointer-events: none;
    z-index: 0;
    animation: float 20s ease-in-out infinite;
}
.bg-glow-1 { width: 500px; height: 500px; background: #10b981; top: -100px; right: -100px; }
.bg-glow-2 { width: 400px; height: 400px; background: #0ea5e9; bottom: -50px; left: -50px; animation-delay: -7s; }
.bg-glow-3 { width: 300px; height: 300px; background: #8b5cf6; top: 40%; left: 30%; animation-delay: -14s; }
@keyframes float {
    0%, 100% { transform: translate(0, 0) scale(1); }
    33%      { transform: translate(30px, -20px) scale(1.05); }
    66%      { transform: translate(-20px, 20px) scale(0.95); }
}

/* ══════════════════════════════════════════════════════════════════════════
   HERO SECTION
   ══════════════════════════════════════════════════════════════════════════ */
.hero {
    background: linear-gradient(135deg, rgba(16,185,129,0.08) 0%, rgba(5,150,105,0.04) 50%, rgba(14,165,233,0.06) 100%);
    border: 1px solid rgba(16,185,129,0.15);
    border-radius: 24px;
    padding: 2rem 2.5rem 1.75rem;
    margin-bottom: 1.75rem;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(20px);
}
.hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(16,185,129,0.4), rgba(14,165,233,0.3), transparent);
}
.hero::after {
    content: '';
    position: absolute;
    top: -40%; right: -5%;
    width: 350px; height: 350px;
    background: radial-gradient(circle, rgba(16,185,129,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.25);
    color: #34d399;
    padding: 0.3rem 0.85rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.85rem;
}
.hero-badge .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #10b981;
    animation: blink 2s ease infinite;
}
@keyframes blink {
    0%, 100% { opacity: 1; }
    50%      { opacity: 0.3; }
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #10b981 0%, #34d399 40%, #6ee7b7 70%, #a7f3d0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    line-height: 1.15;
    letter-spacing: -0.02em;
}
.hero-sub {
    color: #7c8da6;
    font-size: 1rem;
    margin-top: 0.65rem;
    font-weight: 400;
    line-height: 1.6;
    max-width: 600px;
}
.hero-sub b { color: #cbd5e1; }

/* ══════════════════════════════════════════════════════════════════════════
   GLASS CARD
   ══════════════════════════════════════════════════════════════════════════ */
.glass {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 18px;
    padding: 1.5rem;
    backdrop-filter: blur(12px);
    transition: all 0.35s cubic-bezier(.4,0,.2,1);
    position: relative;
    overflow: hidden;
}
.glass::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
}
.glass:hover {
    border-color: rgba(16,185,129,0.2);
    background: rgba(255,255,255,0.035);
    transform: translateY(-1px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}

/* ══════════════════════════════════════════════════════════════════════════
   UPLOAD ZONE
   ══════════════════════════════════════════════════════════════════════════ */
[data-testid="stFileUploader"] {
    background: rgba(16,185,129,0.03) !important;
    border: 2px dashed rgba(16,185,129,0.25) !important;
    border-radius: 18px !important;
    padding: 1.25rem !important;
    transition: all 0.3s ease !important;
}
[data-testid="stFileUploader"]:hover {
    background: rgba(16,185,129,0.06) !important;
    border-color: rgba(16,185,129,0.5) !important;
    box-shadow: 0 0 30px rgba(16,185,129,0.08) !important;
}

/* ══════════════════════════════════════════════════════════════════════════
   RESULT CARDS
   ══════════════════════════════════════════════════════════════════════════ */
.result-card {
    border-radius: 20px;
    padding: 1.75rem 2rem;
    animation: slideUp 0.6s cubic-bezier(.4,0,.2,1);
    position: relative;
    overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
}
.result-healthy {
    background: linear-gradient(135deg, rgba(16,185,129,0.12) 0%, rgba(5,150,105,0.06) 100%);
    border: 1px solid rgba(16,185,129,0.3);
}
.result-healthy::before { background: linear-gradient(90deg, transparent, rgba(16,185,129,0.5), transparent); }
.result-disease {
    background: linear-gradient(135deg, rgba(239,68,68,0.1) 0%, rgba(220,38,38,0.05) 100%);
    border: 1px solid rgba(239,68,68,0.3);
}
.result-disease::before { background: linear-gradient(90deg, transparent, rgba(239,68,68,0.5), transparent); }
.result-warning {
    background: linear-gradient(135deg, rgba(245,158,11,0.1) 0%, rgba(217,119,6,0.05) 100%);
    border: 1px solid rgba(245,158,11,0.3);
}
.result-warning::before { background: linear-gradient(90deg, transparent, rgba(245,158,11,0.5), transparent); }
.result-critical {
    background: linear-gradient(135deg, rgba(220,38,38,0.12) 0%, rgba(185,28,28,0.06) 100%);
    border: 1px solid rgba(220,38,38,0.35);
}
.result-critical::before { background: linear-gradient(90deg, transparent, rgba(220,38,38,0.6), transparent); }

@keyframes slideUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

.result-icon { font-size: 2.8rem; margin-bottom: 0.6rem; }
.result-status {
    display: inline-block;
    padding: 0.25rem 0.85rem;
    border-radius: 999px;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.result-crop {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.75rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0.3rem 0;
    line-height: 1.2;
}
.result-cond {
    font-size: 1.15rem;
    font-weight: 600;
    margin: 0.15rem 0;
}
.result-conf {
    font-size: 0.88rem;
    color: #7c8da6;
    margin-top: 0.65rem;
}

/* Confidence gauge */
.gauge-track {
    margin-top: 0.85rem;
    background: rgba(255,255,255,0.06);
    border-radius: 999px;
    height: 10px;
    overflow: hidden;
    position: relative;
}
.gauge-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 1.2s cubic-bezier(.4,0,.2,1);
    position: relative;
}
.gauge-fill::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 20px; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3));
    border-radius: 999px;
}

/* ══════════════════════════════════════════════════════════════════════════
   CONFIDENCE BARS (top-k predictions)
   ══════════════════════════════════════════════════════════════════════════ */
.pred-bar {
    margin: 0.5rem 0;
    padding: 0.7rem 1rem;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    transition: all 0.25s ease;
    animation: slideUp 0.5s ease;
}
.pred-bar:hover {
    background: rgba(255,255,255,0.05);
    border-color: rgba(255,255,255,0.1);
    transform: translateX(4px);
}
.pred-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.84rem;
    color: #94a3b8;
    margin-bottom: 0.35rem;
    font-weight: 500;
}
.pred-track {
    background: rgba(255,255,255,0.06);
    border-radius: 999px;
    height: 6px;
    overflow: hidden;
}
.pred-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 1s cubic-bezier(.4,0,.2,1);
}

/* ══════════════════════════════════════════════════════════════════════════
   INFO CARDS (treatment, prevention, symptoms)
   ══════════════════════════════════════════════════════════════════════════ */
.info-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 1.25rem 1.4rem;
    margin-bottom: 0.75rem;
    transition: all 0.3s ease;
    animation: slideUp 0.5s ease;
}
.info-card:hover {
    border-color: rgba(255,255,255,0.12);
    background: rgba(255,255,255,0.035);
}
.info-card-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.info-list {
    list-style: none;
    padding: 0;
    margin: 0;
}
.info-list li {
    position: relative;
    padding: 0.35rem 0 0.35rem 1.4rem;
    font-size: 0.84rem;
    color: #94a3b8;
    line-height: 1.55;
}
.info-list li::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0.7rem;
    width: 6px;
    height: 6px;
    border-radius: 50%;
}
.info-list.green li::before  { background: #10b981; }
.info-list.amber li::before  { background: #f59e0b; }
.info-list.red li::before    { background: #ef4444; }
.info-list.blue li::before   { background: #0ea5e9; }

/* ══════════════════════════════════════════════════════════════════════════
   SEVERITY BADGE
   ══════════════════════════════════════════════════════════════════════════ */
.severity-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.3rem 0.8rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* ══════════════════════════════════════════════════════════════════════════
   METRIC TILES
   ══════════════════════════════════════════════════════════════════════════ */
.metric {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 1.1rem 1rem;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.metric::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent);
}
.metric:hover {
    border-color: rgba(16,185,129,0.2);
    transform: translateY(-2px);
    box-shadow: 0 6px 24px rgba(0,0,0,0.15);
}
.metric-icon { font-size: 1.5rem; margin-bottom: 0.4rem; }
.metric-val {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: #34d399;
    line-height: 1.2;
    white-space: nowrap;
}
.metric-lbl {
    font-size: 0.72rem;
    color: #4b6584;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-top: 0.35rem;
    font-weight: 500;
}

/* ══════════════════════════════════════════════════════════════════════════
   SECTION HEADINGS
   ══════════════════════════════════════════════════════════════════════════ */
.section-h {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.88rem;
    font-weight: 600;
    color: #6b7f99;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 1.5rem 0 0.85rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-h::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(255,255,255,0.06), transparent);
}

/* ══════════════════════════════════════════════════════════════════════════
   PIPELINE STEPS
   ══════════════════════════════════════════════════════════════════════════ */
.step {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 1rem 0.6rem;
    text-align: center;
    transition: all 0.3s ease;
}
.step:hover {
    border-color: rgba(16,185,129,0.25);
    background: rgba(16,185,129,0.04);
    transform: translateY(-3px);
}
.step-icon { font-size: 1.5rem; }
.step-title {
    font-size: 0.78rem;
    font-weight: 600;
    color: #cbd5e1;
    margin-top: 0.35rem;
}
.step-sub {
    font-size: 0.65rem;
    color: #4b6584;
    margin-top: 0.2rem;
}

/* ══════════════════════════════════════════════════════════════════════════
   HISTORY ITEM
   ══════════════════════════════════════════════════════════════════════════ */
.hist-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.6rem 0.85rem;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 10px;
    margin-bottom: 0.4rem;
    transition: all 0.2s ease;
    cursor: default;
}
.hist-item:hover {
    background: rgba(255,255,255,0.04);
    border-color: rgba(255,255,255,0.1);
}
.hist-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}
.hist-text {
    flex: 1;
    font-size: 0.78rem;
    color: #94a3b8;
    line-height: 1.4;
}
.hist-text b { color: #cbd5e1; }
.hist-conf {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 500;
    padding: 0.15rem 0.5rem;
    border-radius: 6px;
    background: rgba(255,255,255,0.04);
}

/* ══════════════════════════════════════════════════════════════════════════
   SIDEBAR
   ══════════════════════════════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: rgba(5,13,26,0.95) !important;
    border-right: 1px solid rgba(255,255,255,0.04) !important;
    backdrop-filter: blur(20px) !important;
}
.sb-section {
    background: rgba(16,185,129,0.04);
    border: 1px solid rgba(16,185,129,0.1);
    border-radius: 14px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.85rem;
}
.sb-title {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 0.78rem;
    color: #34d399;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.55rem;
    display: flex;
    align-items: center;
    gap: 0.35rem;
}
.sb-text {
    font-size: 0.8rem;
    color: #7c8da6;
    line-height: 1.65;
}
.sb-text b { color: #a7f3d0; }
.tag {
    display: inline-block;
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.2);
    color: #6ee7b7;
    padding: 0.2rem 0.55rem;
    border-radius: 6px;
    font-size: 0.7rem;
    font-weight: 500;
    margin: 0.12rem;
    transition: all 0.2s ease;
}
.tag:hover { background: rgba(16,185,129,0.18); border-color: rgba(16,185,129,0.35); }

/* ══════════════════════════════════════════════════════════════════════════
   DISCLAIMER
   ══════════════════════════════════════════════════════════════════════════ */
.disclaimer {
    background: rgba(245,158,11,0.05);
    border: 1px solid rgba(245,158,11,0.15);
    border-radius: 14px;
    padding: 0.85rem 1.15rem;
    font-size: 0.8rem;
    color: #d97706;
    margin-top: 1.5rem;
    display: flex;
    align-items: flex-start;
    gap: 0.6rem;
    line-height: 1.55;
}

/* ══════════════════════════════════════════════════════════════════════════
   IMAGE STYLING
   ══════════════════════════════════════════════════════════════════════════ */
[data-testid="stImage"] img {
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.06);
}

/* Spinner color */
.stSpinner > div { border-top-color: #10b981 !important; }

/* ══════════════════════════════════════════════════════════════════════════
   DESCRIPTION TEXT
   ══════════════════════════════════════════════════════════════════════════ */
.desc-text {
    font-size: 0.88rem;
    color: #94a3b8;
    line-height: 1.7;
    padding: 0.85rem 1rem;
    background: rgba(255,255,255,0.015);
    border-left: 3px solid rgba(16,185,129,0.3);
    border-radius: 0 10px 10px 0;
    margin: 0.75rem 0;
}

/* ══════════════════════════════════════════════════════════════════════════
   FOOTER
   ══════════════════════════════════════════════════════════════════════════ */
.footer {
    text-align: center;
    color: #1e3a2e;
    font-size: 0.72rem;
    margin-top: 2.5rem;
    padding-bottom: 1rem;
    opacity: 0.6;
}
</style>
""", unsafe_allow_html=True)

# ─── Background glow elements ────────────────────────────────────────────────
st.markdown("""
<div class="bg-glow bg-glow-1"></div>
<div class="bg-glow bg-glow-2"></div>
<div class="bg-glow bg-glow-3"></div>
""", unsafe_allow_html=True)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:1rem 0 1.5rem 0;">
        <div style="font-size:3.2rem; margin-bottom:0.3rem;">🌿</div>
        <div style="font-family:'Space Grotesk',sans-serif; font-size:1.35rem; font-weight:700;
                    background:linear-gradient(135deg,#10b981,#34d399,#6ee7b7);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text;">
            PlantGuard AI
        </div>
        <div style="color:#4b6584; font-size:0.75rem; margin-top:0.3rem;
                    letter-spacing:0.05em; text-transform:uppercase; font-weight:500;">
            Disease Identification System
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sb-section">
        <div class="sb-title">📋 How to Use</div>
        <div class="sb-text">
            <b>1.</b> Upload a clear photo of a <b>single leaf</b><br>
            <b>2.</b> Ensure good lighting & sharp focus<br>
            <b>3.</b> Avoid cluttered backgrounds<br>
            <b>4.</b> Read the AI diagnosis & treatment plan
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sb-section">
        <div class="sb-title">🧠 Model Details</div>
        <div class="sb-text">
            Architecture: <b>EfficientNetB3 / MobileNetV2</b><br>
            Dataset: <b>PlantVillage (54K+ images)</b><br>
            Input: <b>224 × 224 px RGB</b><br>
            Output: <b>38 disease classes</b><br>
            Pipeline: resize → scale → backbone → softmax
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sb-section">
        <div class="sb-title">🌱 Supported Crops</div>
        <div class="sb-text">
            <span class="tag">Apple</span><span class="tag">Tomato</span><span class="tag">Corn</span>
            <span class="tag">Potato</span><span class="tag">Grape</span><span class="tag">Pepper</span>
            <span class="tag">Cherry</span><span class="tag">Peach</span><span class="tag">Strawberry</span>
            <span class="tag">Orange</span><span class="tag">Squash</span><span class="tag">Raspberry</span>
            <span class="tag">Blueberry</span><span class="tag">Soybean</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Settings section
    st.markdown('<div class="sb-section"><div class="sb-title">⚙️ Settings</div></div>',
                unsafe_allow_html=True)
    conf_threshold = st.slider("Confidence threshold", 0.30, 0.95, 0.60, 0.05,
                                help="Predictions below this are flagged as low-confidence.")
    top_k = st.selectbox("Top-K predictions", [3, 5, 10], index=0)

    # Scan history
    if st.session_state.scan_history:
        st.markdown('<div class="sb-section"><div class="sb-title">📜 Scan History</div></div>',
                    unsafe_allow_html=True)
        for entry in reversed(st.session_state.scan_history[-8:]):
            sev = entry.get("severity", "none")
            dot_color = {"none": "#10b981", "moderate": "#f59e0b",
                         "high": "#ef4444", "critical": "#dc2626"}.get(sev, "#64748b")
            conf_color = dot_color
            st.markdown(f"""
            <div class="hist-item">
                <div class="hist-dot" style="background:{dot_color};"></div>
                <div class="hist-text">
                    <b>{entry['crop']}</b><br>{entry['condition']}
                </div>
                <div class="hist-conf" style="color:{conf_color};">{entry['confidence']:.0%}</div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN CONTENT
# ═══════════════════════════════════════════════════════════════════════════════

# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">
        <span class="dot"></span>
        AI-Powered · Deep Learning · PlantVillage
    </div>
    <h1 class="hero-title">🌿 PlantGuard AI</h1>
    <p class="hero-sub">
        Upload a leaf photo for instant <b>AI-powered disease diagnosis</b> with detailed
        treatment recommendations. Powered by deep learning trained on 54,000+ plant images.
    </p>
</div>
""", unsafe_allow_html=True)

# ─── Main two-column layout ──────────────────────────────────────────────────
col_upload, col_result = st.columns([1, 1.2], gap="large")

with col_upload:
    st.markdown('<div class="section-h">📷 Select Leaf Source</div>', unsafe_allow_html=True)

    input_mode = st.radio(
        "Source Mode",
        ["🌿 Try Demo Sample Leaf", "📁 Upload Custom Image"],
        horizontal=True,
        label_visibility="collapsed",
    )

    img = None
    img_meta = {}

    if input_mode == "📁 Upload Custom Image":
        file = st.file_uploader(
            "Drop or click to upload a leaf image",
            type=["jpg", "jpeg", "png", "webp"],
            label_visibility="collapsed",
        )
        if file is not None:
            img = Image.open(file)
            w, h = img.size
            img_meta = {
                "name": file.name,
                "size": f"{len(file.getvalue()) / 1024:.1f} KB",
                "dims": f"{w}×{h}px",
                "mode": img.mode,
            }
    else:
        sample_choice = st.selectbox(
            "Choose a demo leaf to diagnose:",
            [
                "🍅 Tomato — Early Blight",
                "🥔 Potato — Late Blight",
                "🌽 Corn — Common Rust",
                "🍇 Grape — Black Measles",
                "🍎 Apple — Apple Scab",
            ],
            index=0,
            label_visibility="collapsed",
        )
        sample_files = {
            "🍅 Tomato — Early Blight": ("sample_tomato.jpg", "Tomato · Early Blight"),
            "🥔 Potato — Late Blight": ("sample_potato.jpg", "Potato · Late Blight"),
            "🌽 Corn — Common Rust": ("sample_corn.jpg", "Corn · Common Rust"),
            "🍇 Grape — Black Measles": ("sample_grape.jpg", "Grape · Black Measles"),
            "🍎 Apple — Apple Scab": ("sample_apple.jpg", "Apple · Apple Scab"),
        }
        fname, display_name = sample_files[sample_choice]
        demo_path = Path(__file__).resolve().parent / fname
        if demo_path.exists():
            img = Image.open(demo_path)
            w, h = img.size
            img_meta = {
                "name": f"{fname} ({display_name})",
                "size": f"{demo_path.stat().st_size / 1024:.1f} KB",
                "dims": f"{w}×{h}px",
                "mode": img.mode,
            }

    if img is not None:
        st.image(img, caption=f"📸 {img_meta.get('name', 'Leaf Image')}", use_container_width=True)

        st.markdown(f"""
        <div class="glass" style="padding:0.85rem 1.15rem; margin-top:0.5rem;">
            <div style="display:flex; gap:1.2rem; flex-wrap:wrap; color:#7c8da6; font-size:0.8rem;">
                <span>📐 <b style="color:#cbd5e1">{img_meta.get('dims', '')}</b></span>
                <span>🎨 <b style="color:#cbd5e1">{img_meta.get('mode', '')}</b></span>
                <span>📁 <b style="color:#cbd5e1">{img_meta.get('name', '')}</b></span>
                <span>💾 <b style="color:#cbd5e1">{img_meta.get('size', '')}</b></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_result:
    st.markdown('<div class="section-h">🧬 Diagnosis Results</div>', unsafe_allow_html=True)

    if img is None:
        # Empty state
        st.markdown("""
        <div class="glass" style="text-align:center; padding:3.5rem 2rem;">
            <div style="font-size:4rem; margin-bottom:1rem; opacity:0.6;">🍃</div>
            <div style="font-size:1.05rem; font-weight:600; color:#4b6584;">
                Awaiting leaf image…
            </div>
            <div style="font-size:0.82rem; margin-top:0.5rem; color:#384d65; max-width:280px; margin-left:auto; margin-right:auto; line-height:1.5;">
                Upload a clear photo of a single plant leaf to begin AI-powered disease analysis
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # ── Run inference ─────────────────────────────────────────────────
        try:
            from predict import predict as run_predict, pretty
            with st.spinner("🔬 Analyzing leaf with AI model…"):
                results = run_predict(img, top_k=top_k)
            inference_ok = True
        except FileNotFoundError as e:
            inference_ok = False
            model_error = str(e).split("\n")[0]
            model_hint = "python train.py --model efficientnet --epochs 40"
        except Exception as e:
            inference_ok = False
            model_error = f"{type(e).__name__}: {e}"
            model_hint = "Check the console for details."

        if not inference_ok:
            st.markdown(f"""
            <div class="result-card result-warning">
                <div class="result-icon">⚠️</div>
                <div class="result-status" style="background:rgba(245,158,11,0.15); color:#fbbf24;">
                    Model Not Found
                </div>
                <div class="result-crop" style="font-size:1.3rem;">No Trained Model Available</div>
                <div style="color:#d97706; font-size:0.84rem; margin-top:0.75rem; line-height:1.6;">
                    {model_error}
                </div>
                <div style="background:rgba(0,0,0,0.3); border-radius:10px; padding:0.75rem 1rem;
                            margin-top:1rem; font-size:0.8rem; color:#7c8da6;">
                    <b style="color:#6ee7b7;">Train the model first:</b><br>
                    <code style="color:#a7f3d0; font-family:'JetBrains Mono',monospace; font-size:0.78rem;">
                        {model_hint}
                    </code>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # ── Import disease info ───────────────────────────────────────
            try:
                from disease_info import DISEASE_INFO, SEVERITY_MAP
                has_disease_info = True
            except ImportError:
                has_disease_info = False

            name, conf = results[0]
            crop, cond = pretty(name)

            # Get disease details
            disease_data = DISEASE_INFO.get(name, {}) if has_disease_info else {}
            severity = disease_data.get("severity", "none")
            sev_info = SEVERITY_MAP.get(severity, SEVERITY_MAP["none"]) if has_disease_info else {
                "color": "#10b981", "icon": "✅", "label": "Unknown"
            }

            # Choose card style
            if conf < conf_threshold:
                card_cls = "result-warning"
                icon = "🔍"
                cond_color = "#fbbf24"
                status_label = "Low Confidence"
                status_bg = "rgba(245,158,11,0.15)"
                bar_color = "#f59e0b"
            elif cond.lower() == "healthy":
                card_cls = "result-healthy"
                icon = "✅"
                cond_color = "#34d399"
                status_label = "Healthy"
                status_bg = "rgba(16,185,129,0.15)"
                bar_color = "#10b981"
            elif severity == "critical":
                card_cls = "result-critical"
                icon = "🚨"
                cond_color = "#f87171"
                status_label = "Critical — Immediate Action Needed"
                status_bg = "rgba(220,38,38,0.15)"
                bar_color = "#dc2626"
            else:
                card_cls = "result-disease"
                icon = "🔴"
                cond_color = "#f87171"
                status_label = "Disease Detected"
                status_bg = "rgba(239,68,68,0.15)"
                bar_color = "#ef4444"

            gauge_pct = int(conf * 100)

            # ── Primary result card ───────────────────────────────────────
            st.markdown(f"""
            <div class="result-card {card_cls}">
                <div class="result-icon">{icon}</div>
                <div class="result-status" style="background:{status_bg}; color:{cond_color};">
                    {status_label}
                </div>
                <div class="result-crop">{crop}</div>
                <div class="result-cond" style="color:{cond_color};">{cond}</div>
                <div class="result-conf">
                    Model confidence: <b style="color:{bar_color};">{conf:.1%}</b>
                    {f'&nbsp;·&nbsp; Severity: <b style="color:{sev_info["color"]};">{sev_info["label"]}</b>' if has_disease_info and cond.lower() != "healthy" else ""}
                </div>
                <div class="gauge-track">
                    <div class="gauge-fill" style="width:{gauge_pct}%;
                         background:linear-gradient(90deg, {bar_color}88, {bar_color});"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Add to scan history ───────────────────────────────────────
            st.session_state.scan_history.append({
                "crop": crop,
                "condition": cond,
                "confidence": conf,
                "severity": severity,
                "time": datetime.now().strftime("%H:%M"),
            })

            # ── Low confidence tip ────────────────────────────────────────
            if conf < conf_threshold:
                st.markdown("""
                <div style="color:#d97706; font-size:0.82rem; margin-top:0.6rem; padding:0.65rem 0.85rem;
                            background:rgba(245,158,11,0.05); border-radius:10px;
                            border:1px solid rgba(245,158,11,0.12);">
                    💡 <b>Tip:</b> Try a clearer, well-lit photo of a single leaf on a plain background for better accuracy.
                </div>
                """, unsafe_allow_html=True)

            # ── Disease description ───────────────────────────────────────
            if has_disease_info and disease_data.get("description"):
                st.markdown(f"""
                <div class="desc-text">{disease_data['description']}</div>
                """, unsafe_allow_html=True)

            # ── Top-K predictions ─────────────────────────────────────────
            st.markdown('<div class="section-h" style="margin-top:1.25rem;">📊 All Predictions</div>',
                        unsafe_allow_html=True)

            for rank, (n, p) in enumerate(results):
                c, d = pretty(n)
                pct = int(p * 100)
                if d.lower() == "healthy":
                    fill = "#10b981"
                elif rank == 0:
                    fill = bar_color
                else:
                    fill = "#64748b"
                delay = f"animation-delay:{rank * 0.08}s;"
                st.markdown(f"""
                <div class="pred-bar" style="{delay}">
                    <div class="pred-label">
                        <span>#{rank+1} &nbsp; {c} · {d}</span>
                        <span style="color:{fill}; font-weight:600;
                              font-family:'JetBrains Mono',monospace; font-size:0.8rem;">{p:.1%}</span>
                    </div>
                    <div class="pred-track">
                        <div class="pred-fill" style="width:{pct}%;
                             background:linear-gradient(90deg,{fill}66,{fill});"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  TREATMENT / PREVENTION SECTION (shown when disease detected)
# ═══════════════════════════════════════════════════════════════════════════════
if img is not None and 'inference_ok' in dir() and inference_ok and has_disease_info and disease_data:
    symptoms  = disease_data.get("symptoms", [])
    treatment = disease_data.get("treatment", [])
    prevention = disease_data.get("prevention", [])

    if symptoms or treatment or prevention:
        st.markdown('<div class="section-h" style="margin-top:2rem;">🩺 Treatment & Care Guide</div>',
                    unsafe_allow_html=True)

        info_cols = st.columns(3 if symptoms else 2, gap="medium")
        col_idx = 0

        if symptoms:
            with info_cols[col_idx]:
                items_html = "".join(f"<li>{s}</li>" for s in symptoms)
                st.markdown(f"""
                <div class="info-card">
                    <div class="info-card-title" style="color:#f87171;">🔍 Symptoms</div>
                    <ul class="info-list red">{items_html}</ul>
                </div>
                """, unsafe_allow_html=True)
            col_idx += 1

        if treatment:
            with info_cols[col_idx]:
                items_html = "".join(f"<li>{t}</li>" for t in treatment)
                st.markdown(f"""
                <div class="info-card">
                    <div class="info-card-title" style="color:#34d399;">💊 Treatment</div>
                    <ul class="info-list green">{items_html}</ul>
                </div>
                """, unsafe_allow_html=True)
            col_idx += 1

        if prevention:
            with info_cols[min(col_idx, len(info_cols)-1)]:
                items_html = "".join(f"<li>{p}</li>" for p in prevention)
                st.markdown(f"""
                <div class="info-card">
                    <div class="info-card-title" style="color:#0ea5e9;">🛡️ Prevention</div>
                    <ul class="info-list blue">{items_html}</ul>
                </div>
                """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  SYSTEM STATS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-h" style="margin-top:2rem;">📈 System Overview</div>',
            unsafe_allow_html=True)

m1, m2, m3, m4, m5 = st.columns(5)
stats = [
    (m1, "🦠", "38",   "Disease Classes"),
    (m2, "📸", "54K+", "Training Images"),
    (m3, "🧠", "EfficientNet", "Architecture"),
    (m4, "🎯", "99.6%", "Accuracy"),
    (m5, "📐", "224²",  "Input Resolution"),
]
for col, icon, val, label in stats:
    col.markdown(f"""
    <div class="metric">
        <div class="metric-icon">{icon}</div>
        <div class="metric-val">{val}</div>
        <div class="metric-lbl">{label}</div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  PROCESSING PIPELINE
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-h" style="margin-top:1.75rem;">🔄 Processing Pipeline</div>',
            unsafe_allow_html=True)

steps = [
    ("📷", "Upload",   "JPG / PNG / WebP"),
    ("🔲", "Resize",   "224 × 224 px"),
    ("⚡", "Scale",    "Float32 tensor"),
    ("🧠", "Backbone", "Transfer Learning"),
    ("📊", "Softmax",  "38-class probs"),
    ("🩺", "Diagnose", "Treatment plan"),
]
pcols = st.columns(len(steps))
for col, (icon, title, sub) in zip(pcols, steps):
    col.markdown(f"""
    <div class="step">
        <div class="step-icon">{icon}</div>
        <div class="step-title">{title}</div>
        <div class="step-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  DISCLAIMER & FOOTER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="disclaimer">
    <span style="font-size:1.1rem; flex-shrink:0;">⚠️</span>
    <span>
        <b>Preliminary screening only.</b> PlantVillage images use controlled backgrounds;
        accuracy on real field photos may vary. Always confirm results with a qualified
        agronomist or plant pathologist before applying treatments.
    </span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    PlantGuard AI &nbsp;·&nbsp; Built with TensorFlow / Keras &amp; Streamlit &nbsp;·&nbsp; PlantVillage Dataset
</div>
""", unsafe_allow_html=True)
