import pandas as pd

# ── Full POS names ────────────────────────────────────────────────────────────
POS_FULL_NAMES = {
    "NOUN":  "Noun",
    "VERB":  "Verb",
    "ADJ":   "Adjective",
    "ADV":   "Adverb",
    "PRON":  "Pronoun",
    "PROPN": "Proper Noun",
    "DET":   "Determiner",
    "ADP":   "Preposition",
    "CONJ":  "Conjunction",
    "CCONJ": "Coordinating Conjunction",
    "SCONJ": "Subordinating Conjunction",
    "NUM":   "Numeral",
    "PART":  "Particle",
    "PUNCT": "Punctuation",
    "SYM":   "Symbol",
    "INTJ":  "Interjection",
    "AUX":   "Auxiliary Verb",
    "SPACE": "Space",
    "X":     "Other / Foreign Word",
}

# ── Full dependency relation names ────────────────────────────────────────────
DEP_FULL_NAMES = {
    "ROOT":     "Root (Main Verb)",
    "nsubj":    "Nominal Subject",
    "nsubjpass":"Passive Nominal Subject",
    "dobj":     "Direct Object",
    "iobj":     "Indirect Object",
    "pobj":     "Object of Preposition",
    "attr":     "Attribute",
    "acomp":    "Adjectival Complement",
    "ccomp":    "Clausal Complement",
    "xcomp":    "Open Clausal Complement",
    "prep":     "Prepositional Modifier",
    "agent":    "Agent (Passive)",
    "amod":     "Adjectival Modifier",
    "advmod":   "Adverbial Modifier",
    "npadvmod": "Noun Phrase Adverbial Modifier",
    "nummod":   "Numeric Modifier",
    "appos":    "Appositional Modifier",
    "nn":       "Noun Compound Modifier",
    "compound": "Compound Word",
    "aux":      "Auxiliary Verb",
    "auxpass":  "Passive Auxiliary Verb",
    "cop":      "Copula (Linking Verb)",
    "mark":     "Subordination Marker",
    "det":      "Determiner",
    "poss":     "Possessive Modifier",
    "case":     "Case Marker",
    "punct":    "Punctuation",
    "cc":       "Coordinating Conjunction",
    "conj":     "Conjunct",
    "neg":      "Negation Modifier",
    "expl":     "Expletive (there/it)",
    "prt":      "Phrasal Verb Particle",
    "relcl":    "Relative Clause Modifier",
    "acl":      "Adjectival Clause",
    "advcl":    "Adverbial Clause Modifier",
    "parataxis":"Parataxis",
    "dep":      "Unclassified Dependency",
    "quantmod": "Quantifier Modifier",
    "pcomp":    "Complement of Preposition",
    "csubj":    "Clausal Subject",
    "intj":     "Interjection",
}

# ── POS descriptions for UI legend ───────────────────────────────────────────
POS_DESCRIPTIONS = {
    "Noun":                    "A person, place, thing, or concept",
    "Verb":                    "An action or state of being",
    "Adjective":               "A word that describes or modifies a noun",
    "Adverb":                  "Modifies a verb, adjective, or another adverb",
    "Pronoun":                 "Replaces a noun (he, she, they, it…)",
    "Proper Noun":             "The specific name of a person, place, or thing",
    "Determiner":              "Introduces a noun phrase (a, an, the, this…)",
    "Preposition":             "Shows relationship between words (in, on, to…)",
    "Coordinating Conjunction":"Joins equal clauses or words (and, but, or…)",
    "Subordinating Conjunction":"Begins a dependent clause (because, if, when…)",
    "Auxiliary Verb":          "Helps the main verb (is, was, will, can…)",
    "Numeral":                 "A number or quantity word",
    "Particle":                "A small function word (up, out, not…)",
    "Punctuation":             "Punctuation mark",
    "Interjection":            "An exclamation (wow, oh, yes…)",
}


def get_pos_full_name(pos_tag: str) -> str:
    """Returns the full English name for a spaCy POS tag."""
    return POS_FULL_NAMES.get(pos_tag, pos_tag)


def get_dep_full_name(dep: str) -> str:
    """Returns the full English name for a spaCy dependency label."""
    return DEP_FULL_NAMES.get(dep, dep.capitalize())


def get_pos_explanation(pos_tag: str) -> str:
    """Returns a plain-English description for a given POS tag."""
    full = get_pos_full_name(pos_tag)
    return POS_DESCRIPTIONS.get(full, "")


def calculate_text_statistics(doc) -> dict:
    """
    Calculates basic text statistics from a spaCy Doc object.

    Args:
        doc (spacy.tokens.Doc): The processed text.

    Returns:
        dict: A dictionary containing various text statistics.
    """
    text = doc.text
    char_count = len(text)
    words = [token for token in doc if token.is_alpha]
    word_count = len(words)
    sentences = list(doc.sents)
    sentence_count = len(sentences)
    unique_words = len(set(token.lower_ for token in words))
    avg_wps = word_count / sentence_count if sentence_count > 0 else 0

    return {
        "Character count": char_count,
        "Word count": word_count,
        "Sentence count": sentence_count,
        "Average words per sentence": round(avg_wps, 1),
        "Number of unique words": unique_words,
    }
