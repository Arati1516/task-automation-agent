 import os
import streamlit as st
from langchain_groq import ChatGroq
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
        # Get API key from environment (Secure MLOps practice)
        groq_api_key = os.environ.get("GROQ_API_KEY")
        
        if not groq_api_key:
            st.error("GROQ_API_KEY environment variable is missing! Please configure it.")
        else:
            with st.spinner(f"Stage 1: Searching the web for '{topic}'..."):
                try:
                    search = DuckDuckGoSearchRun()
                    search_data = search.run(topic)
                except Exception as e:
                    search_data = f"Latest updates regarding {topic}."
            
            with st.spinner("Stage 2: Summarizing search results using LLM..."):
                try:
                    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0, api_key=groq_api_key)
                    prompt = f"Topic: {topic}\nSearch Results: {search_data}\n\nTask: Provide a concise research brief of exactly three bullet points summarizing the key findings."
                    
                    response = llm.invoke(prompt)
                    brief = response.content
                    
                    st.success("Workflow completed successfully!")
                    st.markdown("### 📋 Final Research Brief")
                    st.markdown(brief)
                except Exception as e:
                    st.error(f"Error during summarization: {e}")