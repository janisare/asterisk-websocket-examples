import json
import uuid
from typing import Any
from twisted.internet import defer, reactor
from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol
from twisted.logger import Logger

from api.bridges import Bridges
from api.channels import Channels
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
        self.app = "test_inbound_connection"
        self.requests = {}
        self.sessions_by_incoming = {}
        self.log = Logger()

        self.bridges = Bridges(self.send_request)
        self.sounds = Sounds(self.send_request)
        self.channels = Channels(self.send_request)

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onOpen(self):
        pass
        # self.sendMessage(u"Hello, world!".encode('utf8'))

    def send_request(
        self, method, uri, wait_for_response=True, **kwargs
    ) -> defer.Deferred | None:
        """
        Sends a REST request over the WebSocket connection.
        :param method: The HTTP method (GET, POST, etc.) to use for the request.
        :param uri: The URI for the REST request.
        :param wait_for_response: Whether to wait for a response from the server.
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
        rtnobj: dict[str, Any] = {"result": ""}

        response_df = defer.Deferred()

        if wait_for_response:
            rtnobj["event"] = response_df
            self.requests[uuidstr] = rtnobj

        self.log.info(f"RESTRequest: {method} {uri} {uuidstr}")
        self.sendMessage(msg.encode("utf-8"))

        if wait_for_response:
            return response_df
        return None

    def handle_stasisstart(self, msg):
        self.log.info(f"StasisStart: {msg['channel']}")

        if "incoming" in msg["channel"]["dialplan"]["app_data"]:
            incoming_id = msg["channel"]["id"]
            sess = Session(incoming_id, msg["channel"]["name"])
            self.sessions_by_incoming[incoming_id] = sess
            self.log.info("Creating other channel")

            sess.bridge_id = str(uuid.uuid4())
            self.bridges.create(name="bridge123", bridge_id=sess.bridge_id)

            self.bridges.add_channel(
                bridge_id=sess.bridge_id, channel=sess.incoming_channel
            )

            def on_bridge(resp):
                print("HELLO IM BRIDGE:::::::::::::::::::::::", resp)

            bridge_df = self.bridges.get(bridge_id=sess.bridge_id)
            bridge_df.addCallback(on_bridge)

            self.bridges.record(
                bridge_id=sess.bridge_id, name="rec123", recording_format="wav"
            )

            self.bridges.get(bridge_id=sess.bridge_id)

            def on_new_channel(resp):
                print("ON NEW CHANNEL:::::", resp)
                sess.other_channel = resp["id"]
                sess.other_channel_name = resp["name"]

                self.log.info("Dialing other channel")
                self.send_request(
                    "POST",
                    f"channels/{sess.other_channel}/dial?caller={incoming_id}&timeout=5",
                )

            df = self.channels.create(
                endpoint="PJSIP/123456@asterisk-operator",
                app=self.app,
                app_args="dialed",
                originator=incoming_id,
            )
            df.addCallback(on_new_channel)

    def handle_dial(self, msg):
        chan_name = msg["peer"]["name"]
        self.log.info(f"Dial: {chan_name} Status: '{msg['dialstatus']}'")

    def handle_stasisend(self, msg):
        sess = None
        if "incoming" in msg["channel"]["dialplan"]["app_data"]:
            sess = self.sessions_by_incoming.get(msg["channel"]["id"])
            if sess is not None:
                if sess.other_channel is not None:
                    self.log.info("Hanging up ws %s" % sess.other_channel)
                    self.send_request(
                        "DELETE",
                        "channels/%s" % sess.other_channel,
                        wait_for_response=False,
                    )
                del self.sessions_by_incoming[sess.incoming_channel]
                sess.incoming_channel = None

        if sess is not None and sess.bridge_id is not None:
            self.bridges.delete(sess.bridge_id)
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
        return None

    def process_rest_response(self, msg) -> None:
        """
        Processes a REST response message received over the WebSocket.
        :param msg: The REST response message.
        """

        if msg["type"] == "RESTResponse":
            request_id = msg["request_id"]
            req = self.requests.get(request_id)
            if req is None:
                self.log.error(f"Pending request {request_id} not found.")
                return
            req["result"] = msg
            event: defer.Deferred | None = req.get("event", None)
            if event is not None:
                event.callback(req["result"])

    def handle_any(self, msg):
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

    def process_message(self, msg) -> None:
        """
        Processes an incoming ARI event message and call a handler if it exists.
        :param msg: The ARI event message to process.
        """

        if msg["type"] == "RESTResponse":
            self.process_rest_response(msg)

        handler_name = f"handle_{msg['type'].lower()}"
        func = self.get_function(handler_name)
        self.handle_any(msg)
        if func is not None:
            func(msg)

    def onMessage(self, payload, isBinary) -> None:
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            # print("Text message received: {0}".format(payload.decode('utf8')))
            msg = json.loads(payload.decode("utf8"))
            self.process_message(msg)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


def main():
    print("Hello, world!")

    uri = f"ws://127.0.0.1:8088/ari/events?subscribeAll=false&app=test_inbound_connection&api_key={'asterisk:asterisk'}"
    factory = WebSocketClientFactory(uri)
    factory.protocol = MyClientProtocol
    reactor.connectTCP("127.0.0.1", 8088, factory)


if __name__ == "__main__":
    main()
    reactor.run()
