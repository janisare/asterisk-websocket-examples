from api.base import BaseAPI


class Bridges(BaseAPI):
    def __init__(self, send_request):
        super().__init__(send_request)

    async def list(self) -> list[dict]:
        """List all bridges."""

        result = await self.send_request(
            method="GET",
            uri="bridges"
        )
        return self.parse_body(result.get('message_body'))

    async def create(
            self,
            bridge_id: str | None = None,
            name: str | None = None,
            bridge_type: str = "mixing"
    ) -> dict:
        """
        Create a bridge.

        :param bridge_id: string - (Optional) Bridge ID
        :param name: string - (Optional) Name
        :param bridge_type: string - (Optional) Bridge Type
        """

        uri = f"bridges?type={bridge_type}"

        if bridge_id:
            uri = f"bridges/{bridge_id}?type={bridge_type}"

        if name:
            uri += f"&name={name}"

        result = await self.send_request(
            method="POST",
            uri=uri,
        )
        return self.parse_body(result.get('message_body'))

    async def get(self, bridge_id: str) -> dict:
        """
        Get a bridge.

        :param bridge_id: string - (required) Bridge ID
        """
        result = await self.send_request(
            method="GET",
            uri=f"bridges/{bridge_id}"
        )
        return self.parse_body(result.get('message_body'))

    async def delete(self, bridge_id: str) -> None:
        """
        Delete a bridge.

        :param bridge_id: string - (required) Bridge ID
        """
        await self.send_request(method="DELETE", uri=f"bridges/{bridge_id}")

    async def add_channel(
            self,
            bridge_id: str,
            channel: str,
            role: str | None = None,
            absorbDTMF: bool = False,
            mute: bool = False,
            inhibitConnectedLineUpdates: bool = False
    ) -> None:
        """
        Add a channel/-s to the bridge.

        :param bridge_id: string - (required) Bridge ID
        :param channel: string - (required) Ids of channels to add to bridge; Allows comma separated values.
        :param role: string - Channel's role in the bridge.
        :param absorbDTMF: boolean - Absorb DTMF coming from this channel, preventing it to pass through to the bridge
        :param mute: boolean - Mute audio from this channel, preventing it to pass through to the bridge
        :param inhibitConnectedLineUpdates: boolean - Do not present the identity of the newly connected channel to other bridge members
        """

        uri = f"bridges/{bridge_id}/addChannel?channel={channel}"
        if role:
            uri += f"&role={role}"

        if absorbDTMF:
            uri += f"&absorbDTMF={absorbDTMF}"

        if mute:
            uri += f"&mute={mute}"

        if inhibitConnectedLineUpdates:
            uri += f"&inhibitConnectedLineUpdates={inhibitConnectedLineUpdates}"

        await self.send_request(method="POST", uri=uri)

    async def remove_channel(self, bridge_id: str, channel: str) -> None:
        """
        Remove a channel/-s from the bridge.

        :param bridge_id: string - (required) Bridge ID
        :param channel: string - (required) Ids of channels to add to bridge; Allows comma separated values.
        """
        await self.send_request(
            method="POST",
            uri=f"bridges/{bridge_id}/removeChannel?channel={channel}"
        )

    async def start_moh(self, bridge_id: str, mohClass: str) -> None:
        """Start playing music on hold on the bridge.

        :param bridge_id: string - (required) Bridge Id.
        :param mohClass: string - (required) Moh class.
        """
        await self.send_request(
            method="POST", uri=f"bridges/{bridge_id}/moh?mohClass={mohClass}"
        )

    async def stop_moh(self, bridge_id: str) -> None:
        """Stop playing music on hold on the bridge.

        :param bridge_id: string - (required) Bridge Id.
        """
        await self.send_request(method="DELETE", uri=f"bridges/{bridge_id}/moh")

    async def play(
            self,
            bridge_id: str,
            media: str,
            announcer_format: str = None,
            lang: str = None,
            offsetms: int = None,
            skipms: int = 3000,
            playbackId: str = None
    ) -> None:
        """
        Start playback of media on a bridge. The media URI may be any of a number
        of URI's. Currently sound:, recording:, number:, digits:, characters:, and
        tone: URI's are supported. This operation creates a playback resource that can
        be used to control the playback of media (pause, rewind, fast forward, etc.)

        :param bridge_id: string - (required) Bridge Id.
        :param media: string - (required) Media URIs to play.
        Allows comma separated values.
        :param announcer_format: string - Format of the 'Anouncer' channel attached to
        the bridge. Defaults to the format of the channel in the bridge with the
        highest sample rate.
        :param lang: string - For sounds, selects language for sound.
        :param offsetms: int - Number of milliseconds to skip before playing. Only
        applies to the first URI if multiple media URIs are specified.
        Allowed range: Min: 0; Max: None
        :param skipms: int - Number of milliseconds to skip for forward/reverse
        operations.
        Default: 3000
        Allowed range: Min: 0; Max: None
        :param playbackId: string - Playback Id.
        """

        uri = f"bridges/{bridge_id}/play?media={media}"

        if announcer_format:
            uri += f"&announcer_format={announcer_format}"

        if lang:
            uri += f"&lang={lang}"

        if offsetms:
            uri += f"&offsetms={offsetms}"

        if skipms:
            uri += f"&skipms={skipms}"

        if playbackId:
            uri += f"&playbackId={playbackId}"

        await self.send_request(method="POST", uri=uri)

    async def play_with_id(
            self,
            bridge_id: str,
            playbackId: str,
            media: str,
            announcer_format: str = None,
            lang: str = None,
            offsetms: int = None,
            skipms: int = 3000
    ) -> dict:
        """
        Start playback of media on a bridge. The media URI may be any of a number of
        URI's. Currently sound:, recording:, number:, digits:, characters:, and
        tone: URI's are supported. This operation creates a playback resource that can
        be used to control the playback of media (pause, rewind, fast forward, etc.)

        :param bridge_id: string - (required) Bridge Id.
        :param media: string - (required) Media URIs to play.
        :param playbackId: string - (required) Playback Id.
        Allows comma separated values.
        :param announcer_format: string - Format of the 'Anouncer' channel attached to
        the bridge. Defaults to the format of the channel in the bridge with the
        highest sample rate.
        :param lang: string - For sounds, selects language for sound.
        :param offsetms: int - Number of milliseconds to skip before playing. Only
        applies to the first URI if multiple media URIs are specified.
        Allowed range: Min: 0; Max: None
        :param skipms: int - Number of milliseconds to skip for forward/reverse
        operations.
        Default: 3000
        Allowed range: Min: 0; Max: None
        """

        uri = f"bridges/{bridge_id}/play/{playbackId}?media={media}"

        if announcer_format:
            uri += f"&announcer_format={announcer_format}"

        if lang:
            uri += f"&lang={lang}"

        if offsetms:
            uri += f"&offsetms={offsetms}"

        if skipms:
            uri += f"&skipms={skipms}"

        result = await self.send_request(method="POST", uri=uri)
        return self.parse_body(result.get('message_body'))

    async def record(
            self,
            bridge_id: str,
            name: str,
            format: str,
            recorder_format: str | None = None,
            maxDurationSeconds: int = 0,
            maxSilenceSeconds: int = 0,
            ifExists: str = "fail",
            beep: bool = False,
            terminateOn: str = "none"

    ) -> dict:
        """Start a recording. This records the mixed audio from all channels participating in this bridge.

        :param name: string - (required) Recording's filename
        :param format: string - (required) Format to encode audio in
        :param recorder_format: string - Format of the 'Recorder' channel attached to the bridge. Defaults to the same format as the 'format' parameter.
        :param maxDurationSeconds: int - Maximum duration of the recording, in seconds. 0 for no limit.
        Allowed range: Min: 0; Max: None
        :param maxSilenceSeconds: int - Maximum duration of silence, in seconds. 0 for no limit.
        Allowed range: Min: 0; Max: None
        :param ifExists: string - Action to take if a recording with the same name already exists.
        Default: fail
        Allowed values: fail, overwrite, append
        :param beep: boolean - Play beep when recording begins
        :param terminateOn: string - DTMF input to terminate recording.
        Default: none
        Allowed values: none, any, *, #
        """

        uri = f"bridges/{bridge_id}/record?name={name}&format={format}"
        if recorder_format:
            uri += f"&recorder_format={recorder_format}"
        else:
            uri += f"&recorder_format={format}"

        if maxDurationSeconds:
            uri += f"&maxDurationSeconds={maxDurationSeconds}"

        if maxSilenceSeconds:
            uri += f"&maxSilenceSeconds={maxSilenceSeconds}"

        if ifExists:
            uri += f"&ifExists={ifExists}"

        if beep:
            uri += f"&beep={beep}"

        if terminateOn:
            uri += f"&terminateOn={terminateOn}"

        result = await self.send_request(method="POST", uri=uri)
        return self.parse_body(result.get('message_body'))

    def set_video_source(self, bridge_id: int) -> NotImplementedError:
        raise NotImplementedError()

    def clear_video_source(self, bridge_id: int) -> NotImplementedError:
        raise NotImplementedError()
