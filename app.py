
import streamlit as st

from agent import research, generate_research_report


# ==========================================
# 1. Page Configuration
# ==========================================

st.set_page_config(
    page_title="Research Assistant Agent",
    page_icon="🔎",
    layout="centered"
)


# ==========================================
# 2. Custom CSS
# ==========================================

st.markdown(
    """
    <style>

    /* Center the main content */
    .main .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 3rem;
        margin: auto;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# 3. Application Header
# ==========================================

st.title("🔎 Research Assistant Agent")

st.markdown(
    """
    An AI-powered research assistant that searches the web,
    extracts relevant content, summarizes individual sources,
    and generates a research report with source links.
    """
)

st.divider()


# ==========================================
# 4. User Input
# ==========================================

st.subheader("Research Topic")

topic = st.text_input(
    "Enter your research topic:",
    placeholder="e.g. AI Agents for Data Science"
)

max_results = st.slider(
    "Maximum number of search results",
    min_value=1,
    max_value=10,
    value=3
)


# ==========================================
# 5. Research Execution
# ==========================================

if st.button(
    "Start Research",
    type="primary",
    use_container_width=True
):

    if not topic.strip():

        st.warning("Please enter a research topic.")

    else:

        # Clear previous results
        st.session_state.pop("report", None)
        st.session_state.pop("sources", None)
        st.session_state.pop("topic", None)

        try:

            with st.spinner(
                "Searching the web and processing sources..."
            ):

                # Step 1: Search and summarize sources
                sources = research(
                    topic,
                    max_results=max_results
                )

                if not sources:

                    st.warning(
                        "No sources were successfully processed. "
                        "Please try another topic."
                    )

                else:

                    # Step 2: Generate the research report
                    report = generate_research_report(
                        topic,
                        sources
                    )

                    # Step 3: Store results
                    st.session_state["report"] = report
                    st.session_state["sources"] = sources
                    st.session_state["topic"] = topic

        except Exception as e:

            st.error(f"An error occurred: {e}")


# ==========================================
# 6. Display Research Report
# ==========================================

if "report" in st.session_state:

    st.divider()

    st.subheader("📄 Research Report")

    st.markdown(
        st.session_state["report"]
    )


    # ======================================
    # 7. Display Research Sources
    # ======================================

    st.divider()

    st.subheader("🔗 Research Sources")

    for i, source in enumerate(
        st.session_state["sources"],
        start=1
    ):

        st.markdown(
            f"{i}. [{source['title']}]({source['url']})"
        )
