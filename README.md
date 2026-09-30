# English Grammar Analyzer

## Description
A professional, beginner-friendly English Grammar Analyzer web application. It allows users to enter an English sentence or paragraph and receive a breakdown of its grammatical structure, including tokenization, POS tagging, lemmatization, and dependency parsing. It also includes a basic rule-based grammar checker and visualizes the dependency tree.

## Features
* **Tokenization**: Breaks text down into individual tokens (words and punctuation).
* **Part-of-Speech (POS) Tagging**: Identifies the grammatical role of each word.
* **Lemmatization**: Finds the base form of words.
* **Dependency Parsing**: Determines the grammatical structure and relationships between words.
* **Basic Grammar Checker**: Detects common rule-based grammar issues (e.g., subject-verb agreement, common is/are and was/were mistakes).
* **displaCy Visualization**: Renders an interactive dependency tree directly in the browser.
* **Text Statistics**: Displays character count, word count, sentence count, etc.

## Technologies
* Python
* spaCy
* displaCy
* Streamlit
* Pandas

## Installation

1. **Clone or download the project**

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download the spaCy model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Usage

1. **Run the application**
   ```bash
   streamlit run app.py
   ```
2. Open your browser to the URL provided (usually `http://localhost:8501`).
3. Enter English text into the provided text area and click **Analyze Text**.

## Future Improvements

The architecture is designed to support the following advanced features in the future:
* **Version 2**: More advanced grammar rules.
* **Version 3**: Spell checking.
* **Version 4**: Grammar scoring.
* **Version 5**: Machine-learning-based grammar error detection.
* **Version 6**: Transformer-based grammar correction.
* **Version 7**: Advanced writing assistant with context-aware corrections, readability scores, and vocabulary suggestions.
