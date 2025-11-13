from api.base import BaseAPI


class Channels(BaseAPI):
    def __init__(self, send_request):
        super().__init__(send_request)

    async def list(self) -> list[dict]:
        """List all active channels in Asterisk."""

        result = await self.send_request(
            method="GET",
            uri="channels"
        )
        return self.parse_body(result.get('message_body'))

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
        variables: dict | None = None
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

        result = await self.send_request(
            method="POST",
            uri=uri,
            **variables
        )
        return self.parse_body(result.get('message_body'))

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
        variables: dict | None = None
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

        result = await self.send_request(
            method="POST",
            uri=uri,
            **variables
        )
        return self.parse_body(result.get('message_body'))

    async def create(
            self,
            endpoint: str,
            app: str,
            app_args: str | None = None,
            channel_id: str | None = None,
            other_channel_id: str | None = None,
            originator: str | None = None,
            formats: str | None = None,
            variables: dict | None = None
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

        result = await self.send_request(
            method="POST",
            uri=uri,
            **variables
        )
        return self.parse_body(result.get('message_body'))

    async def get(self, channel_id: str) -> dict:
        """Get Channel details.

        :param channel_id: string - Channel's id
        """

        result = await self.send_request(
            method="GET",
            uri=f"channels/{channel_id}",
        )
        return self.parse_body(result.get('message_body'))

    async def hangup(
            self,
            channel_id: str,
            reason_code: str | None = None,
            reason: str | None = None
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
