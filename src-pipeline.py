from typing import Dict, Any, List
from src.pdf_loader import extract_text_from_pdf_bytes
from src.clause_splitter import split_into_clauses
from src.risk_rules import classify_with_rules
from src.config import openai_enabled

def analyze_pdf_bytes(pdf_bytes: bytes, filename: str = "uploaded.pdf") -> Dict[str, Any]:
    text = extract_text_from_pdf_bytes(pdf_bytes)
    clauses = split_into_clauses(text)

    results: List[Dict[str, Any]] = []
    use_llm = openai_enabled()

    llm_fn = None
    if use_llm:
        try:
            from src.llm_openai import llm_explain_clause
            llm_fn = llm_explain_clause
        except Exception:
            llm_fn = None
            use_llm = False

    for i, clause in enumerate(clauses, start=1):
        base = classify_with_rules(clause)

        item = {
            "id": i,
            "clause": clause,
            "risk_level": base["level"],
            "risk_type": base["type"],
            "reason": "",
            "mitigation": base["mitigation"],
            "method": "rules",
        }

        # Optional LLM enrichment
        if use_llm and llm_fn:
            try:
                llm_out = llm_fn(clause)
                item.update({
                    "risk_level": llm_out.get("level", item["risk_level"]),
                    "risk_type": llm_out.get("type", item["risk_type"]),
                    "reason": llm_out.get("reason", ""),
                    "mitigation": llm_out.get("mitigation", item["mitigation"]),
                    "method": "openai",
                })
            except Exception:
                # silently fallback
                pass

        results.append(item)

    # Summary counts
    counts = {"High": 0, "Medium": 0, "Low": 0}
    for r in results:
        lvl = r.get("risk_level", "Low")
        if lvl not in counts:
            counts[lvl] = 0
        counts[lvl] += 1

    return {
        "filename": filename,
        "total_clauses": len(results),
        "risk_summary": counts,
        "clauses": results,
    }
