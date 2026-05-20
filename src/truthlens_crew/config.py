from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    google_api_key: str | None
    tavily_api_key: str | None
    gemini_model: str = "gemini-1.5-flash"
    rate_limit_sleep: float = 1.0
    max_research_loops: int = 2
    use_live_search: bool = False


def load_settings(env_file: str | Path | None = None) -> Settings:
    if env_file:
        load_dotenv(env_file)
    else:
        load_dotenv()

    return Settings(
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        tavily_api_key=os.getenv("TAVILY_API_KEY"),
        gemini_model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
        rate_limit_sleep=float(os.getenv("RATE_LIMIT_SLEEP", "1.0")),
        max_research_loops=int(os.getenv("MAX_RESEARCH_LOOPS", "2")),
        use_live_search=os.getenv("USE_LIVE_SEARCH", "false").lower() == "true",
    )

