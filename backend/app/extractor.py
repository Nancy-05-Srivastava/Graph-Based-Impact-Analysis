import re
from typing import Dict, List

OBLIGATION_PATTERNS = [
    r"\bmust\b", r"\bshall\b", r"\brequired to\b", r"\bshould\b",
    r"\bprohibited\b", r"\bmandatory\b", r"\bmaintain\b",
    r"\bverify\b", r"\bmonitor\b", r"\breport\b",
]

def split_clauses(text: str) -> List[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    parts = re.split(r"(?<=[.!?])\s+|\n+", text)
    return [p.strip() for p in parts if len(p.strip()) > 25]

def extract_obligations(text: str, limit: int = 12) -> List[str]:
    hits = []
    for clause in split_clauses(text):
        if any(re.search(pattern, clause.lower()) for pattern in OBLIGATION_PATTERNS):
            hits.append(clause)
        if len(hits) >= limit:
            break
    return hits

def extract_entities(text: str) -> Dict[str, List[str]]:
    low = text.lower()
    terms = {
        "payment": ["payment", "transaction", "settlement", "remittance"],
        "kyc": ["kyc", "customer due diligence", "identity verification"],
        "aml": ["aml", "money laundering", "suspicious transaction"],
        "sanctions": ["sanctions", "screening", "restricted party"],
        "cross_border": ["cross-border", "international payment", "foreign exchange"],
        "data": ["data retention", "record keeping", "privacy", "personal data"],
    }
    return {
        key: [term for term in values if term in low]
        for key, values in terms.items()
        if any(term in low for term in values)
    }
