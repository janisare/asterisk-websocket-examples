from typing import Any, TypeAlias
from .base import BaseAPI

ConfigTuple: TypeAlias = dict[str, Any]
ConfigTupleList: TypeAlias = list[ConfigTuple]
AsteriskInfo: TypeAlias = dict[str, Any]
AsteriskPing: TypeAlias = dict[str, Any]
Module: TypeAlias = dict[str, Any]
ModuleList: TypeAlias = list[Module]
LogChannel: TypeAlias = dict[str, Any]
LogChannelList: TypeAlias = list[LogChannel]
Variable: TypeAlias = dict[str, Any]


class Asterisk(BaseAPI):
    def __init__(self, send_request):
        super().__init__(send_request)

    def get_object(
        self, config_class: str, object_type: str, object_id: str
    ) -> ConfigTupleList:
        """Retrieve a dynamic configuration object.

        :param config_class: string - The configuration class containing dynamic
        configuration objects.
        :param object_type: string - The type of configuration object to retrieve.
        :param object_id: string - The unique identifier of the object to retrieve.
        """

        df = self.send_request(
            method="GET",
            uri=f"asterisk/config/dynamic/{config_class}/{object_type}/{object_id}",
        )
        df.addCallback(self.process_result)
        return df

    def update_object(
        self,
        config_class: str,
        object_type: str,
        object_id: str,
        fields: dict | None = None,
    ) -> ConfigTupleList:
        """Create or update a dynamic configuration object.

        :param config_class: string - The configuration class containing dynamic
        configuration objects.
        :param object_type: string - The type of configuration object to create or
        update.
        :param object_id: string - The unique identifier of the object to create or
        update.
        :param fields: containers - The body object should have a value that is a list
        of ConfigTuples, which provide the fields to update.
        Ex. [ { "attribute": "directmedia", "value": "false" } ]
        """

        if not fields:
            fields = {}

        df = self.send_request(
            method="PUT",
            uri=f"asterisk/config/dynamic/{config_class}/{object_type}/{object_id}",
            **fields,
        )
        df.addCallback(self.process_result)
        return df

    def delete_object(
        self, config_class: str, object_type: str, object_id: str
    ) -> None:
        """Create or update a dynamic configuration object.

        :param config_class: string - The configuration class containing dynamic
        configuration objects.
        :param object_type: string - The type of configuration object to delete.
        :param object_id: string - The unique identifier of the object to delete.
        """

        self.send_request(
            method="DELETE",
            uri=f"asterisk/config/dynamic/{config_class}/{object_type}/{object_id}",
        )

    def get_info(self, only: str) -> AsteriskInfo:
        """Gets Asterisk system information.

        :param only: string - Filter information returned
        Allowed values: build, system, config, status
        Allows comma separated values.
        """

        query_params: dict[str, str] = {}
        if only:
            query_params["only"] = only

        uri = self._build_uri("asterisk/info", query_params)
        df = self.send_request(method="GET", uri=uri)
        df.addCallback(self.process_result)
        return df

    def ping(self) -> AsteriskPing:
        """Ping Asterisk server."""

        df = self.send_request(method="GET", uri="asterisk/ping")
        df.addCallback(self.process_result)
        return df

    def list_modules(self) -> ModuleList:
        """List Asterisk modules."""

        df = self.send_request(method="GET", uri="asterisk/modules")
        df.addCallback(self.process_result)
        return df

    def get_module(self, name: str) -> Module:
        """Get Asterisk module information.

        :param name: string - (required) Module name.
        """

        df = self.send_request(method="GET", uri=f"asterisk/modules/{name}")
        df.addCallback(self.process_result)
        return df

    def load_module(self, name: str) -> None:
        """Load an Asterisk module.

        :param name: string - (required) Module name.
        """

        self.send_request(method="POST", uri=f"asterisk/modules/{name}")

    def unload_module(self, name: str) -> None:
        """Unload an Asterisk module.

        :param name: string - (required) Module name.
        """

        self.send_request(method="DELETE", uri=f"asterisk/modules/{name}")

    def reload_module(self, name: str) -> None:
        """Reload an Asterisk module.

        :param name: string - (required) Module name.
        """

        self.send_request(method="PUT", uri=f"asterisk/modules/{name}")

    def list_log_channels(self) -> LogChannelList:
        """Gets Asterisk log channel information."""

        df = self.send_request(method="GET", uri="asterisk/logging")
        df.addCallback(self.process_result)
        return df

    def add_log(self, name: str, config: str) -> None:
        """Adds a log channel.

        :param name: string - (required) Name of the log channel.
        :param config: string - (required) levels of the log channel
        """

        self.send_request(
            method="POST", uri=f"asterisk/logging/{name}?configuration={config}"
        )

    def delete_log(self, name: str) -> None:
        """Deletes a log channel.

        :param name: string - (required) Name of the log channel.
        """

        self.send_request(method="DELETE", uri=f"asterisk/logging/{name}")

    def rotate_log(self, name: str) -> None:
        """Rotates a log channel.

        :param name: string - (required) Name of the log channel.
        """

        self.send_request(method="PUT", uri=f"asterisk/logging/{name}/rotate")

    def get_variable(self, variable: str) -> Variable:
        """Get the value of a global variable.

        :param variable: string - (required) The variable to get.
        """

        df = self.send_request(
            method="GET", uri=f"asterisk/variable?variable={variable}"
        )
        df.addCallback(self.process_result)
        return df

    def set_variable(self, variable: str, value: str | None = None) -> None:
        """Get the value of a global variable.

        :param variable: string - (required) The variable to get.
        :param value: string - The value to set the variable to
        """

        query_params: dict[str, str] = {"variable": variable}
        if value:
            query_params["value"] = value

        uri = self._build_uri("asterisk/variable", query_params)
        self.send_request(method="POST", uri=uri)
