"""
Medication interaction checks (rule-based MVP + text parsing).
OpenFDA has no simple interaction API; curated pairs supplement LLM output.
"""

import re
from typing import List

# Curated high-risk pairs (lowercase drug name fragments)
_KNOWN_INTERACTIONS: dict[frozenset[str], str] = {
    frozenset({"warfarin", "aspirin"}): (
        "Warfarin + aspirin: increased risk of bleeding. Seek clinician review."
    ),
    frozenset({"warfarin", "ibuprofen"}): (
        "Warfarin + NSAIDs (e.g. ibuprofen): increased bleeding risk."
    ),
    frozenset({"metformin", "alcohol"}): (
        "Metformin + alcohol: increased risk of lactic acidosis."
    ),
    frozenset({"lisinopril", "potassium"}): (
        "ACE inhibitor + potassium supplements: risk of hyperkalemia."
    ),
    frozenset({"simvastatin", "grapefruit"}): (
        "Statin + grapefruit: may increase statin levels and toxicity risk."
    ),
}


def parse_medication_list(medications_text: str) -> List[str]:
    """Split free-text medications into normalized tokens."""
    if not medications_text or not medications_text.strip():
        return []
    parts = re.split(r"[,;\n]+", medications_text.lower())
    return [p.strip() for p in parts if p.strip()]


def check_known_interactions(medications: List[str]) -> List[str]:
    """Return warnings for curated drug pairs present in the list."""
    if not medications:
        return []
    full_text = " ".join(medications).lower()
    warnings: List[str] = []
    for pair, message in _KNOWN_INTERACTIONS.items():
        if all(drug in full_text for drug in pair):
            warnings.append(message)
    return list(dict.fromkeys(warnings))


def enrich_drug_warnings(
    medications_text: str, existing_warnings: List[str]
) -> List[str]:
    """Merge LLM warnings with rule-based interaction checks."""
    parsed = parse_medication_list(medications_text)
    rule_warnings = check_known_interactions(parsed)
    combined = list(existing_warnings) + rule_warnings
    return list(dict.fromkeys(combined))
