from __future__ import annotations

from dataclasses import dataclass

from truthlens_crew.config import Settings
from truthlens_crew.schemas import EvidenceItem


@dataclass(frozen=True)
class SearchQuery:
    claim: str
    stance: str


class MockSearchEngine:
    def search(self, query: SearchQuery) -> list[EvidenceItem]:
        claim = query.claim.lower()
        support = query.stance == "support"

        if "pakistan" in claim and "1947" in claim:
            if support:
                return [
                    EvidenceItem(
                        title="Pakistan Independence",
                        snippet="Pakistan became independent in August 1947 after the end of British rule.",
                        stance="support",
                    )
                ]
            return []

        if "earth is flat" in claim:
            if support:
                return []
            return [
                EvidenceItem(
                    title="Earth Shape Evidence",
                    snippet="Satellite observations and circumnavigation contradict claims that Earth is flat.",
                    stance="counter",
                )
            ]

        if support:
            return [
                EvidenceItem(
                    title="Limited supporting fixture",
                    snippet=f"Some sources discuss the claim but do not conclusively prove it: {query.claim}",
                    stance="support",
                )
            ]
        return [
            EvidenceItem(
                title="Limited counter fixture",
                snippet=f"Some sources raise uncertainty around the claim: {query.claim}",
                stance="counter",
            )
        ]


class TavilySearchEngine:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._fallback = MockSearchEngine()

    def search(self, query: SearchQuery) -> list[EvidenceItem]:
        if not self.settings.use_live_search or not self.settings.tavily_api_key:
            return self._fallback.search(query)

        try:
            from tavily import TavilyClient

            client = TavilyClient(api_key=self.settings.tavily_api_key)
            response = client.search(
                query=f"{query.stance} evidence for claim: {query.claim}",
                max_results=4,
            )
            return [
                EvidenceItem(
                    title=item.get("title", "Untitled"),
                    snippet=item.get("content", ""),
                    url=item.get("url", "offline://missing-url"),
                    stance=query.stance,
                )
                for item in response.get("results", [])
            ]
        except Exception:
            return self._fallback.search(query)

