from typing import Any, TypeAlias

from .base import BaseAPI

StoredRecording: TypeAlias = dict[str, Any]
LiveRecording: TypeAlias = dict[str, Any]
RecordingList: TypeAlias = list[StoredRecording]


class Recordings(BaseAPI):
    def __init__(self, send_request):
        super().__init__(send_request)

    async def list(self) -> RecordingList:
        """List recordings that are complete."""

        result = await self.send_request(method="GET", uri="recordings/stored")
        return self.parse_body(result.get("message_body"))

    async def get(self, name: str) -> StoredRecording:
        """Get a stored recording's details.

        :param name: string - (required) The name of the recording
        """

        result = await self.send_request(method="GET", uri=f"recordings/stored/{name}")
        return self.parse_body(result.get("message_body"))

    async def copy(self, name: str, destination: str) -> StoredRecording:
        """Copy a stored recording.

        :param name: string - (required) The name of the recording
        :param destination: string - (required) The destination name of the recording
        """

        query_params: dict[str, str] = {"destinationRecordingName": destination}
        uri = self._build_uri(f"recordings/stored/{name}/copy", query_params)
        result = await self.send_request(method="POST", uri=uri)
        return self.parse_body(result.get("message_body"))

    async def get_file(self, name: str) -> str:
        """Get the file associated with the stored recording.

        :param name: string - (required) The name of the recording
        """

        result = await self.send_request(
            method="GET", uri=f"recordings/stored/{name}/file"
        )
        return self.parse_body(result.get("message_body"))

    async def delete(self, name: str) -> None:
        """Delete a stored recording.

        :param name: string - (required) The name of the recording
        """

        await self.send_request(method="DELETE", uri=f"recordings/stored/{name}")

    async def get_live(self, name: str) -> LiveRecording:
        """Get a stored recording's details.

        :param name: string - (required) The name of the recording
        """

        result = await self.send_request(method="GET", uri=f"recordings/live/{name}")

        return self.parse_body(result.get("message_body"))

    async def cancel(self, name: str) -> None:
        """Stop a live recording and discard it.

        :param name: string - (required) The name of the recording
        """

        await self.send_request(method="DELETE", uri=f"recordings/live/{name}")

    async def stop(self, name: str) -> None:
        """Stop a live recording and store it.

        :param name: string - (required) The name of the recording
        """

        await self.send_request(method="POST", uri=f"recordings/live/{name}/stop")

    async def pause(self, name: str) -> None:
        """Pause a live recording. Pausing a recording suspends silence detection,
        which will be restarted when the recording is unpaused. Paused time is not
        included in the accounting for maxDurationSeconds.

        :param name: string - (required) The name of the recording
        """

        await self.send_request(method="POST", uri=f"recordings/live/{name}/pause")

    async def unpause(self, name: str) -> None:
        """Unpause a live recording.

        :param name: string - (required) The name of the recording
        """

        await self.send_request(method="DELETE", uri=f"recordings/live/{name}/pause")

    async def mute(self, name: str) -> None:
        """Mute a live recording. Muting a recording suspends silence detection,
        which will be restarted when the recording is unmuted.

        :param name: string - (required) The name of the recording
        """

        await self.send_request(method="POST", uri=f"recordings/live/{name}/mute")

    async def unmute(self, name: str) -> None:
        """Mute a live recording. Muting a recording suspends silence detection,
        which will be restarted when the recording is unmuted.

        :param name: string - (required) The name of the recording
        """

        await self.send_request(method="DELETE", uri=f"recordings/live/{name}/mute")
