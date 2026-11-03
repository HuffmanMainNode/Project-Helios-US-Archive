"""Optional, read-only CourtListener case-search client.

The wrapper does not download or archive opinions. API responses are untrusted
input and must be reviewed against the official case record before citation.
"""
from __future__ import annotations

import html
import logging
import os
from html.parser import HTMLParser
from urllib.parse import urlsplit, urljoin

import requests

logger = logging.getLogger(__name__)


class _TextOnlyParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


class CourtListenerClient:
    BASE_URL = "https://www.courtlistener.com/api/rest/v3"
    SITE_ORIGIN = "https://www.courtlistener.com"

    def __init__(self, api_key=None, timeout=(5, 20)):
        self.api_key = api_key or os.environ.get("COURTLISTENER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "CourtListener API key is required. Set COURTLISTENER_API_KEY."
            )
        if (
            not isinstance(timeout, tuple)
            or len(timeout) != 2
            or any(not isinstance(value, (int, float)) or value <= 0 for value in timeout)
        ):
            raise ValueError("timeout must be a pair of positive connect/read seconds")
        self.timeout = timeout
        self.headers = {
            "Authorization": f"Token {self.api_key}",
            "Accept": "application/json",
            "User-Agent": "Project-Helios-Archive/1.1",
        }

    def search_cases(self, query, max_results=10):
        if not isinstance(query, str) or not query.strip() or len(query) > 500:
            raise ValueError("query must be a non-empty string of at most 500 characters")
        if not isinstance(max_results, int) or isinstance(max_results, bool) or not 1 <= max_results <= 100:
            raise ValueError("max_results must be an integer between 1 and 100")

        try:
            response = requests.get(
                f"{self.BASE_URL}/search/",
                headers=self.headers,
                params={"q": query.strip()},
                timeout=self.timeout,
            )
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, dict) or not isinstance(payload.get("results"), list):
                logger.warning("CourtListener returned an unexpected response shape.")
                return None
            return [
                item for item in payload["results"] if isinstance(item, dict)
            ][:max_results]
        except requests.exceptions.HTTPError as error:
            status = error.response.status_code if error.response is not None else None
            if status == 429:
                logger.warning("CourtListener rate limit reached.")
            elif status in (401, 403):
                logger.warning("CourtListener authentication or authorization failed.")
            else:
                logger.error("CourtListener HTTP request failed with status %s.", status)
            return None
        except (requests.exceptions.RequestException, ValueError) as error:
            logger.error("CourtListener request failed: %s", type(error).__name__)
            return None

    def parse_case_data(self, case):
        if not isinstance(case, dict):
            return None
        relative_url = case.get("absolute_url")
        if (
            not isinstance(relative_url, str)
            or not relative_url.startswith("/")
            or relative_url.startswith("//")
            or "\\" in relative_url
        ):
            return None
        parsed = urlsplit(relative_url)
        if parsed.scheme or parsed.netloc:
            return None

        return {
            "case_name": self._plain_text(case.get("caseName"), 1000) or "Unknown Case",
            "date_filed": self._plain_text(case.get("dateFiled"), 100) or "Unknown Date",
            "court": self._plain_text(case.get("court"), 300) or "Unknown Court",
            "snippet": self._clean_snippet(case.get("snippet", "")),
            "url": urljoin(self.SITE_ORIGIN, relative_url),
        }

    @staticmethod
    def _plain_text(value, max_length):
        if not isinstance(value, str):
            return ""
        parser = _TextOnlyParser()
        parser.feed(value)
        parser.close()
        return html.escape(" ".join("".join(parser.parts).split())[:max_length])

    @classmethod
    def _clean_snippet(cls, snippet):
        return cls._plain_text(snippet, 10000)
