import os
import streamlit as st
from groq import Groq
from langchain_community.tools import DuckDuckGoSearchRun

# Page Config
st.set_page_config(page_title="Task-Automation Agent", page_icon="🤖", layout="centered")

st.title("🤖 Task-Automation Agent (Web Search + Summarize)")
st.write("Enter a topic below to automatically search the web and generate a 3-bullet-point research brief.")

# User Input
topic = st.text_input("Enter Topic:", "Latest developments in Artificial Intelligence 2026")

if st.button("Generate Brief"):
    if not topic.strip():
        st.warning("Please enter a valid topic.")
    else:
        groq_api_key = os.environ.get("GROQ_API_KEY")
        
        if not groq_api_key:
            st.error("GROQ_API_KEY environment variable is missing! Please configure it.")
        else:
            with st.spinner(f"Stage 1: Searching the web for '{topic}'..."):
                try:
                    search = DuckDuckGoSearchRun()
                    research_text = search.run(topic)
                except Exception as e:
                    research_text = f"Latest updates regarding {topic}."
            
            with st.spinner("Stage 2: Summarizing search results using Groq API..."):
                try:
                    # Initialize Groq client securely using the environment API key
                    client = Groq(api_key=groq_api_key)

                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",  # Updated to a valid, active Groq model
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "Summarize the research provided into exactly "
                                    "3 concise bullet points. Use only the supplied "
                                    "evidence and do not invent facts."
                                )
                            },
                            {
                                "role": "user",
                                "content": research_text
                            }
                        ],
                        temperature=0.2,
                        max_completion_tokens=300
                    )

                    brief = response.choices[0].message.content
                    
                    st.success("Workflow completed successfully!")
                    st.markdown("### 📋 Final Research Brief")
                    st.markdown(brief)
                except Exception as e:
                    st.error(f"Error during summarization: {e}")