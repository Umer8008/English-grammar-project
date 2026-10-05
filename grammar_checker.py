def _conjugate_3rd_singular(lemma: str) -> str:
    """
    Returns the 3rd-person singular present tense form of a verb.
    Handles common English spelling rules:
      - goes, does, has
      - verbs ending in -s, -x, -z, -ch, -sh → add -es
      - verbs ending in consonant+y → replace y with -ies
      - everything else → add -s
    """
    if lemma in ("be", "go"):
        return {"be": "is", "go": "goes"}[lemma]
    if lemma == "have":
        return "has"
    if lemma == "do":
        return "does"
    if lemma.endswith(("s", "x", "z", "ch", "sh")):
        return lemma + "es"
    if lemma.endswith("y") and len(lemma) > 1 and lemma[-2] not in "aeiou":
        return lemma[:-1] + "ies"
    return lemma + "s"


def check_grammar(doc):
    """
    Performs basic, rule-based grammar checking on a spaCy Doc.
    
    Args:
        doc (spacy.tokens.Doc): The processed text.
        
    Returns:
        list: A list of dictionaries containing detected grammar issues.
              Each dict has keys: 'issue_type', 'original', 'suggestion'.
    """
    issues = []
    
    if doc is None:
        return issues
        
    for sent in doc.sents:
        # Check for subject-verb agreement and common is/are/was/were mistakes
        # We iterate through the tokens to find a subject and its root verb
        for token in sent:
            # Look for PRON subjects
            if token.dep_ == "nsubj" and token.pos_ == "PRON":
                subj = token
                verb = token.head
                
                # Only analyze if the head is a verb or auxiliary
                if verb.pos_ in ["VERB", "AUX"]:
                    
                    # 1. Check basic Subject-Verb Agreement for 3rd person singular present
                    if subj.text.lower() in ["he", "she", "it"]:
                        # If verb is present tense, not 3rd person singular
                        if verb.tag_ == "VBP": 
                            # Exception for modals which don't inflect (e.g. "He can")
                            if verb.lemma_ != "be":
                                conjugated = _conjugate_3rd_singular(verb.lemma_)
                                issues.append({
                                    "issue_type": "Possible subject-verb agreement error",
                                    "original": f"{subj.text} {verb.text}",
                                    "suggestion": f"{subj.text} {conjugated}"
                                })
                    
                    # Check plural pronouns with 3rd person singular verb
                    elif subj.text.lower() in ["they", "we", "you", "i"]:
                        if verb.tag_ == "VBZ":
                            if verb.lemma_ != "be":
                                issues.append({
                                    "issue_type": "Possible subject-verb agreement error",
                                    "original": f"{subj.text} {verb.text}",
                                    "suggestion": f"{subj.text} {verb.lemma_}"
                                })

                    # 2. Check "is/are" mistakes
                    if subj.text.lower() in ["they", "we", "you"]:
                        if verb.text.lower() == "is":
                            issues.append({
                                "issue_type": "Common 'is/are' mistake",
                                "original": f"{subj.text} {verb.text}",
                                "suggestion": f"{subj.text} are"
                            })
                    elif subj.text.lower() in ["he", "she", "it"]:
                        if verb.text.lower() == "are":
                            issues.append({
                                "issue_type": "Common 'is/are' mistake",
                                "original": f"{subj.text} {verb.text}",
                                "suggestion": f"{subj.text} is"
                            })
                            
                    # 3. Check "was/were" mistakes (direct head)
                    if subj.text.lower() in ["they", "we", "you"]:
                        if verb.text.lower() == "was":
                            issues.append({
                                "issue_type": "Common 'was/were' mistake",
                                "original": f"{subj.text} {verb.text}",
                                "suggestion": f"{subj.text} were"
                            })
                    elif subj.text.lower() in ["he", "she", "it", "i"]:
                        if verb.text.lower() == "were":
                            # Note: "If I were" is subjunctive and correct, but we keep it simple for now
                            if not (subj.text.lower() == "i" and any(t.text.lower() == "if" for t in sent)):
                                issues.append({
                                    "issue_type": "Common 'was/were' mistake",
                                    "original": f"{subj.text} {verb.text}",
                                    "suggestion": f"{subj.text} was"
                                })

        # Also scan for aux tokens in the sentence that link to a pronoun subject
        # This catches "He were playing" where 'were' is AUX and not the direct nsubj head
        for token in sent:
            if token.pos_ == "AUX" and token.dep_ == "aux":
                # Find the subject of the root verb that this aux is attached to
                root_verb = token.head
                subj_of_root = None
                for child in root_verb.children:
                    if child.dep_ == "nsubj" and child.pos_ == "PRON":
                        subj_of_root = child
                        break
                if subj_of_root is None:
                    continue
                s = subj_of_root.text.lower()
                if s in ["they", "we", "you"] and token.text.lower() == "was":
                    issues.append({
                        "issue_type": "Common 'was/were' mistake",
                        "original": f"{subj_of_root.text} {token.text}",
                        "suggestion": f"{subj_of_root.text} were"
                    })
                elif s in ["he", "she", "it", "i"] and token.text.lower() == "were":
                    if not (s == "i" and any(t.text.lower() == "if" for t in sent)):
                        issues.append({
                            "issue_type": "Common 'was/were' mistake",
                            "original": f"{subj_of_root.text} {token.text}",
                            "suggestion": f"{subj_of_root.text} was"
                        })

    # 4. Basic Article Checking (a/an)
    for token in doc:
        if token.text.lower() in ["a", "an"]:
            # Get the next token
            if token.i + 1 < len(doc):
                next_token = doc[token.i + 1]
                # A very basic phonetic check based on spelling (vowels)
                starts_with_vowel = next_token.text.lower()[0] in ['a', 'e', 'i', 'o', 'u']
                
                # Exceptions like "university", "hour" are complex, so we keep this basic and mark as "Possible"
                if token.text.lower() == "a" and starts_with_vowel:
                    # Ignore 'u' as it often sounds like 'y' (university, user)
                    if next_token.text.lower()[0] != 'u':
                        issues.append({
                            "issue_type": "Possible article mistake (a vs an)",
                            "original": f"{token.text} {next_token.text}",
                            "suggestion": f"an {next_token.text}"
                        })
                elif token.text.lower() == "an" and not starts_with_vowel:
                    # Ignore 'h' as it might be silent (hour, honest)
                    if next_token.text.lower()[0] != 'h':
                        issues.append({
                            "issue_type": "Possible article mistake (a vs an)",
                            "original": f"{token.text} {next_token.text}",
                            "suggestion": f"a {next_token.text}"
                        })
                        
    # Deduplicate issues based on original text
    unique_issues = []
    seen = set()
    for issue in issues:
        if issue["original"] not in seen:
            unique_issues.append(issue)
            seen.add(issue["original"])

    return unique_issues
