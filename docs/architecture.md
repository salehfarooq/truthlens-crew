# Architecture

TruthLens Crew uses a small deterministic search fixture for demos and tests, with an optional Tavily adapter for live web evidence. Gemini is the default model when `GOOGLE_API_KEY` is present. Without a key, an offline fixture keeps the CLI, dashboard, and benchmark runnable.

The workflow has four roles: supporter, skeptic, lead verifier, and report writer. The verifier emits a structured verdict so downstream evaluation can compare `CONFIRMED`, `CONTRADICTED`, and `NEEDS_MORE_INFO` consistently.

