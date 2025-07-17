import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import random # Import for random question selection

# Load environment variables
load_dotenv()

# Configure the Generative AI model
# It's good practice to check if the API key is available
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("GEMINI_API_KEY not found. Please set it in your .env file.")
    st.stop() # Stop the app if the API key is missing

genai.configure(api_key=api_key)

# Initialize the Generative Model. Using a more specific model for chat might be beneficial.
# For general reflection, 'gemini-pro' is fine. If you wanted more conversational turns,
# you might consider a chat-optimized model if available or set up chat history.
model = genai.GenerativeModel('gemini-pro')

# --- Streamlit App ---
st.set_page_config(page_title="🧘 Mental Wellness Reflection Bot", layout="centered")

st.title("🧘 Mental Wellness Reflection Bot")
st.markdown("### Your daily companion for mindful reflection and gentle insights.")

# Reflection Questions - Added variety and a 'random' option
reflection_questions = [
    "How are you feeling today emotionally?",
    "What’s one thing you're grateful for today?",
    "What challenges did you face recently, and how did you navigate them?",
    "What positive thing happened today, big or small?",
    "What helps you relax when you feel stressed, and how often do you practice it?",
    "Describe a recent moment when you felt truly at peace.",
    "What is one small step you can take today towards your well-being goals?",
    "If you could give your past self advice about stress, what would it be?",
    "Random Question" # New option
]

# State management for selected question to persist it
if 'selected_question_index' not in st.session_state:
    st.session_state.selected_question_index = 0

# Allow user to choose or get a random question
selected_question_display = st.selectbox(
    "💬 Choose a Reflection Question or get a random one:",
    reflection_questions,
    index=st.session_state.selected_question_index,
    key="question_selector"
)

# Handle "Random Question" selection
if selected_question_display == "Random Question":
    # Pick a random question from the original set, excluding 'Random Question' itself
    actual_reflection_questions = [q for q in reflection_questions if q != "Random Question"]
    selected_question = random.choice(actual_reflection_questions)
    st.session_state.random_question_generated = selected_question # Store for display
    st.info(f"You got a random question: **{selected_question}**")
else:
    selected_question = selected_question_display
    if 'random_question_generated' in st.session_state:
        del st.session_state.random_question_generated # Clear if user selects specific

# Display the actual question being answered
st.markdown(f"**Your chosen question:** *{selected_question}*")

# User input text area with a clear label
user_input = st.text_area("✍️ Write your reflection here (aim for at least a few sentences for better feedback):", height=150)

# Add a character counter for user guidance
if user_input:
    st.markdown(f"Characters: {len(user_input)}")

# Feedback button with improved logic
col1, col2 = st.columns([1, 3])
with col1:
    get_feedback_button = st.button("✨ Get Feedback")
with col2:
    if st.button("🔄 Clear Reflection"):
        user_input = "" # This will clear the text area
        st.session_state.clear() # Clear all session state, resetting the app to initial state
        st.experimental_rerun() # Rerun to reflect changes immediately

if get_feedback_button:
    if not user_input.strip(): # Check if input is just empty or whitespace
        st.warning("Please write something meaningful before clicking 'Get Feedback'. Your reflections matter!")
    elif len(user_input.strip()) < 20: # Encourage more detailed input
        st.warning("Your reflection seems a bit short. Try adding a few more details for better feedback!")
    else:
        with st.spinner("Processing your reflection with care..."):
            try:
                # Crafting a more nuanced prompt for the AI
                prompt_text = (
                    f"As a compassionate and non-judgmental mental wellness coach, provide gentle, encouraging, and insightful "
                    f"feedback on the following reflection. Focus on active listening, validation of feelings, and offering "
                    f"positive reinforcement or simple, actionable suggestions for well-being. The reflection is in response to the question: '{selected_question}'.\n\n"
                    f"User's Reflection: \"{user_input}\""
                )
                response = model.generate_content(prompt_text)

                st.success("📝 Here's some personalized feedback for you:")
                st.info(response.text) # Using st.info for a different visual style
                st.markdown("---")
                st.markdown("Remember, your well-being journey is unique. Take what resonates with you!")

            except Exception as e:
                st.error(f"An error occurred while generating feedback: {e}. Please try again later.")
                st.warning("If the issue persists, your input might be too long or contain sensitive information that the model cannot process.")

st.markdown("---")
st.markdown("Made with ❤️ for your mental wellness.")