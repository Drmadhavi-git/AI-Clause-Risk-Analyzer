from pypdf import PdfReader
from io import BytesIO

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(pdf_bytes))
    pages_text = []
    for page in reader.pages:
        txt = page.extract_text() or ""
        pages_text.append(txt)
    return "\n".join(pages_text).strip()
