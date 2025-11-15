from typing import Any, TypeAlias
from .base import BaseAPI

Mailbox: TypeAlias = dict[str, Any]
MailboxList: TypeAlias = list[Mailbox]


class Mailboxes(BaseAPI):
    def __init__(self, send_request):
        super().__init__(send_request)

    def list(self) -> MailboxList:
        """List all mailboxes."""

        df = self.send_request(method="GET", uri="mailboxes")
        df.addCallback(self.process_result)
        return df

    def get(self, name: str) -> Mailbox:
        """Retrieve the current state of a mailbox.

        :param name: string - (required) The name of the mailbox
        """

        df = self.send_request(method="GET", uri=f"mailboxes/{name}")
        df.addCallback(self.process_result)
        return df

    def update(self, name: str, old_count: int, new_count: int) -> None:
        """Change the state of a mailbox. (Note - implicitly creates the mailbox).

        :param name: string - (required) The name of the mailbox
        :param old_count: int - (required) The old message count of the mailbox
        :param new_count: int - (required) Count of new messages in the mailbox
        """

        query_params: dict[str, str] = {
            "oldMessages": str(old_count),
            "newMessages": str(new_count),
        }
        uri = self._build_uri(f"mailboxes/{name}", query_params)

        self.send_request(
            method="PUT",
            uri=uri,
        )

    def delete(self, name: str) -> None:
        """Destroy a mailbox.

        :param name: string - (required) The name of the mailbox
        """

        self.send_request(method="DELETE", uri=f"mailboxes/{name}")
