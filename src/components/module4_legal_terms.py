import re

_LEXICON = {
    "indemnity": "Indemnity Clause",
    "indemnify": "Indemnity Clause",
    "security deposit": "Payment Terms",
    "termination": "Termination Clause",
    "arbitration": "Dispute Resolution",
    "dispute resolution": "Dispute Resolution",
    "force majeure": "Force Majeure",
    "governing law": "Governing Law",
    "warranty": "Warranty",
    "confidential": "Confidentiality",
    "intellectual property": "IP Rights",
    "non-compete": "Non-Compete",
    "severability": "Severability",
    "amendment": "Amendment Rights",
    "assignment": "Assignment Rights",
    "liability": "Liability",
    "damages": "Damages",
}

try:
    import spacy
    _HAS_SPACY = True
    try:
        _SPACY_NLP = spacy.load("en_core_web_sm")
    except Exception:
        _SPACY_NLP = None
except Exception:
    _HAS_SPACY = False
    _SPACY_NLP = None


def extract_legal_terms(text: str):
    if not text or not text.strip():
        return []

    found = []
    seen = set()
    
    quoted_pattern = r'["\']([A-Z][A-Za-z\s]{2,30})["\']'
    for match in re.finditer(quoted_pattern, text):
        term = match.group(1).strip()
        if term not in seen:
            found.append((term, "Defined Term"))
            seen.add(term)
    
    definition_pattern = r'([A-Z][A-Za-z\s]{2,30})\s*(?:\(hereinafter|shall mean|means|refers to)'
    for match in re.finditer(definition_pattern, text):
        term = match.group(1).strip()
        if term not in seen:
            found.append((term, "Defined Term"))
            seen.add(term)
    
    t = text.lower()
    for keyword, category in _LEXICON.items():
        if keyword in t:
            if keyword not in seen:
                found.append((keyword.title(), category))
                seen.add(keyword)
    
    if _SPACY_NLP:
        try:
            doc = _SPACY_NLP(text[:5000])
            for ent in doc.ents:
                if ent.label_ in ['LAW', 'ORG', 'EVENT'] and ent.text not in seen:
                    found.append((ent.text, f"{ent.label_} Entity"))
                    seen.add(ent.text)
        except Exception:
            pass

    return found
