from __future__ import annotations

from dataclasses import dataclass

from truthlens_crew.agents import LeadVerifier, ReportWriter, ResearchAgent
from truthlens_crew.config import Settings
from truthlens_crew.models import GeminiClient
from truthlens_crew.schemas import VerificationResult, Verdict
from truthlens_crew.tools import TavilySearchEngine


@dataclass
class FactCheckCrew:
    settings: Settings

    def __post_init__(self) -> None:
        search = TavilySearchEngine(self.settings)
        llm = GeminiClient(self.settings)
        self.supporter = ResearchAgent("supporter", "support", search)
        self.skeptic = ResearchAgent("skeptic", "counter", search)
        self.verifier = LeadVerifier(llm)
        self.writer = ReportWriter(llm)

    def verify(self, claim: str) -> VerificationResult:
        supporting = []
        counter = []
        analysis = ""
        verdict = Verdict.needs_more_info
        confidence = 0.0
        loops = 0

        while loops < self.settings.max_research_loops:
            loops += 1
            supporting = self.supporter.run(claim)
            counter = self.skeptic.run(claim)
            analysis, verdict, confidence = self.verifier.run(claim, supporting, counter)
            if verdict != Verdict.needs_more_info:
                break

        report = self.writer.run(verdict, analysis)
        return VerificationResult(
            claim=claim,
            supporting_evidence=supporting,
            counter_evidence=counter,
            analysis=analysis,
            verdict=verdict,
            confidence=confidence,
            final_report=report,
            loops=loops,
        )

