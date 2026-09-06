import os
import streamlit as st
from google import genai

# Page Configuration
st.set_page_config(page_title="AI Guruji - Student Assistant", page_icon="💡")

# Header Section
st.title("📚 AI Guruji: Smart Study Assistant")
st.write("Your trusted AI Guru for complete study support!")

# API Key handling for both Local & Streamlit Cloud
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("API Key missing! Please set GEMINI_API_KEY in Streamlit Secrets.")
else:
    # Initialize Gemini Client
    from google.genai.types import HttpOptions

client = genai.Client(api_key=api_key, http_options=HttpOptions(api_version="v1"))

    # Dropdown for Academic Tasks
    task_type = st.selectbox(
        "Select Type of Problem",
        [
            "Solve a Doubt / Question (Step-by-Step)",
            "Explain Topic Simply",
            "Summarize Notes & Generate Exam Questions",
            "Create Study Plan from Syllabus"
        ]
    )

    # User Input Area
    user_input = st.text_area("Ask Your Doubt:", height=150)

    # Sidebar Settings
    st.sidebar.header("Guruji Settings")
    temperature = st.sidebar.slider("Creativity / Explanation Style:", 0.0, 1.0, 0.3)

    # Action Button
    if st.button("Search"):
        if not user_input.strip():
            st.warning("Please Enter Your Doubt!")
        else:
            try:
                with st.spinner("Please Wait..."):
                    # Custom System Instruction for AI Guruji
                    system_instruction = (
                        f"You are 'AI Guruji', a friendly, wise, and highly capable academic mentor for students. "
                        f"The student needs help with: '{task_type}'. "
                        "Provide accurate, clear, step-by-step explanations using student-friendly language, bullet points, and clean formatting."
                    )
                    
                    full_prompt = f"{system_instruction}\n\nStudent Query:\n{user_input}"

                    # Primary attempt on gemini-2.5-flash, fallback to gemini-1.5-flash if quota hits
                    try:
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=full_prompt,
                        )
                    except Exception:
                        response = client.models.generate_content(
                            model='gemini-1.5-flash',
                            contents=full_prompt,
                        )
                    
                    st.success("Done!")
                    st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {e}")