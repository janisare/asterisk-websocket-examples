import json
from urllib.parse import urlencode

from typing import Any


class BaseAPI:
    def __init__(self, send_request):
        self.send_request = send_request

    @staticmethod
    def parse_body(body: str) -> Any:
        if not body:
            return None
        return json.loads(body)

    @staticmethod
    def _build_uri(path: str, query_params: dict | None = None) -> str:
        """
        Build a URI with query parameters, skipping empty dictionaries.
        Assumes all values in query_params are already correctly formatted strings.
        """
        if not query_params:
            return path
        return f"{path}?{urlencode(query_params)}"

    def process_result(self, result: dict) -> dict:
        return self.parse_body(result.get("message_body"))
