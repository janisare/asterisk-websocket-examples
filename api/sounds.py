from api.base import BaseAPI


class Sounds(BaseAPI):
    def __init__(self, send_request):
        super().__init__(send_request)

    async def list(
        self, lang: str | None = None, format: str | None = None
    ) -> list[dict]:
        """List all sounds."""

        uri = "sounds"

        if lang:
            uri += f"?lang={lang}"

        if format:
            if lang:
                uri += f"&format={format}"
            else:
                uri += f"?format={format}"

        result = await self.send_request(method="GET", uri=uri)
        return self.parse_body(result.get('message_body'))

    async def get(self, sound_id: str) -> dict:
        """Get a Sound.

        :param sound_id: string - (required) Sound Id.
        """

        result = await self.send_request(
            method="GET",
            uri=f"sounds/{sound_id}"
        )
        return self.parse_body(result.get('message_body'))
