import unittest
from unittest.mock import Mock, patch

import requests

from courtlistener_integration import CourtListenerClient


class CourtListenerTests(unittest.TestCase):
    def test_requires_api_key(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaisesRegex(ValueError, "COURTLISTENER_API_KEY"):
                CourtListenerClient()

    def test_search_uses_timeout_and_bounds_results(self):
        client = CourtListenerClient(api_key="test-token")
        response = Mock()
        response.json.return_value = {
            "results": [{"caseName": "A"}, {"caseName": "B"}, {"caseName": "C"}]
        }
        with patch("courtlistener_integration.requests.get", return_value=response) as get:
            result = client.search_cases("civil rights", max_results=2)

        self.assertEqual(len(result), 2)
        self.assertEqual(get.call_args.kwargs["timeout"], (5, 20))
        self.assertEqual(get.call_args.kwargs["headers"]["Authorization"], "Token test-token")

    def test_rejects_bad_query_and_result_limit(self):
        client = CourtListenerClient(api_key="test-token")
        with self.assertRaises(ValueError):
            client.search_cases(" ")
        with self.assertRaises(ValueError):
            client.search_cases("case", max_results=1000)
        with self.assertRaises(ValueError):
            client.search_cases("case", max_results=True)

    def test_rejects_unexpected_api_shapes(self):
        client = CourtListenerClient(api_key="test-token")
        response = Mock()
        response.json.return_value = ["not", "an", "object"]
        with patch("courtlistener_integration.requests.get", return_value=response):
            self.assertIsNone(client.search_cases("case"))

    def test_handles_http_and_network_errors_without_printing_secrets(self):
        client = CourtListenerClient(api_key="do-not-log-this")
        response = Mock()
        response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=Mock(status_code=401)
        )
        with patch("courtlistener_integration.requests.get", return_value=response):
            self.assertIsNone(client.search_cases("case"))

        with patch(
            "courtlistener_integration.requests.get",
            side_effect=requests.exceptions.Timeout("private detail"),
        ):
            self.assertIsNone(client.search_cases("case"))

    def test_parse_case_data_rejects_external_urls_and_strips_markup(self):
        client = CourtListenerClient(api_key="test-token")
        parsed = client.parse_case_data({
            "caseName": "Example <script>alert(1)</script> Case",
            "dateFiled": "2026-01-01",
            "court": "Test <b>Court</b>",
            "snippet": "Text <em>highlighted</em> &amp; reviewed",
            "absolute_url": "/opinion/123/example/",
        })
        self.assertEqual(parsed["url"], "https://www.courtlistener.com/opinion/123/example/")
        self.assertNotIn("<script>", parsed["case_name"])
        self.assertNotIn("<em>", parsed["snippet"])
        self.assertIn("&amp;", parsed["snippet"])
        self.assertIsNone(client.parse_case_data({
            "absolute_url": "https://evil.example/phishing"
        }))
        self.assertIsNone(client.parse_case_data({
            "absolute_url": "//evil.example/phishing"
        }))


if __name__ == "__main__":
    unittest.main()
