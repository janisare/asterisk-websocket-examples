from typing import Any, TypeAlias

from .base import BaseAPI

Playback: TypeAlias = dict[str, Any]


class Playbacks(BaseAPI):
    def __init__(self, send_request):
        super().__init__(send_request)

    def get(self, playback_id: str) -> Playback:
        """Get a playback.

        :param playback_id: string - (required) Playback Id.
        """

        df = self.send_request(method="GET", uri=f"playbacks/{playback_id}")
        df.addCallback(self.process_result)
        return df

    def control(self, playback_id: str, operation: str) -> None:
        """Control a playback.

        :param playback_id: string - (required) Playback Id.
        :param operation: string - (required) Operation to perform on the playback.
        Allowed values: restart, pause, unpause, reverse, forward
        """

        query_params: dict[str, str] = {"operation": operation}
        uri = self._build_uri(f"playbacks/{playback_id}/control", query_params)
        self.send_request(method="POST", uri=uri)

    def stop(self, playback_id: str) -> None:
        """Stop a playback.

        :param playback_id: string - (required) Playback Id.
        """

        self.send_request(method="DELETE", uri=f"playbacks/{playback_id}")
