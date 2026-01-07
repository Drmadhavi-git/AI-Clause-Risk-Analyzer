import re
from typing import List

def split_into_clauses(text: str, max_len: int = 800) -> List[str]:
    """
    Simple clause/paragraph splitter:
    - splits by blank lines
    - further splits long paragraphs by sentence boundaries
    """
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if not text:
        return []

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    clauses: List[str] = []

    for p in paragraphs:
        if len(p) <= max_len:
            clauses.append(p)
            continue

        # Split long paragraph by sentences
        sentences = re.split(r"(?<=[.!?])\s+", p)
        buf = ""
        for s in sentences:
            if not s:
                continue
            if len(buf) + len(s) + 1 <= max_len:
                buf = (buf + " " + s).strip()
            else:
                if buf:
                    clauses.append(buf)
                buf = s.strip()
        if buf:
            clauses.append(buf)

    # Clean tiny junk
    clauses = [c.strip() for c in clauses if len(c.strip()) > 20]
    return clauses
