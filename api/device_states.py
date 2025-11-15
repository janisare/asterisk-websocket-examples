from typing import Any, TypeAlias
from .base import BaseAPI

DeviceState: TypeAlias = dict[str, Any]
DeviceStateList: TypeAlias = list[DeviceState]


class DeviceStates(BaseAPI):
    def __init__(self, send_request):
        super().__init__(send_request)

    def list(self) -> DeviceStateList:
        """List all ARI controlled device states."""

        df = self.send_request(method="GET", uri="deviceStates")
        df.addCallback(self.process_result)
        return df

    def get(self, name: str) -> DeviceState:
        """Retrieve the current state of a device.

        :param name: string - (required) Name of the device
        """

        df = self.send_request(method="GET", uri=f"deviceStates/{name}")
        df.addCallback(self.process_result)
        return df

    def update(self, name: str, state: str) -> None:
        """Change the state of a device controlled by ARI. (Note - implicitly creates
        the device state).

        :param name: string - (required) Name of the device
        :param state: string - (required) Device state value
        Allowed values: NOT_INUSE, INUSE, BUSY, INVALID, UNAVAILABLE, RINGING,
        RINGINUSE, ONHOLD
        """

        query_params: dict[str, str] = {"deviceState": state}
        uri = self._build_uri(f"deviceStates/{name}", query_params)
        self.send_request(method="PUT", uri=uri)

    def delete(self, name: str) -> None:
        """Destroy a device-state controlled by ARI.

        :param name: string - (required) Name of the device
        """

        self.send_request(method="DELETE", uri=f"deviceStates/{name}")
