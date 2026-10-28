# TruthLens Crew

TruthLens Crew is a fact-checking multi agentic system, which utilises adversarial research agents, structured verdicts, and presents an evidence dashboard.

## What It Demonstrates

- Multi-agent workflow design with supporter, skeptic, verifier, and report writer roles.
- Structured verdict handling with confidence, abstention, and benchmark metrics.

The dashboard presents an **Evidence Courtroom**: a supporter and skeptic argue each side of the claim, then a lead verifier issues `CONFIRMED`, `CONTRADICTED`, or `NEEDS_MORE_INFO`. The benchmark also reports an abstention rate, so uncertainty is measured instead of hidden.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
make demo
```

## Commands

```bash
truthlens verify "Pakistan gained independence in 1947."
truthlens benchmark data/sample/claims.csv
truthlens dashboard
```

Install the dashboard extra first when using Streamlit: `pip install -e ".[ui]"`.

## Repository Layout

```text
src/truthlens_crew/   package code
tests/                unit tests for verdicts, search fixtures, and crew flow
data/sample/          benchmark claims for offline demos
docs/                 architecture and project notes
scripts/              demo automation
```

## Architecture

```text
claim
  -> supporter search agent
  -> skeptic search agent
  -> lead verifier with structured verdict
  -> report writer
  -> benchmark metrics: accuracy, latency, search count, abstention rate
```

## Publishing Checklist

- Rotate any API keys that previously appeared in notebooks before sharing publicly.
- Keep `.env` local and commit only `.env.example`.
- Run `make test` and `make lint` before pushing.

## CV Summary

Built an adversarial fact-checking system with Gemini agents, supporter/skeptic evidence retrieval, structured verdict parsing, uncertainty-aware abstention, benchmark comparisons against simpler baselines, CLI tooling, and a Streamlit Evidence Courtroom dashboard.
