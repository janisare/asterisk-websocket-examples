from api.base import BaseAPI


class Events(BaseAPI):
    def __init__(self, send_request):
        super().__init__(send_request)

    async def events(self, app: str, subscribe_all: bool = False) -> None:
        """WebSocket connection for events.

        :param app: string - (required) Applications to subscribe to.
        Allows comma separated values.
        :param subscribe_all: boolean - Subscribe to all Asterisk events. If provided, the
        applications listed will be subscribed to all events, effectively disabling
        the application specific subscriptions. Default is 'false'.
        """

        result = await self.send_request(
            method="GET",
            uri=f"events?app={app}&subscribeAll={subscribe_all}"
        )
        return self.parse_body(result.get('message_body'))

    async def create(
            self,
            name: str,
            app: str,
            source: str | None = None,
            variables: dict | None = None
    ) -> dict:
        """Generate a user event.

        :param name: string - (required) Event name
        :param app: string - (required) The name of the application that will receive
        this event
        :param source: string - URI for event source (channel:{channelId}, bridge:{bridgeId},
        endpoint:{tech}/{resource}, deviceState:{deviceName}
        Allows comma separated values.

        Body parameter¶
        :param variables: containers - The "variables" key in the body object holds
        custom key/value pairs to add to the user event. Ex. { "variables": { "key": "value" } }
        """

        uri = f"events/user/{name}?application={app}"
        if source:
            uri += f"&source={source}"

        if not variables:
            variables = {}

        result = await self.send_request(
            method="POST",
            uri=uri,
            **variables
        )
        return self.parse_body(result.get('message_body'))
