import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import datetime

# ✅ Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("🚨 GEMINI_API_KEY not found in .env file.")
    st.stop()

genai.configure(api_key=api_key)

# ✅ Set model (you can change it based on available models from genai.list_models())
model = genai.GenerativeModel('gemini-2.0-flash')

# ✅ Streamlit Page Settings
st.set_page_config(page_title="Mental Wellness Reflection Bot", page_icon="🧘", layout="wide")

# ✅ Sidebar Details
st.sidebar.title("🧘 Mental Wellness Reflection Bot")
st.sidebar.markdown("""
**💡 Project Purpose**  
AI-powered mental wellness reflection assistant.

**🌍 UN SDG Alignment**  
Supports Goal 3: Good Health and Well-Being

**🛠️ How It Works**  
- Gemini AI Model  
- Reflection journaling  
- Personalized feedback

**⚠️ Limitations**  
- Suggestions only  
- Not a substitute for therapy

**💡 Tips**  
- Be honest  
- Write clearly  
- Use daily for best results
""")

# ✅ Initialize Session State
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

if "response_text" not in st.session_state:
    st.session_state.response_text = ""

if "journal_entries" not in st.session_state:
    st.session_state.journal_entries = []

# ✅ Reflection Questions
reflection_questions = [
    "How are you feeling today emotionally?",
    "What’s one thing you're grateful for today?",
    "What challenges did you face recently?",
    "What positive thing happened today?",
    "What helps you relax when you feel stressed?"
]

# ✅ Layout
st.title("🧘 Mental Wellness Reflection Bot")

selected_question = st.selectbox("💬 Choose a Reflection Prompt:", reflection_questions)

st.subheader("Write Your Reflection")
st.session_state.user_input = st.text_area("Write here:", value=st.session_state.user_input, height=150)

st.subheader("Choose Feedback Style")
feedback_style = st.radio("Feedback tone:", ["Gentle & Encouraging", "Action-Oriented", "Deep Reflection & Insight"])

# ✅ Action Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("✨ Get Personalized Feedback"):
        if st.session_state.user_input.strip() == "":
            st.warning("Please write something before clicking the button.")
        else:
            prompt = (
                f"You are a mental wellness coach. Provide {feedback_style.lower()} feedback "
                f"for this reflection:\n\n{st.session_state.user_input}"
            )
            with st.spinner("Generating feedback..."):
                try:
                    response = model.generate_content(prompt)
                    st.session_state.response_text = response.text

                    # Save to journal
                    st.session_state.journal_entries.append({
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'question': selected_question,
                        'reflection': st.session_state.user_input,
                        'feedback_style': feedback_style,
                        'feedback': response.text
                    })

                except Exception as e:
                    st.error(f"Error generating feedback: {e}")

with col2:
    if st.button("🔄 Clear Reflection & Start Over"):
        st.session_state.user_input = ""
        st.session_state.response_text = ""
        st.rerun()

# ✅ Show Feedback
if st.session_state.response_text:
    st.subheader("Your Feedback")
    st.write(st.session_state.response_text)

# ✅ Journal History
st.subheader("Reflection Journal 📖")
if st.session_state.journal_entries:
    for entry in reversed(st.session_state.journal_entries):
        with st.expander(f"{entry['timestamp']} – {entry['question'][:50]}..."):
            st.write(f"**Reflection:** {entry['reflection']}")
            st.write(f"**Feedback Style:** {entry['feedback_style']}")
            st.write(f"**Feedback:** {entry['feedback']}")
else:
    st.info("No journal entries yet.")
