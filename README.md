# Zotero-Notion Quiz Generator

This project is a **Streamlit-based application** that generates multiple-choice quizzes from Zotero highlights using the **Gemini API**. The app allows users to input their API keys, retrieve highlights from Zotero, and generate quizzes interactively.

---

## Features

- **Zotero Integration**: Fetch highlights from Zotero collections.
- **Gemini API Integration**: Generate multiple-choice quiz questions based on highlights.
- **Interactive UI**: Built with Streamlit, featuring:
  - Sidebar for API key configuration.
  - Quiz display with options to submit answers.
- **Randomized Highlights**: Highlights are shuffled to ensure variety.
- **Purple Highlights Only**: The script only considers highlights with the purple color (`#a28ae5`). This allows other colors to be used for standard highlighting or other purposes.

---

## Requirements

- Python 3.8 or higher
- Zotero account and API key
- Gemini API key

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/zotero-notion-quiz-generator.git
   cd zotero-notion-quiz-generator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run main.py
   ```

2. Open the app in your browser (usually at `http://localhost:8501`).

3. Configure your API keys in the **sidebar** if not already set in the `.env` file.

4. Interact with the app:
   - View quiz questions generated from Zotero highlights.
   - Submit answers and check correctness.
   - Use the "Next Question" button to load the next quiz.

---

## Project Structure

```
zotero-notion-quiz-generator/
├── main.py                # Streamlit dashboard logic
├── zotero_module.py       # Zotero data retrieval and processing logic
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not included in the repo)
└── README.md              # Project documentation
```

---

## Environment Variables

The app uses the following environment variables:

- `GEMINI_API_KEY`: Your Gemini API key for quiz generation.
- `ZOTERO_LIBRARY_ID`: Your Zotero library ID.
- `ZOTERO_API_KEY`: Your Zotero API key.

These can be set in the `.env` file or entered manually in the app's sidebar.

---

## Dependencies

- `streamlit`: For building the interactive UI.
- `pyzotero`: For interacting with the Zotero API.
- `google-genai`: For using the Gemini API.
- `python-dotenv`: For managing environment variables.

Install all dependencies using:
```bash
pip install -r requirements.txt
```


---

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the interactive UI framework.
- [Zotero](https://www.zotero.org/) for the reference management tool.
- [Gemini API](https://genai.google/) for quiz generation.