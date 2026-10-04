import streamlit as st
import os
from src.nlp_processor import load_spacy_model, process_text, get_token_dataframe
from src.grammar_checker import check_grammar
from src.visualizer import render_dependency_tree
from src.utils import calculate_text_statistics, POS_DESCRIPTIONS, get_pos_full_name


# ── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="English Grammar Analyzer",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Load custom CSS ───────────────────────────────────────────────────────────
def _load_css():
    path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

_load_css()

# ── Load NLP model (cached) ───────────────────────────────────────────────────
with st.spinner("Initialising language model…"):
    nlp = load_spacy_model()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <h1>📖 English Grammar Analyzer</h1>
    <p>Analyze sentence structure, grammatical roles, and linguistic features — powered by advanced NLP.</p>
</div>
""", unsafe_allow_html=True)

# ── Input section ─────────────────────────────────────────────────────────────
st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.markdown("#### ✏️ Enter your text below")

text_input = st.text_area(
    label="Text input",
    label_visibility="collapsed",
    placeholder='e.g.  "She go to university every day. They is happy."',
    height=160,
    key="text_input",
)

def clear_text():
    st.session_state["text_input"] = ""

col_btn1, col_btn2, col_spacer = st.columns([1.2, 1, 7])
with col_btn1:
    analyze_btn = st.button("🔍  Analyze Text", type="primary", use_container_width=True)
with col_btn2:
    st.button("🗑️  Clear", use_container_width=True, on_click=clear_text)

st.markdown('</div>', unsafe_allow_html=True)

# ── Helper: coloured POS badge ────────────────────────────────────────────────
POS_BADGE_COLORS = {
    "Noun":                    ("#1d4ed8", "#dbeafe"),
    "Verb":                    ("#059669", "#d1fae5"),
    "Adjective":               ("#9333ea", "#f3e8ff"),
    "Adverb":                  ("#0891b2", "#cffafe"),
    "Pronoun":                 ("#d97706", "#fef3c7"),
    "Proper Noun":             ("#be185d", "#fce7f3"),
    "Determiner":              ("#475569", "#f1f5f9"),
    "Preposition":             ("#0f766e", "#ccfbf1"),
    "Auxiliary Verb":          ("#16a34a", "#dcfce7"),
    "Coordinating Conjunction":("#7c3aed", "#ede9fe"),
    "Subordinating Conjunction":("#6d28d9","#ede9fe"),
    "Numeral":                 ("#b45309", "#fef3c7"),
    "Punctuation":             ("#334155", "#e2e8f0"),
    "Interjection":            ("#dc2626", "#fee2e2"),
}

def pos_badge(pos_full: str) -> str:
    colors = POS_BADGE_COLORS.get(pos_full, ("#64748b", "#f1f5f9"))
    return (
        f'<span style="background:{colors[1]};color:{colors[0]};'
        f'padding:2px 10px;border-radius:99px;font-size:0.78rem;'
        f'font-weight:600;letter-spacing:0.04em;">{pos_full}</span>'
    )

# ── Analysis ──────────────────────────────────────────────────────────────────
if analyze_btn:
    raw_text = text_input.strip()

    # ── Validation ────────────────────────────────────────────
    if not raw_text:
        st.warning("⚠️  Please enter some English text to analyze.")
        st.stop()
    if len(raw_text) > 5000:
        st.warning("⚠️  Input is too long. Please keep it under 5 000 characters for best results.")
        st.stop()
    if nlp is None:
        st.error("❌  Language model is unavailable. Cannot process text.")
        st.stop()

    # ── Process ───────────────────────────────────────────────
    with st.spinner("Analyzing your text…"):
        doc = process_text(nlp, raw_text)

    if not doc:
        st.error("Could not process the provided text.")
        st.stop()

    # ── Tabs ──────────────────────────────────────────────────
    tab_overview, tab_tokens, tab_grammar, tab_tree = st.tabs([
        "📊  Overview",
        "🔤  Word Analysis",
        "✅  Grammar Check",
        "🌳  Sentence Tree",
    ])

    # ══════════════════════════════════════════════════════════
    # TAB 1 — OVERVIEW
    # ══════════════════════════════════════════════════════════
    with tab_overview:
        st.markdown("### 📋 Text Statistics")
        stats = calculate_text_statistics(doc)

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Sentences",              stats["Sentence count"])
        c2.metric("Total Words",            stats["Word count"])
        c3.metric("Unique Words",           stats["Number of unique words"])
        c4.metric("Characters",             stats["Character count"])
        c5.metric("Avg Words / Sentence",   stats["Average words per sentence"])

        st.markdown("---")
        st.markdown("### 🏷️ Parts of Speech Found")

        # Count POS
        pos_counts: dict[str, int] = {}
        for token in doc:
            if token.is_alpha:
                full = get_pos_full_name(token.pos_)
                pos_counts[full] = pos_counts.get(full, 0) + 1

        if pos_counts:
            sorted_pos = sorted(pos_counts.items(), key=lambda x: -x[1])
            cols = st.columns(min(len(sorted_pos), 4))
            for i, (name, count) in enumerate(sorted_pos):
                cols[i % 4].metric(name, count)
        else:
            st.info("No alphabetic tokens found.")

    # ══════════════════════════════════════════════════════════
    # TAB 2 — WORD ANALYSIS
    # ══════════════════════════════════════════════════════════
    with tab_tokens:
        st.markdown("### 🔤 Word-by-Word Breakdown")
        st.caption(
            "Every word (token) in your text is listed below with its grammatical properties. "
            "The **Base Form** is the dictionary form of the word. "
            "The **Grammatical Role** describes how the word functions in the sentence."
        )

        df = get_token_dataframe(doc)
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("### 📚 Parts of Speech — Legend")
        st.caption("Click on any entry below to learn what each grammatical category means.")

        cols = st.columns(2)
        for i, (name, desc) in enumerate(POS_DESCRIPTIONS.items()):
            badge = pos_badge(name)
            cols[i % 2].markdown(
                f"{badge}&nbsp;&nbsp;<span style='color:#94a3b8;font-size:0.88rem;'>{desc}</span>",
                unsafe_allow_html=True,
            )
            cols[i % 2].markdown("")

    # ══════════════════════════════════════════════════════════
    # TAB 3 — GRAMMAR CHECK
    # ══════════════════════════════════════════════════════════
    with tab_grammar:
        st.markdown("### ✅ Grammar Analysis")
        st.info(
            "ℹ️  This tool uses rule-based NLP analysis to highlight *possible* grammar issues. "
            "It is not a replacement for a full grammar-correction engine — uncertain cases are "
            "labelled **'Possible issue'** rather than definite errors.",
            icon=None,
        )

        issues = check_grammar(doc)

        if not issues:
            st.success("🎉  Great news! No obvious grammar issues were detected in your text.")
        else:
            st.warning(f"⚠️  Found **{len(issues)}** possible grammar issue(s) in your text.")
            st.markdown("")

            for i, issue in enumerate(issues, 1):
                st.markdown(
                    f"""
                    <div class="issue-card">
                        <div class="issue-title">#{i} &nbsp;{issue['issue_type']}</div>
                        <div class="issue-row">
                            <span class="label">Original</span>
                            <span class="original">{issue['original']}</span>
                        </div>
                        <div class="issue-row">
                            <span class="label">Suggestion</span>
                            <span class="suggestion">{issue['suggestion']}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("---")
        st.markdown("### 📖 Rules Applied")
        with st.expander("See the grammar rules this tool checks"):
            st.markdown("""
| Rule | Example Error | Suggested Fix |
|---|---|---|
| Subject–Verb Agreement (3rd-person singular) | *He go* to school | He **goes** to school |
| Subject–Verb Agreement (plural subjects) | *They goes* home | They **go** home |
| Incorrect use of **is** vs **are** | *They is* happy | They **are** happy |
| Incorrect use of **was** vs **were** | *They was* playing | They **were** playing |
| Incorrect use of **a** vs **an** | *a apple* | **an** apple |
""")

    # ══════════════════════════════════════════════════════════
    # TAB 4 — DEPENDENCY TREE
    # ══════════════════════════════════════════════════════════
    with tab_tree:
        st.markdown("### 🌳 Sentence Structure Diagram")
        st.caption(
            "The diagram below shows how every word in your sentence connects to the others. "
            "Arrows point from a word to the word it **modifies or depends on**. "
            "Labels on the arrows and beneath each word use full grammatical names."
        )
        render_dependency_tree(doc)
