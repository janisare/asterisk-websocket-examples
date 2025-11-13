from api.base import BaseAPI


class Applications(BaseAPI):
    def __init__(self, send_request):
        super().__init__(send_request)

    async def list(self) -> list[dict]:
        """List all applications."""

        result = await self.send_request(
            method="GET",
            uri="applications"
        )
        return self.parse_body(result.get('message_body'))

    async def get(self, name: str) -> dict:
        """Retrieve the current state of a mailbox.

        :param name: string - (required) The name of the mailbox
        """

        result = await self.send_request(
            method="GET",
            uri=f"applications/{name}"
        )
        return self.parse_body(result.get('message_body'))

    async def subscribe(self, name: str, source: str) -> None:
        """Subscribe an application to a event source. Returns the state of the
        application after the subscriptions have changed

        :param name: string - (required) The name of the mailbox
        :param source: string - (required) URI for event source (channel:{channelId},
        bridge:{bridgeId}, endpoint:{tech}[/{resource}], deviceState:{deviceName}
        Allows comma separated values.
        """

        await self.send_request(
            method="POST",
            uri=f"applications/{name}/subscription?eventSource={source}"
        )

    async def unsubscribe(self, name: str, source: str) -> None:
        """Unsubscribe an application from an event source. Returns the state of the
        application after the subscriptions have changed

        :param name: string - (required) The name of the mailbox
        :param source: string - (required) URI for event source (channel:{channelId},
        bridge:{bridgeId}, endpoint:{tech}[/{resource}], deviceState:{deviceName}
        Allows comma separated values.
        """

        await self.send_request(
            method="DELETE",
            uri=f"applications/{name}/subscription?eventSource={source}"
        )

    async def filter(self, name: str, filter_obj: dict | None = None) -> None:
        """Filter application events types.

        Allowed and/or disallowed event type filtering can be done. The body
        (parameter) should specify a JSON key/value object that describes the type of
        event filtering needed. One, or both of the following keys can be designated:

        "allowed" - Specifies an allowed list of event types "disallowed" - Specifies
        a disallowed list of event types

        Further, each of those key's value should be a JSON array that holds zero,
        or more JSON key/value objects. Each of these objects must contain the
        following key with an associated value:

        "type" - The type name of the event to filter

        The value must be the string name (case sensitive) of the event type that
        needs filtering. For example:

        { "allowed": [ { "type": "StasisStart" }, { "type": "StasisEnd" } ] }

        As this specifies only an allowed list, then only those two event type
        messages are sent to the application. No other event messages are sent.

        The following rules apply:

        If the body is empty, both the allowed and disallowed filters are set empty.
        If both list types are given then both are set to their respective values
        (note, specifying an empty array for a given type sets that type to empty).
        If only one list type is given then only that type is set. The other type is
        not updated.
        An empty "allowed" list means all events are allowed.
        An empty "disallowed" list means no events are disallowed.
        Disallowed events take precedence over allowed events if the event type is
        specified in both lists.

        :param name: string - (required) The name of the mailbox
        :param filter_obj: object - Specify which event types to allow/disallow
        """

        if not filter_obj:
            filter_obj = {"allowed": [], "disallowed": []}

        await self.send_request(
            method="PUT",
            uri=f"applications/{name}/eventFilter",
            **filter_obj
        )
