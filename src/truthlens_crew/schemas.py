from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class Verdict(str, Enum):
    confirmed = "CONFIRMED"
    contradicted = "CONTRADICTED"
    needs_more_info = "NEEDS_MORE_INFO"


class EvidenceItem(BaseModel):
    title: str
    snippet: str
    url: str = "offline://fixture"
    stance: str = Field(pattern="^(support|counter)$")


class VerificationResult(BaseModel):
    claim: str
    supporting_evidence: list[EvidenceItem]
    counter_evidence: list[EvidenceItem]
    analysis: str
    verdict: Verdict
    confidence: float = Field(ge=0.0, le=1.0)
    final_report: str
    loops: int


def normalize_binary_verdict(value: str) -> str:
    normalized = value.strip().lower()
    if normalized in {"true", "confirmed", Verdict.confirmed.value.lower()}:
        return "true"
    if normalized in {"false", "contradicted", Verdict.contradicted.value.lower()}:
        return "false"
    return "other"

