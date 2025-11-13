import json
from typing import Any


class BaseAPI:
    def __init__(self, send_request):
        self.send_request = send_request

    @staticmethod
    def parse_body(body: str) -> Any:
        if not body:
            return None
        return json.loads(body)
