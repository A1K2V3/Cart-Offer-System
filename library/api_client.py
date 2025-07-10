import logging
import os
import posixpath
import requests
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url if base_url else os.getenv("BASE_URL", "http://localhost:9001")
        logger.info(f"APIClient initialized with base_url: {base_url}")

    def _build_url(self, *segments: str) -> str:
        path = posixpath.join(*segments)
        url = urljoin(self.base_url, path)
        logger.debug(f"Built URL: {url}")
        return url

    def _request(self, method: str, endpoint, **kwargs):
        if isinstance(endpoint, (list, tuple)):
            endpoint = [i.strip("/") for i in endpoint]
            url = self._build_url(*endpoint)
        elif isinstance(endpoint, str):
            url = self._build_url(endpoint.strip("/"))
        else:
            raise ValueError(f"endpoint: {endpoint} is not valid")
        logger.info(f"{method} Request to {url} with kwargs: {kwargs}")
        response = requests.request(method=method, url=url, **kwargs)
        logger.info(f"Response: {response.status_code} - {response.text}")
        return response

    def get(self, endpoint, **kwargs):
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self._request("POST", endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self._request("PUT", endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self._request("DELETE", endpoint, **kwargs)