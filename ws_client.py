import json
import uuid

from twisted.internet import defer, reactor
from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol
from twisted.logger import Logger

from api.bridges import Bridges
from api.sounds import Sounds


class Session:
    def __init__(self, incoming, incoming_name):
        self.incoming_channel = incoming
        self.incoming_channel_name = incoming_name
        self.other_channel = None
        self.other_channel_name = None
        self.bridge_id = None
        self.conn_id = None


class MyClientProtocol(WebSocketClientProtocol):
    def __init__(self):
        super().__init__()
        self.requests = {}
        self.sessions_by_incoming = {}
        self.log = Logger()

        self.bridges = Bridges(self.send_request)
        self.sounds = Sounds(self.send_request)

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onOpen(self):
        self.sendMessage(u"Hello, world!".encode('utf8'))

    async def send_request(
        self, method, uri, wait_for_response=True, callback=None, **kwargs
    ):
        """
        Sends a REST request over the WebSocket connection.
        :param method: The HTTP method (GET, POST, etc.) to use for the request.
        :param uri: The URI for the REST request.
        :param wait_for_response: Whether to wait for a response from the server.
        :param callback: An optional callback function to process the response.
        :param kwargs: Additional parameters to include in the request.
        :return: The response from the server, or the result of the callback function.
        """
        uuidstr = kwargs.pop("request_id", str(uuid.uuid4()))
        req = {
            "type": "RESTRequest",
            "request_id": uuidstr,
            "method": method,
            "uri": uri,
        }

        for k, v in kwargs.items():
            req[k] = v

        msg = json.dumps(req)
        rtnobj = {"result": ""}

        # if wait_for_response:
        #     rtnobj["event"] = asyncio.Event()

        self.requests[uuidstr] = rtnobj
        self.log.info(f"RESTRequest: {method} {uri} {uuidstr}")
        x = self.sendMessage(msg.encode("utf-8"))
        print("SENDING MESSAGE", type(x), x)
        # await self.websocket.send(msg.encode("utf-8"), text=True)
        # if wait_for_response:
        #     await rtnobj["event"].wait()
        del self.requests[uuidstr]
        resp = rtnobj["result"]

        print("I AM RESP", resp)

        self.log.info(
            f"RESTResponse: {method} {uri} {resp['status_code']} {resp['reason_phrase']}",
        )
        if callback is not None:
            return callback(self.websocket, uuidstr, req, rtnobj["result"])

        print("RETURING>>>>>>>", rtnobj["result"])
        return rtnobj["result"]

    async def handle_stasisstart(self, msg):
        self.log.info(f"StasisStart: {msg['channel']}")

        if "incoming" in msg["channel"]["dialplan"]["app_data"]:
            incoming_id = msg["channel"]["id"]
            sess = Session(incoming_id, msg["channel"]["name"])
            self.sessions_by_incoming[incoming_id] = sess
            self.log.info("Creating other channel")

            sess.bridge_id = str(uuid.uuid4())
            x = await self.bridges.create(name="bridge123", bridge_id=sess.bridge_id)
            print("BRIDGE::: {}".format(x))

            await self.bridges.add_channel(
                bridge_id=sess.bridge_id, channel=sess.incoming_channel
            )

            x = await self.bridges.get(bridge_id=sess.bridge_id)
            print("BRIDGE xxx::: {}".format(x))

            x = await self.bridges.record(
                bridge_id=sess.bridge_id, name="rec123", recording_format="wav"
            )
            print("RESULT zzzz::: {}".format(x))

            x = await self.bridges.get(bridge_id=sess.bridge_id)
            print("BRIDGE yyy::: {}".format(x))

            resp = await self.send_request(
                "POST",
                "channels/create",
                query_strings=[
                    {"name": "endpoint", "value": "PJSIP/123456@asterisk-operator"},
                    {"name": "app", "value": self.app},
                    {"name": "appArgs", "value": "dialed"},
                    {"name": "originator", "value": incoming_id},
                ],
            )
            msg_body = json.loads(resp.get("message_body"))
            sess.other_channel = msg_body["id"]
            sess.other_channel_name = msg_body["name"]

            self.log.info("Dialing other channel")
            await self.send_request(
                "POST",
                f"channels/{sess.other_channel}/dial?caller={incoming_id}&timeout=5",
            )

    async def handle_dial(self, msg):
        chan_name = msg["peer"]["name"]

        self.log.info(f"Dial: {chan_name} Status: '{msg['dialstatus']}'")

    async def handle_stasisend(self, msg):
        sess = None
        if "incoming" in msg["channel"]["dialplan"]["app_data"]:
            sess = self.sessions_by_incoming.get(msg["channel"]["id"])
            if sess is not None:
                if sess.other_channel is not None:
                    self.log.info("Hanging up ws %s" % sess.other_channel)
                    await self.send_request(
                        "DELETE", "channels/%s" % sess.other_channel
                    )
                del self.sessions_by_incoming[sess.incoming_channel]
                sess.incoming_channel = None

        if sess is not None and sess.bridge_id is not None:
            await self.send_request("DELETE", "bridges/%s" % sess.bridge_id)
            sess.bridge_id = None

    def get_function(self, func):
        """
        Returns a callable function based on the provided function name.
        :param func: The name of the function to retrieve.
        :return: The callable function if it exists, otherwise None.
        """
        if hasattr(self, func):
            attr = getattr(self, func)
            if callable(attr):
                return attr
            return None

    async def process_rest_response(self, msg):
        """
        Processes a REST response message received over the WebSocket.
        :param msg: The REST response message.
        """

        if msg["type"] == "RESTResponse":
            reqid = msg["request_id"]
            req = self.requests.get(reqid)
            if req is None:
                self.log.error(f"Pending request {reqid} not found.")
                return
            req["result"] = msg
            event = req.get("event", None)
            if event is not None:
                event.set()

    async def handle_any(self, msg):
        """
        Handles any ARI event that does not have a specific handler.
        :param rest_handler: The REST handler to use for processing the event.
        :param msg: The ARI event message.
        """

        if msg["type"] == "ChannelVarset":
            return
        et = msg["type"]
        ts = msg["timestamp"]
        del msg["timestamp"]
        del msg["type"]
        msg["timestamp"] = ts
        name = ""
        if "bridge" in msg:
            name = (
                msg["bridge"]["name"]
                if len(msg["bridge"]["name"]) > 0
                else msg["bridge"]["id"]
            )
        if "channel" in msg:
            name += f" {msg['channel']['name']}"

        self.log.info(f"Received {et} {name}")

    async def process_message(self, msg):
        """
        Processes an incoming ARI event message and call a handler if it exists.
        :param msg: The ARI event message to process.
        """

        if msg["type"] == "RESTResponse":
            await self.process_rest_response(msg)
            return
        handler_name = f"handle_{msg['type'].lower()}"
        func = self.get_function(handler_name)
        await self.handle_any(msg)
        if func is not None:
            await func(msg)

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))
            msg = json.loads(payload.decode('utf8'))
            coro = self.process_message(msg)
            defer.Deferred.fromCoroutine(coro)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


def main():
    print("Hello, world!")

    uri = f"ws://127.0.0.1:8088/ari/events?subscribeAll=false&app=test_inbound_connection&api_key={'asterisk:asterisk'}"
    factory = WebSocketClientFactory(uri)
    factory.protocol = MyClientProtocol
    reactor.connectTCP("127.0.0.1", 8088, factory)


if __name__ == '__main__':
    main()
    reactor.run()
