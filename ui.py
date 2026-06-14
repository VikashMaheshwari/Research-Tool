"""
Shared UI toolkit for ResearchPilot — "Deep Teal + Aqua" edition.

Holds the colour palette, the global CSS theme + animated background graphics,
reusable HTML components so every page looks like one polished product.

Nothing here depends on the research pipeline; it is pure presentation.
"""

import streamlit as st

# --------------------------------------------------------------------------- #
# Brand
# --------------------------------------------------------------------------- #
BRAND = "ResearchPilot"
TAGLINE = "AI Research, on autopilot"

# Deep teal + aqua palette
COLORS = {
    "bg": "#06100f",
    "panel": "rgba(255,255,255,0.04)",
    "border": "rgba(45,212,191,0.16)",
    "teal": "#2dd4bf",
    "aqua": "#5eead4",
    "deep": "#0d9488",
    "text": "#eaf3f1",
    "muted": "#8fa3a0",
}


# --------------------------------------------------------------------------- #
# Global theme + animated background
# --------------------------------------------------------------------------- #
def inject_css() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&display=swap');

        :root {
            --teal:#2dd4bf; --aqua:#5eead4; --deep:#0d9488;
            --bg:#06100f; --text:#eaf3f1; --muted:#8fa3a0;
            --border:rgba(45,212,191,0.16);
        }

        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

        /* Base background: layered teal glow over near-black */
        .stApp {
            background:
                radial-gradient(1100px 700px at 10% -15%, rgba(45,212,191,0.15), transparent 55%),
                radial-gradient(900px 650px at 100% -8%, rgba(13,148,136,0.14), transparent 55%),
                radial-gradient(800px 600px at 50% 125%, rgba(94,234,212,0.07), transparent 60%),
                #06100f;
            color: var(--text);
        }

        /* Faint grid overlay (fixed, behind content) */
        .stApp::before {
            content:""; position: fixed; inset: 0; z-index: 0; pointer-events: none;
            background-image:
                linear-gradient(rgba(45,212,191,0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(45,212,191,0.05) 1px, transparent 1px);
            background-size: 46px 46px;
            mask-image: radial-gradient(circle at 50% 30%, #000 30%, transparent 80%);
            -webkit-mask-image: radial-gradient(circle at 50% 30%, #000 30%, transparent 80%);
        }

        .block-container { position: relative; z-index: 1; padding-top: 2rem; padding-bottom: 3rem; max-width: 1160px; }
        section[data-testid="stSidebar"] { z-index: 2; }
        #MainMenu, header, footer { visibility: hidden; }

        /* Floating teal orbs */
        .bg-orbs { position: fixed; inset: 0; z-index: 0; pointer-events: none; overflow: hidden; }
        .orb { position:absolute; border-radius:50%; filter: blur(70px); opacity:.42; }
        .orb.o1 { width:380px;height:380px; left:-80px; top:8%;
                  background: radial-gradient(circle, #2dd4bf, transparent 70%); animation: float1 16s ease-in-out infinite; }
        .orb.o2 { width:420px;height:420px; right:-100px; top:32%;
                  background: radial-gradient(circle, #0d9488, transparent 70%); animation: float2 20s ease-in-out infinite; }
        .orb.o3 { width:300px;height:300px; left:38%; bottom:-90px;
                  background: radial-gradient(circle, #5eead4, transparent 70%); animation: float1 24s ease-in-out infinite; opacity:.3; }
        @keyframes float1 { 0%,100%{transform:translateY(0) translateX(0);} 50%{transform:translateY(-32px) translateX(18px);} }
        @keyframes float2 { 0%,100%{transform:translateY(0) translateX(0);} 50%{transform:translateY(26px) translateX(-22px);} }

        /* ---------- Hero ---------- */
        .hero { text-align: center; padding: 1rem 0 0.2rem; }
        .wordmark { font-size: 1.3rem; font-weight: 800; letter-spacing:.3px; color: var(--aqua); margin-bottom:.8rem; }
        .badge {
            display:inline-block; padding:6px 15px; border-radius:999px;
            background: rgba(45,212,191,0.12); border:1px solid rgba(45,212,191,0.4);
            color: var(--aqua); font-size:.76rem; font-weight:700; letter-spacing:.7px; margin-bottom:1.1rem;
        }
        .hero h1 {
            font-family:'Fraunces', serif; font-size:3.4rem; font-weight:700; line-height:1.07; margin:0;
            background: linear-gradient(100deg,#fff 6%, #5eead4 55%, #0d9488 100%);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent;
        }
        .hero .sub { color: var(--muted); font-size:1.13rem; margin:1rem auto 0; max-width:640px; }

        /* ---------- Section headers ---------- */
        .sec-eyebrow { text-transform:uppercase; letter-spacing:2.2px; font-size:.75rem; font-weight:800; color: var(--teal); }
        .sec-title { font-family:'Fraunces', serif; font-size:2rem; font-weight:600; margin:.25rem 0 .3rem; color:#eefbf8; }
        .sec-desc { color: var(--muted); font-size:1rem; }

        /* ---------- Cards ---------- */
        .card {
            background: rgba(255,255,255,0.035); border:1px solid var(--border);
            border-radius:18px; padding:1.3rem 1.4rem; height:100%;
            transition: transform .15s ease, border-color .15s ease, box-shadow .15s ease;
        }
        .card:hover { transform: translateY(-4px); border-color: rgba(45,212,191,0.55);
                      box-shadow: 0 20px 45px -24px rgba(45,212,191,0.55); }
        .icon-badge {
            display:inline-flex; align-items:center; justify-content:center;
            width:46px; height:46px; border-radius:13px; font-size:1.4rem;
            background: linear-gradient(135deg, rgba(45,212,191,.26), rgba(13,148,136,.16));
            border:1px solid rgba(45,212,191,0.3); margin-bottom:.8rem;
        }
        .card h3 { font-size:1.08rem; font-weight:700; margin:0 0 .3rem; color:#eefbf8; }
        .card p { color: var(--muted); font-size:.9rem; margin:0; line-height:1.55; }

        /* ---------- Step rail ---------- */
        .step-row { display:flex; gap:12px; flex-wrap:wrap; }
        .step { flex:1 1 0; min-width:150px; background: rgba(255,255,255,0.03);
                border:1px solid var(--border); border-radius:16px; padding:16px; }
        .step .num { display:inline-flex; align-items:center; justify-content:center; width:30px; height:30px;
                     border-radius:9px; font-weight:800; font-size:.9rem;
                     background: linear-gradient(135deg, var(--teal), var(--deep)); color:#04231f; margin-bottom:10px; }
        .step .t { font-weight:700; color:#eefbf8; }
        .step .d { color: var(--muted); font-size:.83rem; margin-top:3px; }

        /* ---------- Stats ---------- */
        .stat { text-align:center; padding:1rem; }
        .stat .v { font-family:'Fraunces',serif; font-size:2.1rem; font-weight:700;
                   background: linear-gradient(120deg,#5eead4,#0d9488);
                   -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
        .stat .l { color: var(--muted); font-size:.85rem; }

        /* ---------- Quote / testimonial ---------- */
        .quote { background: rgba(255,255,255,0.035); border:1px solid var(--border);
                 border-radius:18px; padding:1.3rem 1.4rem; height:100%; }
        .quote p { color:#dcefeb; font-size:.96rem; line-height:1.6; font-style:italic; }
        .quote .who { margin-top:.8rem; color: var(--aqua); font-weight:700; font-size:.88rem; }
        .quote .role { color: var(--muted); font-size:.8rem; }

        /* ---------- Inputs ---------- */
        .stTextInput > div > div > input, .stTextArea textarea {
            background: rgba(255,255,255,0.04) !important; border:1px solid rgba(45,212,191,0.22) !important;
            border-radius:12px !important; color:#fff !important; font-size:1rem; }
        .stTextInput > div > div > input { height:3rem; }
        .stTextInput > div > div > input:focus, .stTextArea textarea:focus {
            border-color: var(--teal) !important; box-shadow:0 0 0 3px rgba(45,212,191,0.25) !important; }

        /* ---------- Buttons ---------- */
        .stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {
            background: linear-gradient(135deg, var(--teal), var(--deep));
            color:#04231f; border:0; border-radius:12px; font-weight:800; height:3rem;
            transition: filter .15s ease, transform .15s ease; }
        .stButton > button:hover, .stDownloadButton > button:hover, .stFormSubmitButton > button:hover {
            filter: brightness(1.08); transform: translateY(-1px); color:#04231f; }

        /* ---------- Tabs ---------- */
        .stTabs [data-baseweb="tab-list"] { gap:6px; }
        .stTabs [data-baseweb="tab"] { background: rgba(255,255,255,0.03); border-radius:10px 10px 0 0;
                                       padding:8px 16px; color: var(--muted); }
        .stTabs [aria-selected="true"] { background: rgba(45,212,191,0.16) !important; color:#eefbf8 !important; }

        /* ---------- Metrics ---------- */
        div[data-testid="stMetric"] { background: rgba(255,255,255,0.035); border:1px solid var(--border);
                                      border-radius:14px; padding:12px 16px; }

        /* ---------- Sidebar ---------- */
        section[data-testid="stSidebar"] { background:#07120f; border-right:1px solid var(--border); }
        section[data-testid="stSidebar"] .block-container { padding-top:1.5rem; }

        /* ---------- Footer / pills ---------- */
        .footer { margin-top:3rem; padding-top:1.4rem; border-top:1px solid var(--border);
                  color:#7e918e; font-size:.85rem; display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px; }
        .pill { display:inline-block; padding:4px 11px; border-radius:999px; font-size:.75rem;
                background: rgba(45,212,191,0.08); border:1px solid rgba(45,212,191,0.22); color:#bfe6df; margin:2px 4px 2px 0; }
        .logo-strip { display:flex; gap:26px; justify-content:center; flex-wrap:wrap; opacity:.6;
                      color:#b6d7d1; font-weight:700; letter-spacing:.5px; font-size:1rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_background() -> None:
    """Floating animated teal orbs behind the page content."""
    st.markdown(
        '<div class="bg-orbs"><div class="orb o1"></div>'
        '<div class="orb o2"></div><div class="orb o3"></div></div>',
        unsafe_allow_html=True,
    )


def page_setup(title: str, icon: str = "🧠") -> None:
    """Call at the top of every page (after navigation runs set_page_config)."""
    inject_css()
    render_background()


# --------------------------------------------------------------------------- #
# Reusable components
# --------------------------------------------------------------------------- #
def sidebar_brand() -> None:
    st.sidebar.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:.4rem;">
            <div class="icon-badge" style="width:38px;height:38px;font-size:1.1rem;margin:0;">🧭</div>
            <div>
                <div style="font-weight:800;font-size:1.15rem;color:#eefbf8;">{BRAND}</div>
                <div style="font-size:.72rem;color:#8fa3a0;">{TAGLINE}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(eyebrow: str, title: str, desc: str = "") -> None:
    st.markdown(
        f"""
        <div style="margin:1.6rem 0 1rem;">
            <div class="sec-eyebrow">{eyebrow}</div>
            <div class="sec-title">{title}</div>
            {f'<div class="sec-desc">{desc}</div>' if desc else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def feature_card(icon: str, title: str, desc: str) -> str:
    return (f'<div class="card"><div class="icon-badge">{icon}</div>'
            f"<h3>{title}</h3><p>{desc}</p></div>")


def quote_card(text: str, who: str, role: str) -> str:
    return (f'<div class="quote"><p>“{text}”</p>'
            f'<div class="who">{who}</div><div class="role">{role}</div></div>')


def footer() -> None:
    st.markdown(
        f"""
        <div class="footer">
            <div>© 2026 {BRAND} · {TAGLINE}</div>
            <div>Built with Streamlit · LangChain · Groq · Tavily</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
