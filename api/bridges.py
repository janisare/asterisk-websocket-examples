from typing import Any, TypeAlias
from .base import BaseAPI

Bridge: TypeAlias = dict[str, Any]
BridgeList: TypeAlias = list[Bridge]
Playback: TypeAlias = dict[str, Any]
LiveRecording: TypeAlias = dict[str, Any]


class Bridges(BaseAPI):
    def __init__(self, send_request):
        super().__init__(send_request)

    def list(self) -> BridgeList:
        """List all bridges."""

        df = self.send_request(method="GET", uri="bridges")
        df.addCallback(lambda result: self.parse_body(result.get("message_body")))
        return df

    def create(
        self,
        bridge_id: str | None = None,
        name: str | None = None,
        bridge_type: str = "mixing",
    ) -> Bridge:
        """
        Create a bridge.

        :param bridge_id: string - (Optional) Bridge ID
        :param name: string - (Optional) Name
        :param bridge_type: string - (Optional) Bridge Type
        """

        query_params: dict[str, str] = {}
        if bridge_type:
            query_params["type"] = bridge_type
        if bridge_id:
            query_params["bridgeId"] = bridge_id
        if name:
            query_params["name"] = name

        uri = self._build_uri("bridges", query_params)
        df = self.send_request(method="POST", uri=uri)
        df.addCallback(lambda result: self.parse_body(result.get("message_body")))
        return df

    def create_with_id(
        self,
        bridge_id: str,
        name: str | None = None,
        bridge_type: str = "mixing",
    ) -> Bridge:
        """
        Create a bridge.

        :param bridge_id: string - (required) Bridge ID
        :param name: string - (Optional) Name
        :param bridge_type: string - (Optional) Bridge Type
        """

        query_params: dict[str, str] = {}
        if bridge_type:
            query_params["type"] = bridge_type
        if name:
            query_params["name"] = name

        uri = self._build_uri(f"bridges/{bridge_id}", query_params)
        df = self.send_request(method="POST", uri=uri)
        df.addCallback(lambda result: self.parse_body(result.get("message_body")))
        return df

    def get(self, bridge_id: str) -> Bridge:
        """
        Get a bridge.

        :param bridge_id: string - (required) Bridge ID
        """

        df = self.send_request(method="GET", uri=f"bridges/{bridge_id}")
        df.addCallback(lambda result: self.parse_body(result.get("message_body")))
        return df

    def delete(self, bridge_id: str) -> None:
        """
        Delete a bridge.

        :param bridge_id: string - (required) Bridge ID
        """

        self.send_request(
            method="DELETE", uri=f"bridges/{bridge_id}", wait_for_response=False
        )

    def add_channel(
        self,
        bridge_id: str,
        channel: str,
        role: str | None = None,
        absorb_dtmf: bool = False,
        mute: bool = False,
        inhibit_connected_line_updates: bool = False,
    ) -> None:
        """
        Add a channel/-s to the bridge.

        :param bridge_id: string - (required) Bridge ID
        :param channel: string - (required) Ids of channels to add to bridge; Allows
        comma separated values.
        :param role: string - Channel's role in the bridge.
        :param absorb_dtmf: boolean - Absorb DTMF coming from this channel, preventing
        it to pass through to the bridge
        :param mute: boolean - Mute audio from this channel, preventing it to pass
        through to the bridge
        :param inhibit_connected_line_updates: boolean - Do not present the identity of
        the newly connected channel to other bridge members
        """

        query_params: dict[str, str] = {"channel": channel}
        if role:
            query_params["role"] = role
        if absorb_dtmf:
            query_params["absorbDTMF"] = "true"
        if mute:
            query_params["mute"] = "true"
        if inhibit_connected_line_updates:
            query_params["inhibitConnectedLineUpdates"] = "true"

        uri = self._build_uri(f"bridges/{bridge_id}/addChannel", query_params)
        self.send_request(method="POST", uri=uri, wait_for_response=False)

    def remove_channel(self, bridge_id: str, channel: str) -> None:
        """
        Remove a channel/-s from the bridge.

        :param bridge_id: string - (required) Bridge ID
        :param channel: string - (required) Ids of channels to add to bridge;
        Allows comma separated values.
        """

        query_params: dict[str, str] = {"channel": channel}
        uri = self._build_uri(f"bridges/{bridge_id}/removeChannel", query_params)
        self.send_request(method="POST", uri=uri, wait_for_response=False)

    def set_video_source(self, bridge_id: int) -> NotImplementedError:
        raise NotImplementedError()

    def clear_video_source(self, bridge_id: int) -> NotImplementedError:
        raise NotImplementedError()

    def start_moh(self, bridge_id: str, moh_class: str) -> None:
        """Start playing music on hold on the bridge.

        :param bridge_id: string - (required) Bridge Id.
        :param moh_class: string - (required) Moh class.
        """

        query_params: dict[str, str] = {"mohClass": moh_class}
        uri = self._build_uri(f"bridges/{bridge_id}/moh", query_params)
        self.send_request(method="POST", uri=uri, wait_for_response=False)

    def stop_moh(self, bridge_id: str) -> None:
        """Stop playing music on hold on the bridge.

        :param bridge_id: string - (required) Bridge Id.
        """

        self.send_request(
            method="DELETE", uri=f"bridges/{bridge_id}/moh", wait_for_response=False
        )

    def play(
        self,
        bridge_id: str,
        media: str,
        announcer_format: str = None,
        lang: str = None,
        offsetms: int = None,
        skipms: int = 3000,
        playback_id: str = None,
    ) -> Playback:
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
        :param playback_id: string - Playback Id.
        """

        query_params: dict[str, str] = {"media": media}
        if announcer_format:
            query_params["announcer_format"] = announcer_format

        if lang:
            query_params["lang"] = lang

        if offsetms:
            query_params["offsetms"] = str(offsetms)

        if skipms:
            query_params["skipms"] = str(skipms)

        if playback_id:
            query_params["playbackId"] = playback_id

        uri = self._build_uri(f"bridges/{bridge_id}/play", query_params)
        df = self.send_request(method="POST", uri=uri)
        df.addCallback(lambda result: self.parse_body(result.get("message_body")))
        return df

    def play_with_id(
        self,
        bridge_id: str,
        playback_id: str,
        media: str,
        announcer_format: str = None,
        lang: str = None,
        offsetms: int = None,
        skipms: int = 3000,
    ) -> Playback:
        """
        Start playback of media on a bridge. The media URI may be any of a number of
        URI's. Currently sound:, recording:, number:, digits:, characters:, and
        tone: URI's are supported. This operation creates a playback resource that can
        be used to control the playback of media (pause, rewind, fast forward, etc.)

        :param bridge_id: string - (required) Bridge Id.
        :param media: string - (required) Media URIs to play.
        :param playback_id: string - (required) Playback Id.
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

        query_params: dict[str, str] = {"media": media}
        if announcer_format:
            query_params["announcer_format"] = announcer_format

        if lang:
            query_params["lang"] = lang

        if offsetms:
            query_params["offsetms"] = str(offsetms)

        if skipms:
            query_params["skipms"] = str(skipms)

        uri = self._build_uri(f"bridges/{bridge_id}/play/{playback_id}", query_params)

        df = self.send_request(method="POST", uri=uri)
        df.addCallback(lambda result: self.parse_body(result.get("message_body")))
        return df

    def record(
        self,
        bridge_id: str,
        name: str,
        recording_format: str,
        recorder_format: str | None = None,
        max_duration_seconds: int = 0,
        max_silence_seconds: int = 0,
        if_exists: str = "fail",
        beep: bool = False,
        terminate_on: str = "none",
    ) -> LiveRecording:
        """Start a recording. This records the mixed audio from all channels
        participating in this bridge.

        :param bridge_id: string - (required) Bridge Id.
        :param name: string - (required) Recording's filename
        :param recording_format: string - (required) Format to encode audio in
        :param recorder_format: string - Format of the 'Recorder' channel attached to
        the bridge. Defaults to the same format as the 'format' parameter.
        :param max_duration_seconds: int - Maximum duration of the recording, in
        seconds. 0 for no limit.
        Allowed range: Min: 0; Max: None
        :param max_silence_seconds: int - Maximum duration of silence, in seconds. 0
        for no limit.
        Allowed range: Min: 0; Max: None
        :param if_exists: string - Action to take if a recording with the same name
        already exists.
        Default: fail
        Allowed values: fail, overwrite, append
        :param beep: boolean - Play beep when recording begins
        :param terminate_on: string - DTMF input to terminate recording.
        Default: none
        Allowed values: none, any, *, #
        """

        query_params: dict[str, str] = {"name": name, "format": recording_format}
        if recorder_format:
            query_params["recorder_format"] = recorder_format
        else:
            query_params["recorder_format"] = recording_format

        if max_duration_seconds:
            query_params["maxDurationSeconds"] = str(max_duration_seconds)

        if max_silence_seconds:
            query_params["maxSilenceSeconds"] = str(max_silence_seconds)

        if if_exists:
            query_params["ifExists"] = if_exists

        if beep:
            query_params["beep"] = "true"

        if terminate_on:
            query_params["terminateOn"] = terminate_on

        uri = self._build_uri(f"bridges/{bridge_id}/record", query_params)

        df = self.send_request(method="POST", uri=uri)
        df.addCallback(lambda result: self.parse_body(result.get("message_body")))
        return df
