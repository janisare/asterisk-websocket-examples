from api.base import BaseAPI


class Playbacks(BaseAPI):
    def __init__(self, send_request):
        super().__init__(send_request)

    async def get(self, playback_id: str) -> dict:
        """Get a playback.

        :param playback_id: string - (required) Playback Id.
        """

        result = await self.send_request(method="GET", uri=f"playbacks/{playback_id}")
        return self.parse_body(result.get("message_body"))

    async def control(self, playback_id: str, operation: str) -> dict:
        """Control a playback.

        :param playback_id: string - (required) Playback Id.
        :param operation: string - (required) Operation to perform on the playback.
        Allowed values: restart, pause, unpause, reverse, forward
        """

        await self.send_request(
            method="POST", uri=f"playbacks/{playback_id}/control?operation={operation}"
        )

    async def stop(self, playback_id: str) -> None:
        """Stop a playback.

        :param playback_id: string - (required) Playback Id.
        """

        await self.send_request(method="DELETE", uri=f"playbacks/{playback_id}")
