"""Main verification orchestrator."""
from parser import ClaimParser
from scorer import ClaimScorer
from dataclasses import dataclass

@dataclass
class VerificationResult:
    claim: str
    status: str          # "verified" | "unverified" | "conflicting"
    confidence: float
    evidence: list[str]
    sources: list[str]

class CitationVerifier:
    def __init__(self):
        self.parser = ClaimParser()
        self.scorer = ClaimScorer()

    def verify(self, text: str) -> list[VerificationResult]:
        claims = self.parser.extract_claims(text)
        results = []
        for claim_data in claims:
            result = self.scorer.score(claim_data["claim"])
            results.append(VerificationResult(
                claim=claim_data["claim"],
                status=result["status"],
                confidence=result["confidence"],
                evidence=result.get("evidence", []),
                sources=result.get("sources", [])
            ))
        return results
