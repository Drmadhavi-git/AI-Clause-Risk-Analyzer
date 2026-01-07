import requests
from typing import Dict
from src.config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL

def llm_explain_clause(clause: str) -> Dict:
    """
    Calls OpenAI Responses API (best-effort).
    If it fails, caller should fallback to rule-based output.
    """
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    prompt = f"""
You are a contract risk analyst.
Analyze this clause and output STRICT JSON with keys:
risk_level (Low/Medium/High),
risk_type (Legal/Financial/Compliance/Delivery/General),
reason (1-2 lines),
mitigation (1-2 lines).

Clause:
\"\"\"{clause}\"\"\"
"""

    # Using /responses (modern) if available; if your account doesn't support, switch to /chat/completions.
    url = f"{OPENAI_BASE_URL.rstrip('/')}/responses"
    payload = {
        "model": OPENAI_MODEL,
        "input": prompt,
        "temperature": 0.2,
    }

    r = requests.post(url, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    data = r.json()

    # Extract text output best-effort
    # Responses API structures differ; handle common cases
    text_out = ""
    if "output" in data:
        for item in data["output"]:
            if item.get("type") == "message":
                for c in item.get("content", []):
                    if c.get("type") in ("output_text", "text"):
                        text_out += c.get("text", "")
    if not text_out and "output_text" in data:
        text_out = data["output_text"]

    text_out = text_out.strip()

    # Expecting JSON; try parse safely
    import json
    try:
        obj = json.loads(text_out)
        return {
            "level": obj.get("risk_level", "Medium"),
            "type": obj.get("risk_type", "General"),
            "reason": obj.get("reason", ""),
            "mitigation": obj.get("mitigation", ""),
        }
    except Exception:
        # If parsing fails, return raw
        return {
            "level": "Medium",
            "type": "General",
            "reason": text_out[:400],
            "mitigation": "Review clause and negotiate clearer terms.",
        }
