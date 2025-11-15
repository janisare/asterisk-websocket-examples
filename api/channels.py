from typing import Any, TypeAlias
from .base import BaseAPI

Channel: TypeAlias = dict[str, Any]
ChannelList: TypeAlias = list[Channel]

Playback: TypeAlias = dict[str, Any]
LiveRecording: TypeAlias = dict[str, Any]
Variable: TypeAlias = dict[str, Any]
RTPstat: TypeAlias = dict[str, Any]


class Channels(BaseAPI):
    def __init__(self, send_request):
        super().__init__(send_request)

    def list(self) -> ChannelList:
        """List all active channels in Asterisk."""

        df = self.send_request(method="GET", uri="channels")
        df.addCallback(self.process_result)
        return df

    def originate(
        self,
        endpoint: str,
        extension: str | None = None,
        context: str | None = None,
        priority: int | None = None,
        label: str | None = None,
        app: str | None = None,
        app_args: str | None = None,
        callerid: str | None = None,
        timeout: int = 30,
        channel_id: str | None = None,
        other_channel_id: str | None = None,
        originator: str | None = None,
        formats: str | None = None,
        variables: dict | None = None,
    ) -> Channel:
        """
        Create a new channel (originate). The new channel is created immediately and
        a snapshot of it returned. If a Stasis application is provided it will be
        automatically subscribed to the originated channel for further events and
        updates.

        :param endpoint: string - (required) Endpoint to call.
        :param extension: string - The extension to dial after the endpoint answers.
        Mutually exclusive with 'app'.
        :param context: string - The context to dial after the endpoint answers. If
        omitted, uses 'default'. Mutually exclusive with 'app'.
        :param priority: long - The priority to dial after the endpoint answers. If
        omitted, uses 1. Mutually exclusive with 'app'.
        :param label: string - The label to dial after the endpoint answers. Will
        supersede 'priority' if provided. Mutually exclusive with 'app'.
        :param app: string - The application that is subscribed to the originated
        channel. When the channel is answered, it will be passed to this Stasis
        application. Mutually exclusive with 'context', 'extension', 'priority', and
        'label'.
        :param app_args: string - The application arguments to pass to the Stasis
        application provided by 'app'. Mutually exclusive with 'context', 'extension',
        'priority', and 'label'.
        :param callerid: string - CallerID to use when dialing the endpoint or
        extension.
        :param timeout: int - Timeout (in seconds) before giving up dialing, or -1 for
        no timeout.
        Default: 30
        :param channel_id: string - The unique id to assign the channel on creation.
        :param other_channel_id: string - The unique id to assign the second channel
        when using local channels.
        :param originator: string - The unique id of the channel which is originating
        this one.
        :param formats: string - The format name capability list to use if originator
        is not specified. Ex. "ulaw,slin16". Format names can be found with "core show
        codecs".
        :param variables: containers - The "variables" key in the body object holds
        variable key/value pairs to set on the channel on creation. Other keys in the
        body object are interpreted as query parameters.
        Ex. { "endpoint": "SIP/Alice", "variables": { "CALLERID(name)": "Alice" } }
        """

        query_params: dict[str, str] = {"endpoint": endpoint}
        if extension:
            query_params["extension"] = extension
        if context:
            query_params["context"] = context
        if priority:
            query_params["priority"] = str(priority)
        if label:
            query_params["label"] = label
        if app:
            query_params["app"] = app
        if app_args:
            query_params["appArgs"] = app_args
        if callerid:
            query_params["callerId"] = callerid
        if timeout:
            query_params["timeout"] = str(timeout)
        if channel_id:
            query_params["channelId"] = channel_id
        if other_channel_id:
            query_params["otherChannelId"] = other_channel_id
        if originator:
            query_params["originator"] = originator
        if formats:
            query_params["formats"] = formats

        uri = self._build_uri("channels", query_params)

        if not variables:
            variables = {}

        df = self.send_request(method="POST", uri=uri, **variables)
        df.addCallback(self.process_result)
        return df

    def originate_with_id(
        self,
        endpoint: str,
        extension: str | None = None,
        context: str | None = None,
        priority: int | None = None,
        label: str | None = None,
        app: str | None = None,
        app_args: str | None = None,
        callerid: str | None = None,
        timeout: int = 30,
        channel_id: str | None = None,
        other_channel_id: str | None = None,
        originator: str | None = None,
        formats: str | None = None,
        variables: dict | None = None,
    ) -> Channel:
        """
        Create a new channel (originate with id). The new channel is created immediately
        and a snapshot of it returned. If a Stasis application is provided it will be
        automatically subscribed to the originated channel for further events and
        updates.

        :param channel_id: string - The unique id to assign the channel on creation.
        :param endpoint: string - (required) Endpoint to call.
        :param extension: string - The extension to dial after the endpoint answers.
        Mutually exclusive with 'app'.
        :param context: string - The context to dial after the endpoint answers. If
        omitted, uses 'default'. Mutually exclusive with 'app'.
        :param priority: long - The priority to dial after the endpoint answers. If
        omitted, uses 1. Mutually exclusive with 'app'.
        :param label: string - The label to dial after the endpoint answers. Will
        supersede 'priority' if provided. Mutually exclusive with 'app'.
        :param app: string - The application that is subscribed to the originated
        channel. When the channel is answered, it will be passed to this Stasis
        application. Mutually exclusive with 'context', 'extension', 'priority', and
        'label'.
        :param app_args: string - The application arguments to pass to the Stasis
        application provided by 'app'. Mutually exclusive with 'context', 'extension',
        'priority', and 'label'.
        :param callerid: string - CallerID to use when dialing the endpoint or
        extension.
        :param timeout: int - Timeout (in seconds) before giving up dialing, or -1 for
        no timeout.
        Default: 30
        :param other_channel_id: string - The unique id to assign the second channel
        when using local channels.
        :param originator: string - The unique id of the channel which is originating
        this one.
        :param formats: string - The format name capability list to use if originator
        is not specified. Ex. "ulaw,slin16". Format names can be found with "core show
        codecs".
        :param variables: containers - The "variables" key in the body object holds
        variable key/value pairs to set on the channel on creation. Other keys in the
        body object are interpreted as query parameters.
        Ex. { "endpoint": "SIP/Alice", "variables": { "CALLERID(name)": "Alice" } }
        """

        query_params: dict[str, str] = {"endpoint": endpoint}
        if extension:
            query_params["extension"] = extension
        if context:
            query_params["context"] = context
        if priority:
            query_params["priority"] = str(priority)
        if label:
            query_params["label"] = label
        if app:
            query_params["app"] = app
        if app_args:
            query_params["appArgs"] = app_args
        if callerid:
            query_params["callerId"] = callerid
        if timeout:
            query_params["timeout"] = str(timeout)
        if other_channel_id:
            query_params["otherChannelId"] = other_channel_id
        if originator:
            query_params["originator"] = originator
        if formats:
            query_params["formats"] = formats

        uri = self._build_uri(f"channels/{channel_id}", query_params)

        if not variables:
            variables = {}

        df = self.send_request(method="POST", uri=uri, **variables)
        df.addCallback(self.process_result)
        return df

    def create(
        self,
        endpoint: str,
        app: str,
        app_args: str | None = None,
        channel_id: str | None = None,
        other_channel_id: str | None = None,
        originator: str | None = None,
        formats: str | None = None,
        variables: dict | None = None,
    ) -> Channel:
        """Create a channel.

        :param endpoint: string - (required) Endpoint for channel communication
        :param app: string - (required) Stasis Application to place channel into
        :param app_args: string - The application arguments to pass to the Stasis
        application provided by 'app'. Mutually exclusive with 'context', 'extension',
        'priority', and 'label'.
        :param channel_id: string - The unique id to assign the channel on creation.
        :param other_channel_id: string - The unique id to assign the second channel
        when using local channels.
        :param originator: string - Unique ID of the calling channel
        :param formats: string - The format name capability list to use if originator
        is not specified. Ex. "ulaw,slin16". Format names can be found with "core show
        codecs".
        :param variables: containers - The "variables" key in the body object holds
        variable key/value pairs to set on the channel on creation. Other keys in the
        body object are interpreted as query parameters. Ex. { "endpoint": "SIP/Alice",
        "variables": { "CALLERID(name)": "Alice" } }
        """

        query_params: dict[str, str] = {
            "endpoint": endpoint,
            "app": app,
        }
        if app_args:
            query_params["appArgs"] = app_args
        if channel_id:
            query_params["channelId"] = channel_id
        if other_channel_id:
            query_params["otherChannelId"] = other_channel_id
        if originator:
            query_params["originator"] = originator
        if formats:
            query_params["formats"] = formats

        uri = self._build_uri("channels/create", query_params)

        if not variables:
            variables = {}

        df = self.send_request(method="POST", uri=uri, **variables)
        df.addCallback(self.process_result)
        return df

    def get(self, channel_id: str) -> Channel:
        """Get Channel details.

        :param channel_id: string - Channel's id
        """

        df = self.send_request(
            method="GET",
            uri=f"channels/{channel_id}",
        )
        df.addCallback(self.process_result)
        return df

    def hangup(
        self, channel_id: str, reason_code: str | None = None, reason: str | None = None
    ) -> None:
        """Delete (i.e. hangup) a channel.

        :param channel_id: string - Channel's id
        :param reason_code: string - The reason code for hanging up the channel for
        detail use. Mutually exclusive with 'reason'. See detail hangup codes at here.
        https://docs.asterisk.org/Configuration/Miscellaneous/Hangup-Cause-Mappings/
        :param reason: string - Reason for hanging up the channel for simple use.
        Mutually exclusive with 'reason_code'.
        Allowed values: normal, busy, congestion, no_answer, timeout, rejected,
        unallocated, normal_unspecified, number_incomplete, codec_mismatch,
        interworking, failure, answered_elsewhere
        """

        uri = f"channels/{channel_id}"
        if reason_code:
            uri = self._build_uri(uri, {"reasonCode": reason_code})
        elif reason:
            uri = self._build_uri(uri, {"reason": reason})

        self.send_request(method="DELETE", uri=uri)

    def continue_in_dialplan(
        self,
        channel_id: str,
        context: str | None = None,
        extension: str | None = None,
        priority: int | None = None,
        label: str | None = None,
    ) -> None:
        """Exit application; continue execution in the dialplan.

        :param channel_id: (required) string - Channel's id
        :param context: string - The context to continue to.
        :param extension: string - The extension to continue to.
        :param priority: int - The priority to continue to.
        :param label: string - The label to continue to - will supersede 'priority' if
        both are provided.
        """

        query_params: dict[str, str] = {}
        if context:
            query_params["context"] = context
        if extension:
            query_params["extension"] = extension
        if priority:
            query_params["priority"] = str(priority)
        if label:
            query_params["label"] = label

        uri = self._build_uri(f"/channels/{channel_id}/continue", query_params)
        self.send_request(method="POST", uri=uri)

    def move(self, channel_id: str, app: str, app_args: str | None = None) -> None:
        """Move the channel from one Stasis application to another.

        :param channel_id: (required) string - Channel's id
        :param app: string - (required) The channel will be passed to this Stasis
        application.
        :param app_args: string - The application arguments to pass to the Stasis
        application provided by 'app'.
        """

        query_params: dict[str, str] = {"app": app}
        if app_args:
            query_params["appArgs"] = app_args

        uri = self._build_uri(f"/channels/{channel_id}/move", query_params)
        self.send_request(method="POST", uri=uri)

    def redirect(
        self,
        channel_id: str,
        endpoint: str,
    ) -> None:
        """Redirect the channel to a different location.

        :param channel_id: (required) string - Channel's id
        :param endpoint: string - (required) The endpoint to redirect the channel to
        """

        uri = self._build_uri(
            f"/channels/{channel_id}/redirect", {"endpoint": endpoint}
        )
        self.send_request(method="POST", uri=uri)

    def answer(
        self,
        channel_id: str,
    ) -> None:
        """Answer a channel.

        :param channel_id: (required) string - Channel's id
        """

        self.send_request(method="POST", uri=f"/channels/{channel_id}/answer")

    def ring(
        self,
        channel_id: str,
    ) -> None:
        """Indicate ringing to a channel.

        :param channel_id: (required) string - Channel's id
        """

        self.send_request(method="POST", uri=f"/channels/{channel_id}/ring")

    def ring_stop(
        self,
        channel_id: str,
    ) -> None:
        """Stop ringing indication on a channel if locally generated.

        :param channel_id: (required) string - Channel's id
        """

        self.send_request(method="DELETE", uri=f"/channels/{channel_id}/ring")

    def progress(
        self,
        channel_id: str,
    ) -> None:
        """Indicate progress to a channel.

        :param channel_id: (required) string - Channel's id
        """

        self.send_request(method="POST", uri=f"/channels/{channel_id}/progress")

    def send_dtmf(
        self,
        channel_id: str,
        dtmf: str,
        before: int | None = None,
        between: int | None = 100,
        duration: int | None = 100,
        after: int | None = None,
    ) -> None:
        """Send provided DTMF to a given channel.

        :param channel_id: (required) string - Channel's id
        :param dtmf: string - DTMF To send.
        :param before: int - Amount of time to wait before DTMF digits (specified in
        milliseconds) start.
        :param between: int - Amount of time in between DTMF digits (specified in
        milliseconds). Default: 100
        :param duration: int - Length of each DTMF digit (specified in milliseconds).
        Default: 100
        :param after: int - Amount of time to wait after DTMF digits (specified in
        milliseconds) end.
        """
        query_params: dict[str, str] = {}
        if dtmf:
            query_params["dtmf"] = dtmf
        if before:
            query_params["before"] = str(before)
        if between:
            query_params["between"] = str(between)
        if duration:
            query_params["duration"] = str(duration)
        if after:
            query_params["after"] = str(after)

        uri = self._build_uri(f"/channels/{channel_id}/dtmf", query_params)
        self.send_request(method="POST", uri=uri)

    def mute(self, channel_id: str, direction: str = "both") -> None:
        """Mute a channel.

        :param channel_id: (required) string - Channel's id
        :param direction: string - Direction in which to mute audio
        Default: both
        Allowed values: both, in, out
        """

        uri = self._build_uri(f"/channels/{channel_id}/mute", {"direction": direction})
        self.send_request(method="POST", uri=uri)

    def unmute(self, channel_id: str, direction: str = "both") -> None:
        """Unmute a channel.

        :param channel_id: (required) string - Channel's id
        :param direction: string - Direction in which to mute audio
        Default: both
        Allowed values: both, in, out
        """

        uri = self._build_uri(f"/channels/{channel_id}/mute", {"direction": direction})
        self.send_request(method="DELETE", uri=uri)

    def hold(self, channel_id: str) -> None:
        """Hold a channel.

        :param channel_id: (required) string - Channel's id
        """

        self.send_request(method="POST", uri=f"/channels/{channel_id}/hold")

    def unhold(self, channel_id: str) -> None:
        """Remove a channel from hold.

        :param channel_id: (required) string - Channel's id
        """

        self.send_request(method="DELETE", uri=f"/channels/{channel_id}/hold")

    def start_moh(self, channel_id: str, moh_class: str | None = None) -> None:
        """Play music on hold to a channel. Using media operations such as /play on a
        channel playing MOH in this manner will suspend MOH without resuming
        automatically. If continuing music on hold is desired, the stasis application
        must reinitiate music on hold.

        :param channel_id: (required) string - Channel's id
        :param moh_class: string - Music on hold class to use
        """

        query_params: dict[str, str] = {}
        if moh_class:
            query_params["mohClass"] = moh_class

        uri = self._build_uri(f"/channels/{channel_id}/moh", query_params)
        self.send_request(method="POST", uri=uri)

    def stop_moh(self, channel_id: str) -> None:
        """Remove a channel from hold.

        :param channel_id: (required) string - Channel's id
        """

        self.send_request(method="DELETE", uri=f"/channels/{channel_id}/moh")

    def start_silence(self, channel_id: str) -> None:
        """Play silence to a channel. Using media operations such as /play on a channel
        playing silence in this manner will suspend silence without resuming
        automatically.

        :param channel_id: (required) string - Channel's id
        """
        self.send_request(method="POST", uri=f"/channels/{channel_id}/silence")

    def stop_silence(self, channel_id: str) -> None:
        """Stop playing silence to a channel.

        :param channel_id: (required) string - Channel's id
        """

        self.send_request(method="DELETE", uri=f"/channels/{channel_id}/silence")

    def play(
        self,
        channel_id: str,
        media: str,
        lang: str | None = None,
        offsetms: int | None = None,
        skipms: int | None = 3000,
        playback_id: str | None = None,
    ) -> Playback:
        """Start playback of media. The media URI may be any of a number of URI's.
        Currently sound:, recording:, number:, digits:, characters:, and tone: URI's
        are supported. This operation creates a playback resource that can be used to
        control the playback of media (pause, rewind, fast forward, etc.)

        :param channel_id: (required) string - Channel's id
        :param media: string - (required) Media URIs to play.
        Allows comma separated values.
        :param lang: string - For sounds, selects language for sound.
        :param offsetms: int - Number of milliseconds to skip before playing. Only
        applies to the first URI if multiple media URIs are specified.
        :param skipms: int - Number of milliseconds to skip for forward/reverse
        operations.
        Default: 3000
        :param playback_id: string - Playback ID.
        """

        query_params: dict[str, str] = {"media": media}
        if lang:
            query_params["lang"] = lang
        if offsetms:
            query_params["offsetms"] = str(offsetms)
        if skipms:
            query_params["skipms"] = str(skipms)
        if playback_id:
            query_params["playbackId"] = playback_id

        uri = self._build_uri(f"/channels/{channel_id}/play", query_params)
        df = self.send_request(method="POST", uri=uri)
        df.addCallback(self.process_result)
        return df

    def play_with_id(
        self,
        channel_id: str,
        playback_id: str,
        media: str,
        lang: str | None = None,
        offsetms: int | None = None,
        skipms: int | None = 3000,
    ) -> Playback:
        """Start playback of media and specify the playbackId. The media URI may be any
        of a number of URI's. Currently sound:, recording:, number:, digits:,
        characters:, and tone: URI's are supported. This operation creates a playback
        resource that can be used to control the playback of media (pause, rewind, fast
        forward, etc.)

        :param channel_id: (required) string - Channel's id
        :param playback_id: string - (required) Playback ID.

        :param media: string - (required) Media URIs to play.
        Allows comma separated values.
        :param lang: string - For sounds, selects language for sound.
        :param offsetms: int - Number of milliseconds to skip before playing. Only
        applies to the first URI if multiple media URIs are specified.
        :param skipms: int - Number of milliseconds to skip for forward/reverse
        operations.
        Default: 3000
        """

        query_params: dict[str, str] = {"media": media}
        if lang:
            query_params["lang"] = lang
        if offsetms:
            query_params["offsetms"] = str(offsetms)
        if skipms:
            query_params["skipms"] = str(skipms)

        uri = self._build_uri(f"/channels/{channel_id}/play{playback_id}", query_params)
        df = self.send_request(method="POST", uri=uri)
        df.addCallback(self.process_result)
        return df

    def record(
        self,
        channel_id: str,
        name: str,
        record_format: str,
        max_duration_seconds: int = 0,
        max_silence_seconds: int = 0,
        if_exists: str = "fail",
        beep: bool = False,
        terminate_on: str = "none",
    ) -> LiveRecording:
        """Start a recording. Record audio from a channel. Note that this will not
        capture audio sent to the channel. The bridge itself has a record feature
        if that's what you want.

        :param channel_id: (required) string - Channel's id
        :param name: string - (required) Recording's filename
        :param record_format: string - (required) Format to encode audio in
        :param max_duration_seconds: int - Maximum duration of the recording, in seconds.
        0 for no limit
        Allowed range: Min: 0; Max: None
        :param max_silence_seconds: int - Maximum duration of silence, in seconds.
        0 for no limit
        Allowed range: Min: 0; Max: None
        :param if_exists: string - Action to take if a recording with the same name
        already exists.
        Default: fail
        Allowed values: fail, overwrite, append
        :param beep: boolean - Play beep when recording begins
        :param terminate_on: string - DTMF input to terminate recording
        Default: none
        Allowed values: none, any, *, #
        """

        query_params: dict[str, str] = {
            "name": name,
            "format": record_format,
        }
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

        uri = self._build_uri(f"/channels/{channel_id}/record", query_params)

        df = self.send_request(method="POST", uri=uri)
        df.addCallback(self.process_result)
        return df

    def get_variable(self, channel_id: str, variable: str) -> Variable:
        """Get the value of a channel variable or function.

        :param channel_id: string - (required) Channel's id
        :param variable: string - (required) The channel variable or function to get
        """
        uri = self._build_uri(f"channels/{channel_id}/variable", {"variable": variable})
        df = self.send_request(method="GET", uri=uri)
        df.addCallback(self.process_result)
        return df

    def set_variable(
        self, channel_id: str, variable: str, value: str | None = None
    ) -> None:
        """Get the value of a channel variable or function.

        :param channel_id: string - (required) Channel's id
        :param variable: string - (required) The channel variable or function to get
        :param value: string - The value to set the variable to
        """
        query_params: dict[str, str] = {"variable": variable}
        if value:
            query_params["value"] = value

        uri = self._build_uri(f"channels/{channel_id}/variable", query_params)
        self.send_request(method="POST", uri=uri)

    def snoop(
        self,
        channel_id: str,
        spy: str = "none",
        whisper: str = "none",
        app: str | None = None,
        app_args: str | None = None,
        snoop_id: str | None = None,
    ) -> Channel:
        """Start snooping. Snoop (spy/whisper) on a specific channel.

        :param channel_id: string - (required) Channel's id
        :param spy: string - Direction of audio to spy on
        Default: none
        Allowed values: none, both, out, in
        :param whisper: string - Direction of audio to whisper into
        Default: none
        Allowed values: none, both, out, in
        :param app: string - (required) Application the snooping channel is placed into
        :param app_args: string - The application arguments to pass to the Stasis
        application
        :param snoop_id: string - Unique ID to assign to snooping channel
        """
        query_params: dict[str, str] = {}
        if spy:
            query_params["spy"] = spy
        if whisper:
            query_params["whisper"] = whisper
        if app:
            query_params["app"] = app
        if app_args:
            query_params["appArgs"] = app_args
        if snoop_id:
            query_params["snoopId"] = snoop_id

        uri = self._build_uri(f"channels/{channel_id}/snoop", query_params)

        df = self.send_request(method="POST", uri=uri)
        df.addCallback(self.process_result)
        return df

    def snoop_with_id(
        self,
        channel_id: str,
        snoop_id: str,
        spy: str = "none",
        whisper: str = "none",
        app: str | None = None,
        app_args: str | None = None,
    ) -> Channel:
        """Start snooping. Snoop (spy/whisper) on a specific channel.

        :param channel_id: string - (required) Channel's id
        :param snoop_id: string - (required) Unique ID to assign to snooping channel
        :param spy: string - Direction of audio to spy on
        Default: none
        Allowed values: none, both, out, in
        :param whisper: string - Direction of audio to whisper into
        Default: none
        Allowed values: none, both, out, in
        :param app: string - (required) Application the snooping channel is placed into
        :param app_args: string - The application arguments to pass to the Stasis
        application
        """

        query_params: dict[str, str] = {}
        if spy:
            query_params["spy"] = spy
        if whisper:
            query_params["whisper"] = whisper
        if app:
            query_params["app"] = app
        if app_args:
            query_params["appArgs"] = app_args

        uri = self._build_uri(f"channels/{channel_id}/snoop/{snoop_id}", query_params)

        df = self.send_request(method="POST", uri=uri)
        df.addCallback(self.process_result)
        return df

    def dial(
        self, channel_id: str, caller: str | None = None, timeout: int | None = None
    ) -> None:
        """Dial a created channel.

        :param channel_id: string - (required) Channel's id
        :param caller: string - Channel ID of caller
        :param timeout: int - Dial timeout
        Allowed range: Min: 0; Max: None
        """

        query_params: dict[str, str] = {}
        if caller:
            query_params["caller"] = caller
        if timeout:
            query_params["timeout"] = str(timeout)

        uri = self._build_uri(f"channels/{channel_id}/dial", query_params)
        self.send_request(method="POST", uri=uri)

    def rtp_statistics(self, channel_id: str) -> RTPstat:
        """RTP stats on a channel.

        :param channel_id: string - (required) Channel's id
        """
        df = self.send_request(
            method="GET", uri=f"channels/{channel_id}/rtp_statistics"
        )
        df.addCallback(self.process_result)
        return df

    def external_media(
        self,
        app: str,
        channel_id: str | None = None,
        external_host: str | None = None,
        encapsulation: str | None = "rtp",
        transport: str | None = "udp",
        connection_type: str | None = "client",
        format: str | None = None,
        direction: str | None = "both",
        data: str | None = None,
        transport_data: str | None = None,
        variables: dict | None = None,
    ) -> Channel:
        """
        Start an External Media session. Create a channel to an External Media
        source/sink. The combination of transport and encapsulation will select one
        of chan_rtp(udp/rtp), chan_audiosocket(tcp/audiosocket) or
        chan_websocket(websocket/none) channel drivers.

        :param: channelId: string - The unique id to assign the channel on creation.
        :param: app: string - (required) Stasis Application to place channel into
        :param: external_host: string - Hostname/ip:port or websocket_client connection
        ID of external host. May be empty for a websocket server connection.
        :param: encapsulation: string - Payload encapsulation protocol. Must be 'none'
        for the websocket transport.
        Default: rtp
        Allowed values: rtp, audiosocket, none
        :param: transport: string - Transport protocol
        Default: udp
        Allowed values: udp, tcp, websocket
        :param: connection_type: string - Connection type (client/server). 'server' is
        only valid for the websocket transport.
        Default: client
        Allowed values: client, server
        :param: format: string - (required) Format to encode audio in
        :param: direction: string - External media direction
        Default: both
        Allowed values: both
        :param: data: string - An arbitrary data field
        :param: transport_data: string - Transport-specific data. For websocket this is
        appended to the dialstring.

        :param: variables: containers - The "variables" key in the body object holds
        variable key/value pairs to set on the channel on creation. Other keys in the
        body object are interpreted as query parameters. Ex. { "endpoint": "SIP/Alice",
        "variables": { "CALLERID(name)": "Alice" } }
        """

        query_params: dict[str, str] = {"app": app}
        if channel_id:
            query_params["channelId"] = channel_id
        if external_host:
            query_params["external_host"] = external_host
        if encapsulation:
            query_params["encapsulation"] = encapsulation
        if transport:
            query_params["transport"] = transport
        if connection_type:
            query_params["connection_type"] = connection_type
        if format:
            query_params["format"] = format
        if direction:
            query_params["direction"] = direction
        if data:
            query_params["data"] = data
        if transport_data:
            query_params["transport_data"] = transport_data

        uri = self._build_uri("channels/externalMedia", query_params)

        if not variables:
            variables = {}

        df = self.send_request(method="POST", uri=uri, **variables)
        df.addCallback(self.process_result)
        return df

    def transfer_progress(self, channel_id: str, states: str) -> None:
        """Inform the channel about the progress of the attended/blind transfer.

        :param channel_id: string - (required) Channel's id
        :param states: string - (required) The state of the progress
        """

        uri = self._build_uri(
            f"channels/{channel_id}/transfer_progress", {"states": states}
        )
        self.send_request(method="POST", uri=uri)
