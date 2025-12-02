"""Utilities to scrape basic Premier League schedule data from FBref."""
from __future__ import annotations

import random
import time
from typing import List, Dict

import pandas as pd
import requests
from requests import Response

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36",
]


class FBRefScrapeError(RuntimeError):
    """Raised when scraping FBref fails."""


def _build_schedule_url(season: str) -> str:
    sanitized = season.strip()
    slug = f"{sanitized}-Premier-League-Scores-and-Fixtures"
    return f"https://fbref.com/en/comps/9/{sanitized}/schedule/{slug}"


def _fetch_html(url: str, *, retries: int = 3, backoff: int = 5) -> str:
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            headers = {"User-Agent": random.choice(USER_AGENTS)}
            response: Response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            return response.text
        except Exception as exc:  # pragma: no cover - network failure branch
            last_error = exc
            if attempt < retries:
                time.sleep(backoff * attempt)
    raise FBRefScrapeError(f"Failed to fetch data from FBref: {last_error}")


def scrape_season_schedule(season: str) -> List[Dict[str, str]]:
    """Scrape the Premier League match schedule for a given season.

    Args:
        season: The season identifier in the format "YYYY-YYYY" (e.g., "2023-2024").

    Returns:
        A list of dictionaries describing each fixture (completed or scheduled).
    """

    if not season or "-" not in season:
        raise ValueError("Season must be provided in the format 'YYYY-YYYY'.")

    url = _build_schedule_url(season)
    html = _fetch_html(url)

    tables = pd.read_html(html)
    if not tables:
        raise FBRefScrapeError("Could not find any tables on the schedule page.")

    schedule = tables[0].fillna("")
    expected_columns = {"Date", "Round", "Home", "Away", "Score", "Venue"}
    missing_columns = expected_columns - set(schedule.columns)
    if missing_columns:
        raise FBRefScrapeError(
            f"Unexpected table format from FBref; missing columns: {', '.join(sorted(missing_columns))}"
        )

    results: List[Dict[str, str]] = []
    for _, row in schedule.iterrows():
        results.append(
            {
                "date": str(row.get("Date", "")),
                "round": str(row.get("Round", "")),
                "home": str(row.get("Home", "")),
                "away": str(row.get("Away", "")),
                "score": str(row.get("Score", "")),
                "venue": str(row.get("Venue", "")),
            }
        )

    return results


__all__ = ["scrape_season_schedule", "FBRefScrapeError"]
