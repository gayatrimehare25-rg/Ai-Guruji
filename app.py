import os
import streamlit as st
import google.generativeai as genai
# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(page_title="AI Guruji - Student Assistant", page_icon="💡")

# Header Section
st.title("📚 AI Guruji:Smart Study Assistant ")
st.write("Your trusted AI Guru for complete study support. !")

# Initialize Gemini Client
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Dropdown for Academic Tasks
task_type = st.selectbox(
    " Select Type of Problem ",
    [
        "Solve a Doubt / Question (Step-by-Step)",
        "Explain Topic Simply (ELI5 Mode)",
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
if st.button("Search "):
    if not user_input.strip():
        st.warning("Please Enter Your Doubt !")
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

                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=full_prompt,
                    config={
                        'temperature': temperature,
                        'max_output_tokens': 4000
                    }
                )
                
                st.success("Done ")
                st.markdown(response.text)
        except Exception as e:
            st.error(f"Error: {e}")