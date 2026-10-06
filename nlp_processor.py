import spacy
import pandas as pd
import streamlit as st
from src.utils import get_pos_full_name, get_dep_full_name, get_pos_explanation


@st.cache_resource
def load_spacy_model(model_name: str = "en_core_web_md"):
    """
    Loads the spaCy model.
    Uses st.cache_resource to avoid reloading the model on every interaction.
    Automatically downloads the model if it's missing.
    """
    try:
        nlp = spacy.load(model_name)
        return nlp
    except OSError:
        print(f"Downloading the spaCy language model '{model_name}'... This might take a minute on the first run.")
        from spacy.cli import download
        try:
            download(model_name)
            nlp = spacy.load(model_name)
            print(f"Successfully downloaded and loaded '{model_name}'!")
            return nlp
        except Exception as e:
            st.error(f"Failed to automatically download and load the spaCy model '{model_name}'. Error: {e}")
            return None


def process_text(nlp, text: str):
    """
    Processes text using the loaded spaCy model.

    Args:
        nlp (spacy.Language): The loaded spaCy model.
        text (str):           The text to process.

    Returns:
        spacy.tokens.Doc | None
    """
    if not text or not str(text).strip():
        return None
    return nlp(text)


def get_token_dataframe(doc) -> pd.DataFrame:
    """
    Extracts token information from a spaCy Doc and returns a formatted DataFrame
    with full human-readable names for every column.

    Args:
        doc (spacy.tokens.Doc): The processed text.

    Returns:
        pd.DataFrame
    """
    if doc is None:
        return pd.DataFrame()

    rows = []
    for token in doc:
        rows.append({
            "Token (Word)":         token.text,
            "Base Form (Lemma)":    token.lemma_,
            "Part of Speech":       get_pos_full_name(token.pos_),
            "Grammatical Role":     get_dep_full_name(token.dep_),
            "Fine-grained Tag":     token.tag_,
            "Is a Stop Word":       "Yes" if token.is_stop else "No",
            "Is Alphabetic":        "Yes" if token.is_alpha else "No",
        })

    return pd.DataFrame(rows)
