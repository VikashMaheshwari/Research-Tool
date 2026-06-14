"""My Reports — browse and download past research from this session."""

import streamlit as st
import ui

ui.page_setup("My Reports")

if "history" not in st.session_state:
    st.session_state.history = []

st.markdown(
    """
    <div style="margin-bottom:.6rem;">
        <div class="sec-eyebrow">Library</div>
        <div class="sec-title">📚 My Reports</div>
        <div class="sec-desc">Every report you generate this session is saved here.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

history = st.session_state.history

if not history:
    st.markdown(
        '<div class="card" style="text-align:center;color:#9aa0b5;">'
        "No reports yet. Head to the <b style='color:#c9bcff;'>Research</b> page to create your first one.</div>",
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("Go to Research  →", use_container_width=True):
            st.switch_page("views/research.py")
else:
    # Summary stats
    total_words = sum(len(h["report"].split()) for h in history)
    s1, s2 = st.columns(2)
    s1.metric("Reports created", str(len(history)))
    s2.metric("Total words written", f"{total_words:,}")
    st.write("")

    # Toolbar
    top = st.columns([3, 1])
    with top[1]:
        if st.button("🗑️ Clear all", use_container_width=True):
            st.session_state.history = []
            st.session_state.result = None
            st.rerun()

    # Newest first
    for i, h in enumerate(reversed(history)):
        with st.expander(f"📌 {h['topic']}   ·   {h['timestamp']}", expanded=(i == 0)):
            words = len(h["report"].split())
            sources = h["search_results"].count("URL:")
            st.caption(f"{words} words · {sources} sources scanned")

            tabs = st.tabs(["📄 Report", "🧐 Critic", "🔎 Sources"])
            with tabs[0]:
                st.markdown(h["report"])
            with tabs[1]:
                st.markdown(h["feedback"])
            with tabs[2]:
                st.code(h["search_results"], language="text")

            st.download_button(
                "⬇️ Download (.md)",
                data=h["report"],
                file_name=f"research_{h['topic'][:30].replace(' ', '_')}.md",
                mime="text/markdown",
                key=f"dl_{i}",
            )

ui.footer()
