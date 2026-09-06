```python
import os
import time
import streamlit as st
from google import genai
from google.genai import types

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Guruji - Student Assistant",
    page_icon="💡",
    layout="centered"
)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("📚 AI Guruji: Smart Study Assistant")
st.write("Your trusted AI Guru for complete study support!")

# --------------------------------------------------
# API Key
# --------------------------------------------------

api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error(
        "❌ API Key missing! Please add GEMINI_API_KEY "
        "in Streamlit Secrets."
    )
    st.stop()

# --------------------------------------------------
# Gemini Client
# --------------------------------------------------

client = genai.Client(api_key=api_key)

# --------------------------------------------------
# Academic Task
# --------------------------------------------------

task_type = st.selectbox(
    "Select Type of Problem",
    [
        "Solve a Doubt / Question (Step-by-Step)",
        "Explain Topic Simply",
        "Summarize Notes & Generate Exam Questions",
        "Create Study Plan from Syllabus"
    ]
)

# --------------------------------------------------
# User Input
# --------------------------------------------------

user_input = st.text_area(
    "Ask Your Doubt:",
    height=150,
    placeholder="Example: Explain operating system in simple language..."
)

# --------------------------------------------------
# Sidebar Settings
# --------------------------------------------------

st.sidebar.header("⚙️ Guruji Settings")

temperature = st.sidebar.slider(
    "Creativity / Explanation Style:",
    min_value=0.0,
    max_value=1.0,
    value=0.3,
    step=0.1
)

# --------------------------------------------------
# Generate Answer
# --------------------------------------------------

if st.button("🔍 Search", use_container_width=True):

    if not user_input.strip():
        st.warning("⚠️ Please enter your doubt!")
        st.stop()

    try:

        with st.spinner("🤔 AI Guruji is thinking..."):

            system_instruction = f"""
You are AI Guruji, a friendly and highly capable academic
mentor for college students.

The student needs help with:
{task_type}

Your job is to:
- Explain concepts clearly
- Use simple student-friendly language
- Give step-by-step explanations
- Use bullet points wherever useful
- Give examples
- Highlight important exam points
- Avoid unnecessary complicated language
- If the question is mathematical or programming-related,
  show the solution step-by-step
"""

            full_prompt = f"""
{system_instruction}

Student Query:
{user_input}
"""

            # --------------------------------------------------
            # Gemini Model
            # --------------------------------------------------

            response = None

            # Primary model
            models_to_try = [
                "gemini-2.5-flash",
                "gemini-2.5-flash-lite"
            ]

            last_error = None

            # --------------------------------------------------
            # Retry + Fallback
            # --------------------------------------------------

            for model_name in models_to_try:

                for attempt in range(3):

                    try:

                        response = client.models.generate_content(
                            model=model_name,
                            contents=full_prompt,
                            config=types.GenerateContentConfig(
                                temperature=temperature
                            )
                        )

                        # If successful, stop retrying
                        if response and response.text:
                            break

                    except Exception as e:

                        last_error = e

                        # Wait before retrying
                        if attempt < 2:
                            time.sleep(2)

                # If successful, stop trying other models
                if response and response.text:
                    break

            # --------------------------------------------------
            # Display Response
            # --------------------------------------------------

            if response and response.text:

                st.success("✅ Done!")
                st.markdown(response.text)

            else:

                st.error(
                    "❌ Gemini is currently unavailable. "
                    "Please try again after a few seconds."
                )

                if last_error:
                    st.code(str(last_error))

    except Exception as e:

        st.error("❌ Gemini API Error")
        st.code(str(e))
```
