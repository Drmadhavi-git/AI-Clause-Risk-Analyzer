
---

# 5) `api/app.py`

```python
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from src.pipeline import analyze_pdf_bytes

app = FastAPI(title="AI Clause Risk Analyzer", version="1.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
      <head><title>AI Clause Risk Analyzer</title></head>
      <body style="font-family: Arial; margin: 40px;">
        <h2>AI Clause Risk Analyzer</h2>
        <p>Upload a PDF and get clause-level risk analysis (JSON).</p>
        <form action="/analyze" method="post" enctype="multipart/form-data">
          <input type="file" name="file" accept="application/pdf" required />
          <button type="submit" style="margin-left:10px;">Analyze</button>
        </form>
        <p style="margin-top:20px;">
          Or use Swagger UI: <a href="/docs">/docs</a>
        </p>
      </body>
    </html>
    """

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        return JSONResponse({"error": "Please upload a PDF file."}, status_code=400)

    pdf_bytes = await file.read()
    result = analyze_pdf_bytes(pdf_bytes, filename=file.filename)
    return JSONResponse(result)
