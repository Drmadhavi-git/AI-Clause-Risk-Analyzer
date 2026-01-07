from typing import Dict, List, Tuple

# Keyword-driven rules for v1 (works without any LLM)
RISK_RULES: List[Tuple[str, Dict]] = [
    ("termination for convenience", {"level": "High", "type": "Legal", "mitigation": "Negotiate termination notice, compensation, and partial payment protections."}),
    ("penalty", {"level": "High", "type": "Financial", "mitigation": "Cap penalties, add grace period, and define measurable triggers."}),
    ("liquidated damages", {"level": "High", "type": "Financial", "mitigation": "Negotiate LD cap, exclusions for force majeure, and mutuality."}),
    ("indemn", {"level": "High", "type": "Legal", "mitigation": "Limit indemnity scope, add liability caps, exclude indirect damages."}),
    ("unlimited liability", {"level": "High", "type": "Legal", "mitigation": "Add liability cap and exclude consequential damages."}),
    ("audit", {"level": "Medium", "type": "Compliance", "mitigation": "Define audit scope, notice period, and confidentiality handling."}),
    ("data protection", {"level": "Medium", "type": "Compliance", "mitigation": "Ensure GDPR/DPDP alignment, add DPA, define breach notification SLAs."}),
    ("payment shall be made within 90", {"level": "High", "type": "Financial", "mitigation": "Reduce payment terms to 30 days; add interest on late payments."}),
    ("delay", {"level": "Medium", "type": "Delivery", "mitigation": "Define realistic timelines, add dependency clauses, and change control process."}),
    ("force majeure", {"level": "Low", "type": "Legal", "mitigation": "Ensure FM is mutual and includes clear triggers and notice requirements."}),
]

DEFAULT = {"level": "Low", "type": "General", "mitigation": "Clarify definitions, responsibilities, and add change-control where needed."}

def classify_with_rules(clause: str) -> Dict:
    c = clause.lower()

    matched = []
    for key, meta in RISK_RULES:
        if key in c:
            matched.append(meta)

    if matched:
        # Pick the highest severity among matches
        # High > Medium > Low
        priority = {"High": 3, "Medium": 2, "Low": 1}
        best = sorted(matched, key=lambda x: priority.get(x["level"], 1), reverse=True)[0]
        return best

    # Secondary heuristics
    if any(k in c for k in ["shall", "must", "required"]):
        return {"level": "Medium", "type": "Obligation", "mitigation": "Validate obligations, define acceptance criteria, and align with delivery capacity."}

    return DEFAULT
