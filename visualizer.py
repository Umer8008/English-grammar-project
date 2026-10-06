import re
from spacy import displacy
import streamlit as st
from src.utils import POS_FULL_NAMES, DEP_FULL_NAMES

# displaCy color palette — each POS gets a distinct background
POS_COLORS = {
    "NOUN":  "#1d4ed8",  # blue
    "VERB":  "#059669",  # green
    "ADJ":   "#9333ea",  # purple
    "ADV":   "#0891b2",  # cyan
    "PRON":  "#d97706",  # amber
    "PROPN": "#be185d",  # pink
    "DET":   "#64748b",  # slate
    "ADP":   "#0f766e",  # teal
    "AUX":   "#16a34a",  # green (lighter)
    "CCONJ": "#7c3aed",  # violet
    "SCONJ": "#6d28d9",  # violet darker
    "NUM":   "#b45309",  # orange
    "PART":  "#475569",  # slate darker
    "PUNCT": "#334155",  # very dark
    "INTJ":  "#dc2626",  # red
}


def _build_displacy_options() -> dict:
    """
    Builds displaCy render options so every token is coloured and every label
    (POS + dependency) is replaced with its full English name.
    """
    # Map short POS tag → full name for the token colour labels
    ent_labels = {short: full for short, full in POS_FULL_NAMES.items()}
    colors = {POS_FULL_NAMES.get(k, k): v for k, v in POS_COLORS.items()}

    return {
        "compact": False,
        "color": "#e2e8f0",
        "bg": "#0f172a",
        "font": "Inter, sans-serif",
    }


def _replace_labels_in_html(html: str) -> str:
    """
    Post-processes displaCy SVG/HTML to swap every short label with its full
    English name.

    displaCy uses:
      <tspan class="displacy-tag" ...>PRON</tspan>   ← POS tags
      <textPath class="displacy-label" ...>nsubj</textPath>  ← dep labels
    """
    # ── POS tags: <tspan class="displacy-tag" ...>PRON</tspan>
    for short, full in sorted(POS_FULL_NAMES.items(), key=lambda x: -len(x[0])):
        html = re.sub(
            rf'(<tspan\b[^>]*class="displacy-tag"[^>]*>){re.escape(short)}(</tspan>)',
            lambda m, f=full: m.group(1) + f + m.group(2),
            html,
        )

    # ── Dependency labels: <textPath class="displacy-label" ...>nsubj</textPath>
    for short, full in sorted(DEP_FULL_NAMES.items(), key=lambda x: -len(x[0])):
        html = re.sub(
            rf'(<textPath\b[^>]*class="displacy-label"[^>]*>){re.escape(short)}(</textPath>)',
            lambda m, f=full: m.group(1) + f + m.group(2),
            html,
        )

    return html




def render_dependency_tree(doc) -> None:
    """
    Generates and renders the displaCy dependency tree inside Streamlit.
    Uses full English names for all POS tags and dependency relations.

    Args:
        doc (spacy.tokens.Doc): The processed text.
    """
    if doc is None:
        st.warning("No text to visualize.")
        return

    sentences = list(doc.sents)

    options = {
        "compact": False,
        "color": "#e2e8f0",
        "bg": "#1e293b",
        "font": "Inter, sans-serif",
        "distance": 120,
        "arrow_spacing": 20,
        "word_spacing": 45,
    }

    if len(sentences) > 3:
        st.info(
            f"Your text contains {len(sentences)} sentences. "
            "Displaying each sentence separately for clarity."
        )
        for i, sent in enumerate(sentences):
            st.markdown(f"**Sentence {i + 1}** — *{sent.text.strip()}*")
            raw_html = displacy.render(sent, style="dep", page=False, options=options)
            clean_html = _replace_labels_in_html(raw_html)
            st.components.v1.html(clean_html, height=380, scrolling=True)
            st.markdown("---")
    else:
        raw_html = displacy.render(doc, style="dep", page=False, options=options)
        clean_html = _replace_labels_in_html(raw_html)
        st.components.v1.html(clean_html, height=500, scrolling=True)
