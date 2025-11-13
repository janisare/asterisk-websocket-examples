from api.base import BaseAPI


class Mailboxes(BaseAPI):
    def __init__(self, send_request):
        super().__init__(send_request)

    async def list(self) -> list[dict]:
        """List all mailboxes."""

        result = await self.send_request(method="GET", uri="mailboxes")
        return self.parse_body(result.get("message_body"))

    async def get(self, name: str) -> dict:
        """Retrieve the current state of a mailbox.

        :param name: string - (required) The name of the mailbox
        """

        result = await self.send_request(method="GET", uri=f"mailboxes/{name}")
        return self.parse_body(result.get("message_body"))

    async def update(self, name: str, old_count: int, new_count: int) -> dict:
        """Change the state of a mailbox. (Note - implicitly creates the mailbox).

        :param name: string - (required) The name of the mailbox
        :param old_count: int - (required) The old message count of the mailbox
        :param new_count: int - (required) Count of new messages in the mailbox
        """

        result = await self.send_request(
            method="PUT",
            uri=f"mailboxes/{name}?oldMessages={old_count}&newMessages={new_count}",
        )
        return self.parse_body(result.get("message_body"))

    async def delete(self, name: str) -> None:
        """Destroy a mailbox.

        :param name: string - (required) The name of the mailbox
        """

        await self.send_request(method="DELETE", uri=f"mailboxes/{name}")
