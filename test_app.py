import sys
import os

# Ensure we can import from src
sys.path.insert(0, os.path.abspath("."))

from src.nlp_processor import load_spacy_model, process_text, get_token_dataframe
from src.grammar_checker import check_grammar

def test_grammar_checker():
    print("Loading model...")
    nlp = load_spacy_model()
    if not nlp:
        print("Failed to load model. Exiting.")
        return

    test_cases = [
        {
            "text": "He go to school.",
            "expected_issue": "Possible subject-verb agreement error",
            "expected_suggestion": "He goes"
        },
        {
            "text": "They is happy.",
            "expected_issue": "Common 'is/are' mistake",
            "expected_suggestion": "They are"
        },
        {
            "text": "They was playing.",
            "expected_issue": "Common 'was/were' mistake",
            "expected_suggestion": "They were"
        },
        {
            "text": "She went to a university.", # Correct, 'university' sounds like 'y' so 'a' is okay, shouldn't flag it usually, but let's check what it does
            "expected_issue": None,
            "expected_suggestion": None
        },
        {
            "text": "He is an honest man.", # Same, 'honest' starts with 'o' sound. We might not catch it perfectly with basic rules, let's see.
            "expected_issue": None,
            "expected_suggestion": None
        }
    ]

    print("Running tests...")
    for idx, case in enumerate(test_cases, 1):
        text = case["text"]
        print(f"\n--- Test Case {idx} ---")
        print(f"Text: '{text}'")
        
        doc = process_text(nlp, text)
        issues = check_grammar(doc)
        
        if issues:
            print("Found Issues:")
            for issue in issues:
                print(f"  - {issue['issue_type']}: '{issue['original']}' -> '{issue['suggestion']}'")
        else:
            print("No issues found.")

    print("\nTests completed.")

if __name__ == "__main__":
    test_grammar_checker()
