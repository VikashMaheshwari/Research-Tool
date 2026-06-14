"""Home / landing page — product marketing front door."""

import streamlit as st
import ui

ui.page_setup("Home")

# --------------------------------------------------------------------------- #
# Hero
# --------------------------------------------------------------------------- #
st.markdown(
    f"""
    <div class="hero">
        <div class="wordmark">🧭 {ui.BRAND}</div>
        <span class="badge">⚡ MULTI-AGENT · LIVE WEB RESEARCH</span>
        <h1>Research anything.<br>Get a sourced report in seconds.</h1>
        <div class="sub">Four specialised AI agents search the live web, read the best
        source, write a structured report, and critique it — so you don't have to.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")
c1, c2, c3 = st.columns([1, 1.2, 1])
with c2:
    if st.button("🚀  Start researching free", use_container_width=True):
        st.switch_page("views/research.py")

st.write("")
st.write("")

# --------------------------------------------------------------------------- #
# Stats
# --------------------------------------------------------------------------- #
s1, s2, s3, s4 = st.columns(4)
for col, val, lab in [
    (s1, "4", "AI agents"),
    (s2, "~30s", "Avg. report time"),
    (s3, "Live", "Web sources"),
    (s4, "100%", "Cited output"),
]:
    col.markdown(f'<div class="stat"><div class="v">{val}</div><div class="l">{lab}</div></div>',
                 unsafe_allow_html=True)

# --------------------------------------------------------------------------- #
# Features
# --------------------------------------------------------------------------- #
ui.section_header("Why ResearchPilot",
                  "Everything you need for fast, trustworthy research",
                  "A complete pipeline — not just a chatbot. Each agent has one job and does it well.")

f1, f2, f3 = st.columns(3)
f1.markdown(ui.feature_card("🔎", "Live web search",
            "Pulls recent, reliable sources with Tavily — never stale training data."), unsafe_allow_html=True)
f2.markdown(ui.feature_card("📖", "Deep reading",
            "Scrapes the single most relevant page for real depth, not just snippets."), unsafe_allow_html=True)
f3.markdown(ui.feature_card("✍️", "Structured writing",
            "Drafts a clean report: intro, key findings, conclusion, and sources."), unsafe_allow_html=True)
st.write("")
f4, f5, f6 = st.columns(3)
f4.markdown(ui.feature_card("🧐", "Built-in critic",
            "A reviewer agent scores the report and flags weak spots automatically."), unsafe_allow_html=True)
f5.markdown(ui.feature_card("📚", "Saved library",
            "Every report is kept in your account so you can revisit and download it."), unsafe_allow_html=True)
f6.markdown(ui.feature_card("⚡", "Fast & private",
            "Runs on Groq for near-instant generation, right from your own machine."), unsafe_allow_html=True)

# --------------------------------------------------------------------------- #
# How it works
# --------------------------------------------------------------------------- #
ui.section_header("How it works", "From question to report in four steps")
st.markdown(
    """
    <div class="step-row">
        <div class="step"><div class="num">1</div><div class="t">🔎 Search</div>
            <div class="d">The search agent finds the best live sources on your topic.</div></div>
        <div class="step"><div class="num">2</div><div class="t">📖 Read</div>
            <div class="d">The reader agent scrapes the top page for deeper content.</div></div>
        <div class="step"><div class="num">3</div><div class="t">✍️ Write</div>
            <div class="d">The writer turns the research into a structured report.</div></div>
        <div class="step"><div class="num">4</div><div class="t">🧐 Critique</div>
            <div class="d">The critic scores and reviews the finished report.</div></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------- #
# Testimonials
# --------------------------------------------------------------------------- #
ui.section_header("Loved by researchers", "What people are saying")
t1, t2, t3 = st.columns(3)
t1.markdown(ui.quote_card(
    "I used to spend an afternoon on background research. ResearchPilot gets me 80% there in under a minute.",
    "Aisha R.", "Market Analyst"), unsafe_allow_html=True)
t2.markdown(ui.quote_card(
    "The critic agent is the killer feature — it catches weak claims before I send anything to my team.",
    "Daniel K.", "Founder"), unsafe_allow_html=True)
t3.markdown(ui.quote_card(
    "Sourced, structured, and fast. It's become the first tab I open when I start a new topic.",
    "Maria L.", "PhD Student"), unsafe_allow_html=True)

# --------------------------------------------------------------------------- #
# Final CTA
# --------------------------------------------------------------------------- #
st.write("")
st.markdown(
    """
    <div class="card" style="text-align:center;background:
        linear-gradient(135deg, rgba(232,182,90,0.18), rgba(200,146,47,0.08));">
        <h3 style="font-family:'Fraunces',serif;font-size:1.6rem;">Ready to dig in?</h3>
        <p style="font-size:1rem;">Pick a topic and let the agents do the heavy lifting.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
cc1, cc2, cc3 = st.columns([1, 1, 1])
with cc2:
    if st.button("Open the Research Lab  →", use_container_width=True, key="cta_bottom"):
        st.switch_page("views/research.py")

ui.footer()
