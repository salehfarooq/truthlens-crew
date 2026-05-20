from __future__ import annotations

import argparse
from pathlib import Path

from truthlens_crew.config import load_settings
from truthlens_crew.evaluation import run_benchmark, write_benchmark
from truthlens_crew.graphs import FactCheckCrew


def _verify(args: argparse.Namespace) -> None:
    result = FactCheckCrew(load_settings()).verify(args.claim)
    print(f"Verdict: {result.verdict.value} ({result.confidence:.0%})")
    print(result.final_report)
    print("\nEvidence Courtroom")
    for item in result.supporting_evidence:
        print(f"- support | {item.title}: {item.snippet}")
    for item in result.counter_evidence:
        print(f"- counter | {item.title}: {item.snippet}")


def _benchmark(args: argparse.Namespace) -> None:
    rows = run_benchmark(args.claims, load_settings())
    write_benchmark(rows, args.output)
    accuracy = sum(row.correct for row in rows) / len(rows)
    abstention_rate = sum(row.abstained for row in rows) / len(rows)
    print(f"Wrote {len(rows)} rows -> {args.output}")
    print(f"accuracy={accuracy:.2%} abstention_rate={abstention_rate:.2%}")


def _dashboard(_: argparse.Namespace) -> None:
    import subprocess
    import sys

    subprocess.run([sys.executable, "-m", "streamlit", "run", "src/truthlens_crew/dashboard.py"], check=False)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="TruthLens Crew")
    subparsers = parser.add_subparsers(dest="command", required=True)

    verify = subparsers.add_parser("verify", help="Verify one claim.")
    verify.add_argument("claim")
    verify.set_defaults(func=_verify)

    benchmark = subparsers.add_parser("benchmark", help="Benchmark sample claims.")
    benchmark.add_argument("claims", type=Path, nargs="?", default=Path("data/sample/claims.csv"))
    benchmark.add_argument("--output", "-o", type=Path, default=Path("artifacts/benchmark.csv"))
    benchmark.set_defaults(func=_benchmark)

    dashboard = subparsers.add_parser("dashboard", help="Launch Streamlit dashboard.")
    dashboard.set_defaults(func=_dashboard)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
