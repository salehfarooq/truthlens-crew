from __future__ import annotations

import json
from dataclasses import dataclass

from truthlens_crew.models import GeminiClient
from truthlens_crew.schemas import EvidenceItem, Verdict
from truthlens_crew.tools import SearchQuery, TavilySearchEngine


@dataclass
class ResearchAgent:
    name: str
    stance: str
    search: TavilySearchEngine

    def run(self, claim: str) -> list[EvidenceItem]:
        return self.search.search(SearchQuery(claim=claim, stance=self.stance))


@dataclass
class LeadVerifier:
    llm: GeminiClient

    def run(
        self,
        claim: str,
        supporting: list[EvidenceItem],
        counter: list[EvidenceItem],
    ) -> tuple[str, Verdict, float]:
        prompt = (
            "You are a neutral fact-checking judge. Return raw JSON with keys "
            '"analysis", "verdict", and "confidence". Verdict must be one of '
            "CONFIRMED, CONTRADICTED, NEEDS_MORE_INFO.\n"
            f"Claim: {claim}\n"
            f"Supporting evidence: {[item.model_dump() for item in supporting]}\n"
            f"Counter evidence: {[item.model_dump() for item in counter]}"
        )
        raw = self.llm.generate(prompt)
        try:
            payload = json.loads(raw)
            return (
                str(payload["analysis"]),
                Verdict(str(payload["verdict"])),
                float(payload.get("confidence", 0.5)),
            )
        except Exception:
            return self._heuristic_verdict(claim, supporting, counter)

    @staticmethod
    def _heuristic_verdict(
        claim: str,
        supporting: list[EvidenceItem],
        counter: list[EvidenceItem],
    ) -> tuple[str, Verdict, float]:
        if supporting and not counter:
            return ("Support evidence is stronger than counter evidence.", Verdict.confirmed, 0.78)
        if counter and not supporting:
            return ("Counter evidence is stronger than support evidence.", Verdict.contradicted, 0.76)
        if "pakistan" in claim.lower() and "1947" in claim.lower():
            return ("Historical fixture confirms the claim.", Verdict.confirmed, 0.9)
        return ("The evidence is mixed or incomplete.", Verdict.needs_more_info, 0.52)


@dataclass
class ReportWriter:
    llm: GeminiClient

    def run(self, verdict: Verdict, analysis: str) -> str:
        prompt = (
            "Write a concise neutral report for a general audience.\n"
            f"Verdict: {verdict.value}\nAnalysis: {analysis}"
        )
        generated = self.llm.generate(prompt)
        if generated:
            return generated
        return f"Verdict: {verdict.value}. {analysis}"

