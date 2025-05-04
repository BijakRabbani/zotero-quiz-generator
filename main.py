import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
from zotero_module import get_highlights, get_randomized_highlights, clear_cache

# Load environment variables from .env file
load_dotenv()


#% Generate quizzes using Gemini
@st.cache_data
def generate_quiz_with_gemini(highlight):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    prompt = (
        f"Create a multiple-choice quiz question based on the following sentence: {highlight}. "

        "Provide four options, one of which is correct. Clearly indicate the correct answer."
        "Format the output as follows:"
        "[Your question here]\n"
        "A. [Option 1];B. [Option 2];C. [Option 3];D. [Option 4]\n"
        "[Correct option number]\n"
        "Make sure the question is clear and the options are distinct."
        "Make sure to not include the square bracktes in the output."
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )

    quiz_text = response.text

    # Parse the response to extract the question, options, and correct answer
    lines = quiz_text.split("\n")
    question = lines[0]
    options = lines[1].split(";")
    correct_answer = lines[2]
    return question, options, correct_answer


#%% Streamlit app for quiz generation with API key input in the sidebar
def create_quiz_app_with_gemini(highlights):
    st.title("Zotero Quiz Generator with Gemini")
    st.write("This app generates quizzes based on your Zotero highlights using Gemini.")

    # Check environment variables for API keys and set them in session state
    if "GEMINI_API_KEY" not in st.session_state and os.getenv("GEMINI_API_KEY"):
        st.session_state["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
    if "ZOTERO_LIBRARY_ID" not in st.session_state and os.getenv("ZOTERO_LIBRARY_ID"):
        st.session_state["ZOTERO_LIBRARY_ID"] = os.getenv("ZOTERO_LIBRARY_ID")
    if "ZOTERO_API_KEY" not in st.session_state and os.getenv("ZOTERO_API_KEY"):
        st.session_state["ZOTERO_API_KEY"] = os.getenv("ZOTERO_API_KEY")

    # Sidebar for API key input
    if (
        "GEMINI_API_KEY" not in st.session_state
        or "ZOTERO_LIBRARY_ID" not in st.session_state
        or "ZOTERO_API_KEY" not in st.session_state
    ):
        st.sidebar.title("Configuration")
        gemini_api_key = st.sidebar.text_input("Gemini API Key", type="password")
        zotero_api_key = st.sidebar.text_input("Zotero API Key", type="password")
        zotero_library_id = st.sidebar.text_input("Zotero Library ID")

        # Save API keys to session state
        if gemini_api_key:
            st.session_state["GEMINI_API_KEY"] = gemini_api_key
        if zotero_library_id:
            st.session_state["ZOTERO_LIBRARY_ID"] = zotero_library_id
        if zotero_api_key:
            st.session_state["ZOTERO_API_KEY"] = zotero_api_key

    

    # Check if API keys are provided
    if "GEMINI_API_KEY" not in st.session_state or "ZOTERO_LIBRARY_ID" not in st.session_state or "ZOTERO_API_KEY" not in st.session_state:
        st.error("Please provide all required API keys in the sidebar.")
        return

    if st.button("Refresh Data"):
        # clear_cache()
        st.rerun()

    # Session state to track the current highlight index
    if 'current_index' not in st.session_state:
        st.session_state['current_index'] = 0

    # Get the current highlight
    current_index = st.session_state['current_index']
    if current_index >= len(highlights):
        st.write("No more questions available.")
        return

    selected_highlight = highlights[current_index]

    # Generate quiz for the current highlight
    question, options, correct_answer = generate_quiz_with_gemini(selected_highlight)

    st.write("### Quiz Question")
    st.write(question)

    selected_option = st.radio("Options", options, key=f"options_{current_index}")

    if st.button("Submit Answer"):
        if selected_option == correct_answer:
            st.success("Correct! 🎉")
        else:
            st.error(f"Incorrect. The correct answer is: {correct_answer}")

    # Next button to move to the next highlight
    if st.button("Next Question"):
        st.session_state['current_index'] += 1
        st.rerun()

#%% Example usage
if __name__ == "__main__":
    highlights = get_highlights()
    highlights_list = get_randomized_highlights(highlights)
    create_quiz_app_with_gemini(highlights_list)