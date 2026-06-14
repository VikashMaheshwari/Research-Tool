"""Research tool page — runs the live 4-agent pipeline."""

import os
import time
import datetime

import streamlit as st
from dotenv import load_dotenv

import ui
# Reuse the existing pipeline building blocks (no logic duplicated).
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

ui.page_setup("Research")

# Shared session storage (also read by the History page).
if "history" not in st.session_state:
    st.session_state.history = []
if "result" not in st.session_state:
    st.session_state.result = None
if "preset_topic" not in st.session_state:
    st.session_state.preset_topic = ""

# --------------------------------------------------------------------------- #
# Sidebar: environment status
# --------------------------------------------------------------------------- #
load_dotenv()
groq_ok = bool(os.getenv("GROQ_API_KEY"))
tavily_ok = bool(os.getenv("TAVILY_API_KEY"))
with st.sidebar:
    st.markdown("**Environment**")
    st.markdown(("🟢" if groq_ok else "🔴") + " Groq API key", unsafe_allow_html=True)
    st.markdown(("🟢" if tavily_ok else "🔴") + " Tavily API key", unsafe_allow_html=True)
    if not (groq_ok and tavily_ok):
        st.warning("Add the missing keys to your `.env` file.")

# --------------------------------------------------------------------------- #
# Header
# --------------------------------------------------------------------------- #
st.markdown(
    """
    <div style="margin-bottom:.6rem;">
        <div class="sec-eyebrow">Research Lab</div>
        <div class="sec-title">What would you like to research?</div>
        <div class="sec-desc">Enter a topic and the agents will search, read, write and critique.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------- #
# Input form
# --------------------------------------------------------------------------- #
with st.form("research_form"):
    col_in, col_btn = st.columns([5, 1])
    with col_in:
        topic = st.text_input(
            "Research topic",
            value=st.session_state.preset_topic,
            placeholder="e.g.  Latest breakthroughs in solid-state batteries",
            label_visibility="collapsed",
        )
    with col_btn:
        submitted = st.form_submit_button("Research  →", use_container_width=True)

# Example chips
st.caption("Or try an example:")
ex_cols = st.columns(3)
examples = [
    "AI breakthroughs in 2026",
    "State of fusion energy startups",
    "How CRISPR is curing genetic disease",
]
for col, ex in zip(ex_cols, examples):
    if col.button(ex, use_container_width=True):
        st.session_state.preset_topic = ex
        st.rerun()


# --------------------------------------------------------------------------- #
# Pipeline (mirrors pipelines.run_research_pipeline, UI-aware)
# --------------------------------------------------------------------------- #
def run_pipeline_with_ui(topic: str) -> dict:
    state, timings = {}, {}
    with st.status("🚀 Spinning up the research agents…", expanded=True) as status:
        t0 = time.time()
        st.write("🔎 **Step 1/4 — Search agent** is gathering live sources…")
        search_agent = build_search_agent()
        search_result = search_agent.invoke(
            {"messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]}
        )
        state["search_results"] = search_result["messages"][-1].content
        timings["search"] = time.time() - t0

        t0 = time.time()
        st.write("📖 **Step 2/4 — Reader agent** is scraping the top source…")
        reader_agent = build_reader_agent()
        reader_result = reader_agent.invoke(
            {"messages": [(
                "user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}",
            )]}
        )
        state["scraped_content"] = reader_result["messages"][-1].content
        timings["read"] = time.time() - t0

        t0 = time.time()
        st.write("✍️ **Step 3/4 — Writer** is drafting the report…")
        research_combined = (
            f"SEARCH RESULTS : \n {state['search_results']} \n\n"
            f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
        )
        state["report"] = writer_chain.invoke({"topic": topic, "research": research_combined})
        timings["write"] = time.time() - t0

        t0 = time.time()
        st.write("🧐 **Step 4/4 — Critic** is reviewing the report…")
        state["feedback"] = critic_chain.invoke({"report": state["report"]})
        timings["critique"] = time.time() - t0

        status.update(label="✅ Research complete!", state="complete", expanded=False)

    state["topic"] = topic
    state["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    state["timings"] = timings
    return state


# --------------------------------------------------------------------------- #
# Run on submit
# --------------------------------------------------------------------------- #
if submitted:
    if not topic.strip():
        st.error("Please enter a research topic first.")
    elif not (groq_ok and tavily_ok):
        st.error("API keys are missing. Add them to your `.env` file and reload.")
    else:
        st.session_state.preset_topic = ""
        try:
            result = run_pipeline_with_ui(topic.strip())
            st.session_state.result = result
            st.session_state.history.append(result)
        except Exception as e:
            st.error(f"Pipeline failed: {e}")
            st.exception(e)

# --------------------------------------------------------------------------- #
# Results
# --------------------------------------------------------------------------- #
result = st.session_state.result
if result:
    st.write("")
    st.markdown(f"### 📌 {result['topic']}")
    st.caption(f"Generated {result['timestamp']}")

    t = result.get("timings", {})
    total = sum(t.values()) if t else 0
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total time", f"{total:.1f}s")
    m2.metric("Report length", f"{len(result['report'].split())} words")
    m3.metric("Sources scanned", str(result["search_results"].count("URL:")))
    m4.metric("Agents run", "4")

    st.write("")
    tab_report, tab_critic, tab_sources, tab_scraped = st.tabs(
        ["📄  Report", "🧐  Critic Review", "🔎  Search Results", "📖  Scraped Content"]
    )
    with tab_report:
        st.markdown(result["report"])
        st.download_button(
            "⬇️  Download report (.md)",
            data=result["report"],
            file_name=f"research_{result['topic'][:30].replace(' ', '_')}.md",
            mime="text/markdown",
        )
    with tab_critic:
        st.markdown(result["feedback"])
    with tab_sources:
        st.code(result["search_results"], language="text")
    with tab_scraped:
        st.code(result["scraped_content"], language="text")
else:
    st.write("")
    st.markdown(
        '<div class="card" style="text-align:center;color:#9aa0b5;">'
        "👋 Enter a topic above (or pick an example) and hit "
        "<b style='color:#c9bcff;'>Research →</b> to watch the agents work.</div>",
        unsafe_allow_html=True,
    )

ui.footer()
