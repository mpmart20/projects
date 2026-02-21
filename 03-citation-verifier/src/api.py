"""FastAPI backend for Citation Verifier."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from verifier import CitationVerifier
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(title="Citation Verifier")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
verifier = CitationVerifier()

class VerifyRequest(BaseModel):
    text: str

@app.post("/api/verify")
async def verify_text(req: VerifyRequest):
    results = verifier.verify(req.text)
    return {
        "results": [
            {"claim": r.claim, "status": r.status, "confidence": r.confidence,
             "evidence": r.evidence, "sources": r.sources}
            for r in results
        ],
        "summary": {
            "total": len(results),
            "verified": sum(1 for r in results if r.status == "verified"),
            "unverified": sum(1 for r in results if r.status == "unverified"),
            "conflicting": sum(1 for r in results if r.status == "conflicting"),
        }
    }

@app.get("/api/health")
def health():
    return {"status": "ok"}
