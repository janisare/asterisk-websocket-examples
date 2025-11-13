from api.base import BaseAPI


class Channels(BaseAPI):
    def __init__(self, send_request):
        super().__init__(send_request)

    async def list(self) -> list[dict]:
        """List all active channels in Asterisk."""

        result = await self.send_request(method="GET", uri="channels")
        return self.parse_body(result.get("message_body"))

    async def originate(
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
    ) -> dict:
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
        :param other_channel_id: string - The unique id to assign the second channel when
        using local channels.
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

        uri = f"channels?endpoint={endpoint}"
        if extension:
            uri += f"&extension={extension}"
        if context:
            uri += f"&context={context}"
        if priority:
            uri += f"&priority={priority}"
        if label:
            uri += f"&label={label}"
        if app:
            uri += f"&app={app}"
        if app_args:
            uri += f"&appArgs={app_args}"
        if callerid:
            uri += f"&callerId={callerid}"
        if timeout:
            uri += f"&timeout={timeout}"
        if channel_id:
            uri += f"&channelId={channel_id}"
        if other_channel_id:
            uri += f"&otherChannelId={other_channel_id}"
        if originator:
            uri += f"&originator={originator}"
        if formats:
            uri += f"&formats={formats}"

        if not variables:
            variables = {}

        result = await self.send_request(method="POST", uri=uri, **variables)
        return self.parse_body(result.get("message_body"))

    async def originate_with_id(
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
    ) -> dict:
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
        :param other_channel_id: string - The unique id to assign the second channel when
        using local channels.
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

        uri = f"channels/{channel_id}?endpoint={endpoint}"
        if extension:
            uri += f"&extension={extension}"
        if context:
            uri += f"&context={context}"
        if priority:
            uri += f"&priority={priority}"
        if label:
            uri += f"&label={label}"
        if app:
            uri += f"&app={app}"
        if app_args:
            uri += f"&appArgs={app_args}"
        if callerid:
            uri += f"&callerId={callerid}"
        if timeout:
            uri += f"&timeout={timeout}"
        if other_channel_id:
            uri += f"&otherChannelId={other_channel_id}"
        if originator:
            uri += f"&originator={originator}"
        if formats:
            uri += f"&formats={formats}"

        if not variables:
            variables = {}

        result = await self.send_request(method="POST", uri=uri, **variables)
        return self.parse_body(result.get("message_body"))

    async def create(
        self,
        endpoint: str,
        app: str,
        app_args: str | None = None,
        channel_id: str | None = None,
        other_channel_id: str | None = None,
        originator: str | None = None,
        formats: str | None = None,
        variables: dict | None = None,
    ) -> dict:
        """Create a channel.

        :param endpoint: string - (required) Endpoint for channel communication
        :param app: string - (required) Stasis Application to place channel into
        :param app_args: string - The application arguments to pass to the Stasis
        application provided by 'app'. Mutually exclusive with 'context', 'extension',
        'priority', and 'label'.
        :param channel_id: string - The unique id to assign the channel on creation.
        :param other_channel_id: string - The unique id to assign the second channel when
        using local channels.
        :param originator: string - Unique ID of the calling channel
        :param formats: string - The format name capability list to use if originator
        is not specified. Ex. "ulaw,slin16". Format names can be found with "core show
        codecs".
        :param variables: containers - The "variables" key in the body object holds
        variable key/value pairs to set on the channel on creation. Other keys in the
        body object are interpreted as query parameters. Ex. { "endpoint": "SIP/Alice",
        "variables": { "CALLERID(name)": "Alice" } }
        """

        uri = f"channels/create?endpoint={endpoint}&app={app}"
        if app_args:
            uri += f"&appArgs={app_args}"
        if channel_id:
            uri += f"&channelId={channel_id}"
        if other_channel_id:
            uri += f"&otherChannelId={other_channel_id}"
        if originator:
            uri += f"&originator={originator}"
        if formats:
            uri += f"&formats={formats}"

        if not variables:
            variables = {}

        result = await self.send_request(method="POST", uri=uri, **variables)
        return self.parse_body(result.get("message_body"))

    async def get(self, channel_id: str) -> dict:
        """Get Channel details.

        :param channel_id: string - Channel's id
        """

        result = await self.send_request(
            method="GET",
            uri=f"channels/{channel_id}",
        )
        return self.parse_body(result.get("message_body"))

    async def hangup(
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
            uri += f"?reasonCode={reason_code}"
        elif reason:
            uri += f"?reason={reason}"

        await self.send_request(method="DELETE", uri=uri)

    async def continue_in_dialplan(
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
        :param label: string - The label to continue to - will supersede 'priority' if both are provided.
        """

        uri = f"/channels/{channel_id}/continue"
        if context:
            uri += f"?context={context}"
        if extension:
            uri += f"&extension={extension}"
        if priority:
            uri += f"&priority={priority}"
        if label:
            uri += f"&label={label}"

        await self.send_request(method="POST", uri=uri)

    async def move(
        self, channel_id: str, app: str, app_args: str | None = None
    ) -> None:
        """Move the channel from one Stasis application to another.

        :param channel_id: (required) string - Channel's id
        :param app: string - (required) The channel will be passed to this Stasis
        application.
        :param app_args: string - The application arguments to pass to the Stasis
        application provided by 'app'.
        """

        uri = f"/channels/{channel_id}/move?app={app}"
        if app_args:
            uri += f"&appArgs={app_args}"

        await self.send_request(method="POST", uri=uri)

    async def redirect(
        self,
        channel_id: str,
        endpoint: str,
    ) -> None:
        """Redirect the channel to a different location.

        :param channel_id: (required) string - Channel's id
        :param endpoint: string - (required) The endpoint to redirect the channel to
        """

        await self.send_request(
            method="POST", uri=f"/channels/{channel_id}/redirect?endpoint={endpoint}"
        )

    async def answer(
        self,
        channel_id: str,
    ) -> None:
        """Answer a channel.

        :param channel_id: (required) string - Channel's id
        """

        await self.send_request(method="POST", uri=f"/channels/{channel_id}/answer")

    async def ring(
        self,
        channel_id: str,
    ) -> None:
        """Indicate ringing to a channel.

        :param channel_id: (required) string - Channel's id
        """

        await self.send_request(method="POST", uri=f"/channels/{channel_id}/ring")

    async def ring_stop(
        self,
        channel_id: str,
    ) -> None:
        """Stop ringing indication on a channel if locally generated.

        :param channel_id: (required) string - Channel's id
        """

        await self.send_request(method="DELETE", uri=f"/channels/{channel_id}/ring")

    async def progress(
        self,
        channel_id: str,
    ) -> None:
        """Indicate progress to a channel.

        :param channel_id: (required) string - Channel's id
        """

        await self.send_request(method="POST", uri=f"/channels/{channel_id}/progress")

    async def send_dtmf(
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
        uri = f"/channels/{channel_id}/dtmf"
        if dtmf:
            uri += f"?dtmf={dtmf}"
        if before:
            uri += f"&before={before}"
        if between:
            uri += f"&between={between}"
        if duration:
            uri += f"&duration={duration}"
        if after:
            uri += f"&after={after}"

        await self.send_request(method="POST", uri=uri)

    async def mute(self, channel_id: str, direction: str = "both") -> None:
        """Mute a channel.

        :param channel_id: (required) string - Channel's id
        :param direction: string - Direction in which to mute audio
        Default: both
        Allowed values: both, in, out
        """

        await self.send_request(
            method="POST", uri=f"/channels/{channel_id}/mute?direction={direction}"
        )

    async def unmute(self, channel_id: str, direction: str = "both") -> None:
        """Unmute a channel.

        :param channel_id: (required) string - Channel's id
        :param direction: string - Direction in which to mute audio
        Default: both
        Allowed values: both, in, out
        """

        await self.send_request(
            method="DELETE", uri=f"/channels/{channel_id}/mute?direction={direction}"
        )

    async def hold(self, channel_id: str) -> None:
        """Hold a channel.

        :param channel_id: (required) string - Channel's id
        """

        await self.send_request(method="POST", uri=f"/channels/{channel_id}/hold")

    async def unhold(self, channel_id: str) -> None:
        """Remove a channel from hold.

        :param channel_id: (required) string - Channel's id
        """

        await self.send_request(method="DELETE", uri=f"/channels/{channel_id}/hold")

    async def start_moh(self, channel_id: str, moh_class: str | None = None) -> None:
        """Play music on hold to a channel. Using media operations such as /play on a
        channel playing MOH in this manner will suspend MOH without resuming
        automatically. If continuing music on hold is desired, the stasis application
        must reinitiate music on hold.

        :param channel_id: (required) string - Channel's id
        :param moh_class: string - Music on hold class to use
        """
        uri = f"/channels/{channel_id}/moh"
        if moh_class:
            uri += f"?mohClass={moh_class}"

        await self.send_request(method="POST", uri=uri)

    async def stop_moh(self, channel_id: str) -> None:
        """Remove a channel from hold.

        :param channel_id: (required) string - Channel's id
        """

        await self.send_request(method="DELETE", uri=f"/channels/{channel_id}/moh")

    async def start_silence(self, channel_id: str) -> None:
        """Play silence to a channel. Using media operations such as /play on a channel
        playing silence in this manner will suspend silence without resuming
        automatically.

        :param channel_id: (required) string - Channel's id
        """
        await self.send_request(method="POST", uri=f"/channels/{channel_id}/silence")

    async def stop_silence(self, channel_id: str) -> None:
        """Stop playing silence to a channel.

        :param channel_id: (required) string - Channel's id
        """

        await self.send_request(method="DELETE", uri=f"/channels/{channel_id}/silence")

    async def play(
        self,
        channel_id: str,
        media: str,
        lang: str | None = None,
        offsetms: int | None = None,
        skipms: int | None = 3000,
        playback_id: str | None = None,
    ) -> None:
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

        uri = f"/channels/{channel_id}/play?media={media}"
        if lang:
            uri += f"&lang={lang}"
        if offsetms:
            uri += f"&offsetms={offsetms}"
        if skipms:
            uri += f"&skipms={skipms}"
        if playback_id:
            uri += f"&playbackId={playback_id}"

        await self.send_request(method="POST", uri=uri)

    async def play_with_id(
        self,
        channel_id: str,
        playback_id: str,
        media: str,
        lang: str | None = None,
        offsetms: int | None = None,
        skipms: int | None = 3000,
    ) -> None:
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

        uri = f"/channels/{channel_id}/play{playback_id}?media={media}"
        if lang:
            uri += f"&lang={lang}"
        if offsetms:
            uri += f"&offsetms={offsetms}"
        if skipms:
            uri += f"&skipms={skipms}"

        await self.send_request(method="POST", uri=uri)

    async def record(
        self,
        channel_id: str,
        name: str,
        format: str,
        max_duration_seconds: int = 0,
        max_silence_seconds: int = 0,
        if_exists: str = "fail",
        beep: bool = False,
        terminate_on: str = "none",
    ) -> dict:
        """Start a recording. Record audio from a channel. Note that this will not
        capture audio sent to the channel. The bridge itself has a record feature
        if that's what you want.

        :param channel_id: (required) string - Channel's id
        :param name: string - (required) Recording's filename
        :param format: string - (required) Format to encode audio in
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
        uri = f"/channels/{channel_id}/record?name={name}&format={format}"
        if max_duration_seconds:
            uri += f"&maxDurationSeconds={max_duration_seconds}"
        if max_silence_seconds:
            uri += f"&maxSilenceSeconds={max_silence_seconds}"
        if if_exists:
            uri += f"&ifExists={if_exists}"
        if beep:
            uri += "&beep=true"
        if terminate_on:
            uri += f"&terminateOn={terminate_on}"

        result = await self.send_request(method="POST", uri=uri)
        return self.parse_body(result.get("message_body"))

    async def get_variable(self, channel_id: str, variable: str) -> dict:
        """Get the value of a channel variable or function.

        :param channel_id: string - (required) Channel's id
        :param variable: string - (required) The channel variable or function to get
        """
        uri = f"channels/{channel_id}/variable?variable={variable}"
        result = await self.send_request(method="GET", uri=uri)
        return self.parse_body(result.get("message_body"))

    async def set_variable(
        self, channel_id: str, variable: str, value: str | None = None
    ) -> None:
        """Get the value of a channel variable or function.

        :param channel_id: string - (required) Channel's id
        :param variable: string - (required) The channel variable or function to get
        :param value: string - The value to set the variable to
        """
        uri = f"channels/{channel_id}/variable?variable={variable}"
        if value:
            uri += f"&value={value}"

        await self.send_request(method="POST", uri=uri)

    async def snoop(
        self,
        channel_id: str,
        spy: str = "none",
        whisper: str = "none",
        app: str | None = None,
        app_args: str | None = None,
        snoop_id: str | None = None,
    ) -> dict:
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
        uri = f"channels/{channel_id}/snoop"
        if spy:
            uri += f"?spy={spy}"
        if whisper:
            uri += f"&whisper={whisper}"
        if app:
            uri += f"&app={app}"
        if app_args:
            uri += f"&appArgs={app_args}"
        if snoop_id:
            uri += f"&snoopId={snoop_id}"

        result = await self.send_request(method="POST", uri=uri)
        return self.parse_body(result.get("message_body"))

    async def snoop_with_id(
        self,
        channel_id: str,
        snoop_id: str,
        spy: str = "none",
        whisper: str = "none",
        app: str | None = None,
        app_args: str | None = None,
    ) -> dict:
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
        uri = f"channels/{channel_id}/snoop/{snoop_id}"
        if spy:
            uri += f"?spy={spy}"
        if whisper:
            uri += f"&whisper={whisper}"
        if app:
            uri += f"&app={app}"
        if app_args:
            uri += f"&appArgs={app_args}"

        result = await self.send_request(method="POST", uri=uri)
        return self.parse_body(result.get("message_body"))

    async def dial(
        self, channel_id: str, caller: str | None = None, timeout: int | None = None
    ) -> None:
        """Dial a created channel.

        :param channel_id: string - (required) Channel's id
        :param caller: string - Channel ID of caller
        :param timeout: int - Dial timeout
        Allowed range: Min: 0; Max: None
        """

        uri = f"channels/{channel_id}/dial"
        if caller:
            uri += f"?caller={caller}"
        if timeout:
            uri += f"&timeout={timeout}"

        await self.send_request(method="POST", uri=uri)

    async def rtp_statistics(self, channel_id: str) -> dict:
        """RTP stats on a channel.

        :param channel_id: string - (required) Channel's id
        """
        result = await self.send_request(
            method="GET", uri=f"channels/{channel_id}/rtp_statistics"
        )
        return self.parse_body(result.get("message_body"))

    async def external_media(
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
    ) -> dict:
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

        uri = f"channels/externalMedia?app={app}"
        if channel_id:
            uri += f"&channelId={channel_id}"
        if external_host:
            uri += f"&external_host={external_host}"
        if encapsulation:
            uri += f"&encapsulation={encapsulation}"
        if transport:
            uri += f"&transport={transport}"
        if connection_type:
            uri += f"&connection_type={connection_type}"
        if format:
            uri += f"&format={format}"
        if direction:
            uri += f"&direction={direction}"
        if data:
            uri += f"&data={data}"
        if transport_data:
            uri += f"&transport_data={transport_data}"

        if not variables:
            variables = {}

        result = await self.send_request(method="POST", uri=uri, **variables)
        return self.parse_body(result.get("message_body"))

    async def transfer_progress(self, channel_id: str, states: str) -> None:
        """Inform the channel about the progress of the attended/blind transfer.

        :param channel_id: string - (required) Channel's id
        :param states: string - (required) The state of the progress
        """

        await self.send_request(
            method="POST",
            uri=f"channels/{channel_id}/transfer_progress?states={states}",
        )
