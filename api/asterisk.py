from api.base import BaseAPI


class Asterisk(BaseAPI):
    def __init__(self, send_request):
        super().__init__(send_request)

    async def get_object(
        self, config_class: str, object_type: str, object_id: str
    ) -> list[dict]:
        """Retrieve a dynamic configuration object.

        :param config_class: string - The configuration class containing dynamic
        configuration objects.
        :param object_type: string - The type of configuration object to retrieve.
        :param object_id: string - The unique identifier of the object to retrieve.
        """

        result = await self.send_request(
            method="GET",
            uri=f"asterisk/config/dynamic/{config_class}/{object_type}/{object_id}",
        )
        return self.parse_body(result.get("message_body"))

    async def update_object(
        self,
        config_class: str,
        object_type: str,
        object_id: str,
        fields: dict | None = None,
    ) -> list[dict]:
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

        result = await self.send_request(
            method="PUT",
            uri=f"asterisk/config/dynamic/{config_class}/{object_type}/{object_id}",
            **fields,
        )
        return self.parse_body(result.get("message_body"))

    async def delete_object(
        self, config_class: str, object_type: str, object_id: str
    ) -> None:
        """Create or update a dynamic configuration object.

        :param config_class: string - The configuration class containing dynamic
        configuration objects.
        :param object_type: string - The type of configuration object to delete.
        :param object_id: string - The unique identifier of the object to delete.
        """

        await self.send_request(
            method="DELETE",
            uri=f"asterisk/config/dynamic/{config_class}/{object_type}/{object_id}",
        )

    async def get_info(self, only: str) -> dict:
        """Gets Asterisk system information.

        :param only: string - Filter information returned
        Allowed values: build, system, config, status
        Allows comma separated values.
        """

        uri = "asterisk/info"

        if only:
            uri += f"?only={only}"

        result = await self.send_request(method="GET", uri=uri)
        return self.parse_body(result.get("message_body"))

    async def ping(self) -> dict:
        """Ping Asterisk server."""

        result = await self.send_request(method="GET", uri="asterisk/ping")
        return self.parse_body(result.get("message_body"))

    async def list_modules(self) -> list[dict]:
        """List Asterisk modules."""

        result = await self.send_request(method="GET", uri="asterisk/modules")
        return self.parse_body(result.get("message_body"))

    async def get_module(self, name: str) -> dict:
        """Get Asterisk module information.

        :param name: string - (required) Module name.
        """

        result = await self.send_request(method="GET", uri=f"asterisk/modules/{name}")
        return self.parse_body(result.get("message_body"))

    async def load_module(self, name: str) -> None:
        """Load an Asterisk module.

        :param name: string - (required) Module name.
        """

        await self.send_request(method="POST", uri=f"asterisk/modules/{name}")

    async def unload_module(self, name: str) -> None:
        """Unload an Asterisk module.

        :param name: string - (required) Module name.
        """

        await self.send_request(method="DELETE", uri=f"asterisk/modules/{name}")

    async def reload_module(self, name: str) -> None:
        """Reload an Asterisk module.

        :param name: string - (required) Module name.
        """

        await self.send_request(method="PUT", uri=f"asterisk/modules/{name}")

    async def list_log_channels(self) -> list[dict]:
        """Gets Asterisk log channel information."""

        result = await self.send_request(method="GET", uri="asterisk/logging")
        return self.parse_body(result.get("message_body"))

    async def add_log(self, name: str, config: str) -> None:
        """Adds a log channel.

        :param name: string - (required) Name of the log channel.
        :param config: string - (required) levels of the log channel
        """

        await self.send_request(
            method="POST", uri=f"asterisk/logging/{name}?configuration={config}"
        )

    async def delete_log(self, name: str) -> None:
        """Deletes a log channel.

        :param name: string - (required) Name of the log channel.
        """

        await self.send_request(method="DELETE", uri=f"asterisk/logging/{name}")

    async def rotate_log(self, name: str) -> None:
        """Rotates a log channel.

        :param name: string - (required) Name of the log channel.
        """

        await self.send_request(method="PUT", uri=f"asterisk/logging/{name}/rotate")

    async def get_variable(self, variable: str) -> str:
        """Get the value of a global variable.

        :param variable: string - (required) The variable to get.
        """

        result = await self.send_request(
            method="GET", uri=f"asterisk/variable?variable={variable}"
        )
        return self.parse_body(result.get("message_body"))

    async def set_variable(self, variable: str, value: str | None = None) -> None:
        """Get the value of a global variable.

        :param variable: string - (required) The variable to get.
        :param value: string - The value to set the variable to
        """

        uri = f"asterisk/variable?variable={variable}"

        if value:
            uri += f"&value={value}"

        await self.send_request(method="POST", uri=uri)
