from __future__ import annotations

import csv
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from truthlens_crew.config import Settings
from truthlens_crew.graphs import FactCheckCrew
from truthlens_crew.models import GeminiClient
from truthlens_crew.schemas import normalize_binary_verdict
from truthlens_crew.tools import SearchQuery, TavilySearchEngine


@dataclass(frozen=True)
class BenchmarkRow:
    claim: str
    ground_truth: str
    method: str
    prediction: str
    correct: bool
    latency_seconds: float
    search_count: int
    abstained: bool


def zero_shot(claim: str, settings: Settings) -> str:
    raw = GeminiClient(settings).generate(
        "You are a fact-checker. Respond with only True or False.\n"
        f"Claim: {claim}"
    )
    return "True" if "true" in raw.lower() else "False"


def simple_search(claim: str, settings: Settings) -> str:
    search = TavilySearchEngine(settings)
    evidence = search.search(SearchQuery(claim=claim, stance="support"))
    counter = search.search(SearchQuery(claim=claim, stance="counter"))
    if evidence and not counter:
        return "True"
    if counter and not evidence:
        return "False"
    return "Other"


def run_benchmark(path: str | Path, settings: Settings) -> list[BenchmarkRow]:
    with Path(path).open(newline="", encoding="utf-8") as handle:
        claims = [dict(row) for row in csv.DictReader(handle)]

    crew = FactCheckCrew(settings)
    rows: list[BenchmarkRow] = []

    for item in claims:
        claim = item["claim"]
        ground_truth = item["ground_truth"].lower()

        for method_name, runner in [
            ("zero_shot", lambda: zero_shot(claim, settings)),
            ("simple_search", lambda: simple_search(claim, settings)),
        ]:
            start = time.perf_counter()
            prediction = normalize_binary_verdict(runner())
            latency = time.perf_counter() - start
            rows.append(
                BenchmarkRow(
                    claim=claim,
                    ground_truth=ground_truth,
                    method=method_name,
                    prediction=prediction,
                    correct=prediction == ground_truth,
                    latency_seconds=latency,
                    search_count=0 if method_name == "zero_shot" else 2,
                    abstained=prediction == "other",
                )
            )

        start = time.perf_counter()
        result = crew.verify(claim)
        prediction = normalize_binary_verdict(result.verdict.value)
        rows.append(
            BenchmarkRow(
                claim=claim,
                ground_truth=ground_truth,
                method="crew",
                prediction=prediction,
                correct=prediction == ground_truth,
                latency_seconds=time.perf_counter() - start,
                search_count=2 * result.loops,
                abstained=prediction == "other",
            )
        )

    return rows


def write_benchmark(rows: list[BenchmarkRow], path: str | Path) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)

