"""
    📋 Problem Statement
    Given a URL, fetch its content efficiently and print it.

    Must handle:
        - Connection issues (timeouts).

        - Temporary failures (retry with backoff).

        - Repeated requests (session pooling).

    📄 Example
        Suppose URL:
        https://example.com/data

        Requirements:
            Set a reasonable timeout (e.g., 5 seconds).

            If fails (network glitch), retry (up to 3 retries) with backoff (waits between tries).

            Reuse connections (don't open a new TCP connection for each request).
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class URLFetcher:
    def __init__(self, timeout=5, retries=3, backoff_factor=0.3):
        self.timeout = timeout
        self.retries = retries
        self.backoff_factor = backoff_factor
        self.session = self._init_session()

    def _init_session(self):
        session = requests.Session()

        # Define retry strategy
        retry_strategy = Retry(
            total=self.retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=[409, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )

        # Mount HttpAdapter with retry_strategy to session
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount(prefix="http://", adapter=adapter)
        session.mount(prefix="https://", adapter=adapter)

        return session

    def fetch(self, url):
        try:
            response = self.session.get(url=url, timeout=self.timeout)
            # Raise exception for HTTP errors (4xx, 5xx)
            response.raise_for_status()

            return response.text
        except requests.RequestException as e:
            print(f"Failed to fetch {url}: {e}")
            return None


# Example usage
if __name__ == "__main__":
    fetcher = URLFetcher(timeout=5, retries=3, backoff_factor=0.5)
    content = fetcher.fetch("https://www.google.com")
    if content:
        print("Fetched Content:", content)
