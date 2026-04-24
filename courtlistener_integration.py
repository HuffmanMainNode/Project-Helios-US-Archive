import requests
import json
import os
import time
import re

class CourtListenerClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('COURTLISTENER_API_KEY')
        if not self.api_key:
            raise ValueError("CourtListener API key is required. Set it via initialization or 'COURTLISTENER_API_KEY' environment variable.")
        self.base_url = 'https://www.courtlistener.com/api/rest/v3'
        self.headers = {
            'Authorization': f'Token {self.api_key}',
            'User-Agent': 'Project-Helios-Archive-Bot/1.0'
        }

    def search_cases(self, query, max_results=10):
        endpoint = f'{self.base_url}/search/'
        params = {'q': query}
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status() # Raise exception for 4xx/5xx status codes
            data = response.json()
            return data.get('results', [])[:max_results]
            
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            if status_code == 429:
                print(f"Rate limit exceeded: {e}. Consider adding exponential backoff.")
            elif status_code in (401, 403):
                print(f"Authentication error: {e}. Check your API key.")
            else:
                print(f"HTTP error occurred: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Network error occurred: {e}")
            return None
        except ValueError as e:
             print(f"Error parsing JSON response: {e}")
             return None

    def parse_case_data(self, case):
        parsed_data = {
            'case_name': case.get('caseName', 'Unknown Case'),
            'date_filed': case.get('dateFiled', 'Unknown Date'),
            'court': case.get('court', 'Unknown Court'),
            'snippet': self._clean_snippet(case.get('snippet', 'No summary available.')),
            'url': f"https://www.courtlistener.com{case.get('absolute_url', '')}"
        }
        return parsed_data
        
    def _clean_snippet(self, snippet):
        # Basic cleanup of highlighted snippets
        return snippet.replace('<em>', '**').replace('</em>', '**')

# Example usage (commented out to prevent execution without a key)
# if __name__ == '__main__':
#     try:
#         # client = CourtListenerClient(api_key='YOUR_API_KEY_HERE') 
#         client = CourtListenerClient()
#         results = client.search_cases('civil rights', max_results=2)
#         if results:
#             for case in results:
#                 parsed = client.parse_case_data(case)
#                 print(json.dumps(parsed, indent=2))
#     except ValueError as e:
#         print(e)
