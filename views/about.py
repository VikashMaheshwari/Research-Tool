"""About — explains the agents, the tech stack, and answers FAQs."""

import streamlit as st
import ui

ui.page_setup("About")

st.markdown(
    f"""
    <div class="hero" style="padding-top:.4rem;">
        <span class="badge">ABOUT THE PROJECT</span>
        <h1 style="font-size:2.6rem;">Meet the {ui.BRAND} team of agents</h1>
        <div class="sub">A multi-agent research system that turns a single question into a
        sourced, reviewed report — built with LangChain, Groq and Tavily.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------- #
# The agents
# --------------------------------------------------------------------------- #
ui.section_header("The crew", "Four agents, one mission")

a1, a2 = st.columns(2)
a1.markdown(
    ui.feature_card("🔎", "Search Agent",
                    "Decides what to search for and queries the live web through Tavily, "
                    "returning the most recent and reliable sources."),
    unsafe_allow_html=True,
)
a2.markdown(
    ui.feature_card("📖", "Reader Agent",
                    "Picks the single most relevant URL from the search results and scrapes "
                    "its full text with BeautifulSoup for real depth."),
    unsafe_allow_html=True,
)
st.write("")
a3, a4 = st.columns(2)
a3.markdown(
    ui.feature_card("✍️", "Writer Chain",
                    "An LCEL chain that turns the gathered research into a structured report: "
                    "introduction, key findings, conclusion and sources."),
    unsafe_allow_html=True,
)
a4.markdown(
    ui.feature_card("🧐", "Critic Chain",
                    "Reviews the finished report, assigns a score out of 10, and lists "
                    "strengths and areas to improve."),
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------- #
# Tech stack
# --------------------------------------------------------------------------- #
ui.section_header("Under the hood", "Built with a modern, lightweight stack")
st.markdown(
    """
    <div>
        <span class="pill">🐍 Python</span>
        <span class="pill">🎈 Streamlit</span>
        <span class="pill">🦜 LangChain (LCEL)</span>
        <span class="pill">⚡ Groq · Llama 3.1</span>
        <span class="pill">🔎 Tavily Search</span>
        <span class="pill">🍲 BeautifulSoup</span>
        <span class="pill">🔐 python-dotenv</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------- #
# FAQ
# --------------------------------------------------------------------------- #
ui.section_header("FAQ", "Good to know")

with st.expander("Where do the results come from?"):
    st.write(
        "The search agent uses Tavily to fetch live web results, and the reader agent "
        "scrapes the most relevant page directly. Reports reflect current web content, "
        "not just a model's training data."
    )
with st.expander("Are my reports saved permanently?"):
    st.write(
        "Reports are kept in your **My Reports** library for the current session. Use the "
        "download button to save any report as a Markdown file on your computer."
    )
with st.expander("What do I need to run it?"):
    st.write(
        "A Groq API key and a Tavily API key in a `.env` file at the project root:\n\n"
        "```\nGROQ_API_KEY=your_key\nTAVILY_API_KEY=your_key\n```\n\n"
        "Then run `streamlit run app.py`."
    )
with st.expander("Can I change the AI model?"):
    st.write(
        "Yes — the model is configured in `agents.py` (`ChatGroq(model_name=...)`). "
        "Swap it for any model your Groq account supports."
    )

st.write("")
cc1, cc2, cc3 = st.columns([1, 1, 1])
with cc2:
    if st.button("Try it now  →", use_container_width=True):
        st.switch_page("views/research.py")

ui.footer()
