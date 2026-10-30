
import os
import streamlit as st
from groq import Groq
from ddgs import DDGS

# Page Configuration
st.set_page_config(
    page_title="Task-Automation Agent",
    page_icon="🤖",
    layout="centered"
)

# App Title
st.title("🤖 Task-Automation Agent (Web Search + Summarize)")
st.write(
    "Enter a topic to automatically search the web "
    "and generate a 3-bullet-point research brief."
)

# User Input
topic = st.text_input(
    "Enter Topic:",
    "Latest developments in Artificial Intelligence 2026"
)

# Generate Brief Button
if st.button("Generate Brief"):

    if not topic.strip():
        st.warning("Please enter a valid topic.")

    else:
        groq_api_key = os.environ.get("GROQ_API_KEY")

        if not groq_api_key:
            st.error("GROQ_API_KEY is missing. Configure it first.")

        else:

            # Stage 1: Web Search
            with st.spinner("Stage 1: Searching the web..."):

                try:
                    with DDGS() as ddgs:
                        results = list(
                            ddgs.text(topic, max_results=5)
                        )

                    research_text = "\n\n".join(
                        f"Title: {r.get('title', '')}\n"
                        f"Snippet: {r.get('body', '')}\n"
                        f"URL: {r.get('href', '')}"
                        for r in results
                    )

                    if not research_text.strip():
                        st.error("No search results found. Try another topic.")
                        st.stop()

                except Exception as e:
                    st.error(f"Web search failed: {e}")
                    st.stop()

            # Stage 2: AI Summarization
            with st.spinner("Stage 2: Summarizing search results..."):

                try:
                    client = Groq(api_key=groq_api_key)

                    response = client.chat.completions.create(
                        model="openai/gpt-oss-20b",

                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are a research assistant. "
                                    "Summarize the supplied research into "
                                    "exactly 3 concise bullet points. "
                                    "Use only the supplied evidence. "
                                    "Do not invent facts."
                                )
                            },
                            {
                                "role": "user",
                                "content": (
                                    f"Topic: {topic}\n\n"
                                    f"Research Results:\n{research_text}"
                                )
                            }
                        ],

                        temperature=0.2,
                        max_completion_tokens=1000
                    )

                    brief = response.choices[0].message.content

                    if brief and brief.strip():

                        st.success("Workflow completed successfully!")

                        st.markdown("### 📋 Final Research Brief")

                        st.markdown(brief)

                    else:
                        st.error(
                            "Groq returned an empty response. "
                            "Please try again."
                        )

                except Exception as e:
                    st.error(f"Error during summarization: {e}")
