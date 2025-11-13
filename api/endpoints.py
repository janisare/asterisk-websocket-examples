from api.base import BaseAPI


class Endpoints(BaseAPI):
    def __init__(self, send_request):
        super().__init__(send_request)

    async def list(self) -> list[dict]:
        """List all endpoints."""

        result = await self.send_request(
            method="GET",
            uri="endpoints"
        )
        return self.parse_body(result.get('message_body'))

    async def list_by_tech(self, tech: str) -> list[dict]:
        """List available endpoints for a given endpoint technology.

        :param tech: string - Technology of the endpoints (pjsip,iax2,...)
        """

        result = await self.send_request(
            method="GET",
            uri=f"endpoints/{tech}"
        )
        return self.parse_body(result.get('message_body'))

    async def get(self, tech: str, resource: str) -> dict:
        """Details for an endpoint.

        :param tech: string - Technology of the endpoints (pjsip,iax2,...)
        :param resource: string - ID of the endpoint
        """

        result = await self.send_request(
            method="GET",
            uri=f"endpoints/{tech}/{resource}"
        )
        return self.parse_body(result.get('message_body'))

    async def send(
            self, to: str, sender: str, body: str, variables: dict | None = None
    ) -> None:
        """Send a message to some technology URI or endpoint.

        :param to: string - (required) The endpoint resource or technology specific
        URI to send the message to. Valid resources are pjsip, and xmpp.
        :param sender: string - (required) The endpoint resource or technology specific
        identity to send this message from. Valid resources are pjsip, and xmpp.
        :param body: string - The body of the message
        :param variables: containers -
        """

        uri = f"endpoints/sendMessage?to={to}&from={sender}&body={body}"

        if not variables:
            variables = {}

        await self.send_request(
            method="PUT",
            uri=uri,
            **variables
        )

    async def send_to_endpoint(
            self,
            tech: str,
            resource: str,
            sender: str,
            body: str,
            variables: dict | None = None
    ) -> None:
        """Send a message to some technology URI or endpoint.

        :param tech: string - Technology of the endpoints (pjsip,iax2,...)
        :param resource: string - ID of the endpoint
        URI to send the message to. Valid resources are pjsip, and xmpp.
        :param sender: string - (required) The endpoint resource or technology specific
        identity to send this message from. Valid resources are pjsip, and xmpp.
        :param body: string - The body of the message
        :param variables: containers -
        """

        uri = f"endpoints/{tech}/{resource}/sendMessage?from={sender}&body={body}"

        if not variables:
            variables = {}

        await self.send_request(
            method="PUT",
            uri=uri,
            **variables
        )

    async def refer(
            self, to: str, sender: str, refer_to: str, to_self: bool = False,
            variables: dict | None = None
    ):
        """Refer an endpoint or technology URI to some technology URI or endpoint.

        :param to: string - (required) The endpoint resource or technology specific URI that
        should be referred to somewhere. Valid resource is pjsip.
        :param sender: string - (required) The endpoint resource or technology specific identity
        to refer from.
        :param refer_to: string - (required) The endpoint resource or technology specific URI
        to refer to.
        :param to_self: boolean - If true and "refer_to" refers to an Asterisk endpoint, the
        "refer_to" value is set to point to this Asterisk endpoint - so the referee is
        referred to Asterisk. Otherwise, use the contact URI associated with the
        endpoint.
        :param variables: containers -
        """

        uri = f"endpoints/refer?to={to}&from={sender}&refer_to={refer_to}&to_self={to_self}"

        result = await self.send_request(
            method="POST",
            uri=uri,
            **variables
        )
        return self.parse_body(result.get('message_body'))

    async def refer_to_endpoint(
            self,
            tech: str,
            resource: str,
            sender: str,
            refer_to: str,
            to_self: bool = False,
            variables: dict | None = None
    ):
        """Refer an endpoint or technology URI to some technology URI or endpoint.

        :param tech: string - Technology of the endpoints (pjsip,iax2,...)
        :param resource: string - ID of the endpoint
        :param sender: string - (required) The endpoint resource or technology specific identity
        to refer from.
        :param refer_to: string - (required) The endpoint resource or technology specific URI
        to refer to.
        :param to_self: boolean - If true and "refer_to" refers to an Asterisk endpoint, the
        "refer_to" value is set to point to this Asterisk endpoint - so the referee is
        referred to Asterisk. Otherwise, use the contact URI associated with the
        endpoint.
        :param variables: containers -
        """

        uri = f"endpoints/{tech}/{resource}/refer?from={sender}&refer_to={refer_to}&to_self={to_self}"

        result = await self.send_request(
            method="POST",
            uri=uri,
            **variables
        )
        return self.parse_body(result.get('message_body'))
