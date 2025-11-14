from typing import Any, TypeAlias

from .base import BaseAPI


Sound: TypeAlias = dict[str, Any]
SoundList: TypeAlias = list[Sound]


class Sounds(BaseAPI):
    def __init__(self, send_request):
        super().__init__(send_request)

    async def list(
        self, lang: str | None = None, file_format: str | None = None
    ) -> SoundList:
        """List all sounds.

        :param lang: string - Lookup sound for a specific language.
        :param file_format: string - Lookup sound in a specific format.
        """

        query_params: dict[str, str] = {}

        if lang:
            query_params["lang"] = lang

        if file_format:
            query_params["format"] = file_format

        uri = self._build_uri("sounds", query_params)
        result = await self.send_request(method="GET", uri=uri)
        return self.parse_body(result.get("message_body"))

    async def get(self, sound_id: str) -> Sound:
        """Get a Sound.

        :param sound_id: string - (required) Sound Id.
        """

        result = await self.send_request(method="GET", uri=f"sounds/{sound_id}")
        return self.parse_body(result.get("message_body"))
