#!/usr/bin/env python3

"""
Copyright (C) 2025, Sangoma Technologies Corporation
George T Joseph <gjoseph@sangoma.com>

This program is free software, distributed under the terms of
the Apache License Version 2.0.
"""
import uuid
from argparse import ArgumentParser as ArgParser
import asyncio
import json
import logging
import sys
import traceback

from my_ari_websocket import AstAriWebSocketClient

from api.bridges import Bridges
from api.sounds import Sounds

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s %(message)s",
    datefmt="[%Y-%m-%d %H:%M:%S]",
    level=logging.INFO,
)


class Session:
    def __init__(self, incoming, incoming_name):
        self.incoming_channel = incoming
        self.incoming_channel_name = incoming_name
        self.other_channel = None
        self.other_channel_name = None
        self.bridge_id = None
        self.conn_id = None


class WSClient(AstAriWebSocketClient):
    def __init__(self, host, port, app, credentials, tag=None, log_level=logging.INFO):
        super().__init__(host, port, app, credentials, tag, log_level)
        self.sessions_by_incoming = {}
        self.tag = tag
        self.log_level = log_level
        self.bridges = Bridges(self.send_request)
        self.sounds = Sounds(self.send_request)

    async def handle_stasisstart(self, msg):
        logger.info(f"StasisStart: {msg['channel']}")

        if "incoming" in msg["channel"]["dialplan"]["app_data"]:
            incoming_id = msg["channel"]["id"]
            sess = Session(incoming_id, msg["channel"]["name"])
            self.sessions_by_incoming[incoming_id] = sess
            logger.info("Creating other channel")

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

            logger.info("Dialing other channel")
            await self.send_request(
                "POST",
                f"channels/{sess.other_channel}/dial?caller={incoming_id}&timeout=5",
            )

    async def handle_dial(self, msg):
        chan_name = msg["peer"]["name"]

        logger.info(f"Dial: {chan_name} Status: '{msg['dialstatus']}'")

    async def handle_stasisend(self, msg):
        sess = None
        if "incoming" in msg["channel"]["dialplan"]["app_data"]:
            sess = self.sessions_by_incoming.get(msg["channel"]["id"])
            if sess is not None:
                if sess.other_channel is not None:
                    logger.info("Hanging up ws %s" % sess.other_channel)
                    await self.send_request(
                        "DELETE", "channels/%s" % sess.other_channel
                    )
                del self.sessions_by_incoming[sess.incoming_channel]
                sess.incoming_channel = None

        if sess is not None and sess.bridge_id is not None:
            await self.send_request("DELETE", "bridges/%s" % sess.bridge_id)
            sess.bridge_id = None


async def main(args):
    event_handler = WSClient(
        args.ari_host,
        args.ari_port,
        args.stasis_app,
        (args.ari_user, args.ari_password),
        log_level=logging.INFO,
    )
    try:
        await event_handler.connect()
    except KeyboardInterrupt:
        return
    except Exception as e:
        logger.error(f"Error connecting to ARI: {e}")
        traceback.print_exc()
        return


if __name__ == "__main__":
    description = "Command line utility to test ARI client connections"

    parser = ArgParser(description=description)
    parser.add_argument(
        "-ah",
        "--ari-host",
        type=str,
        help="Asterisk ARI Host to connect to",
        required=False,
        default="localhost",
    )
    parser.add_argument(
        "-ap",
        "--ari-port",
        type=str,
        help="Port to connect to",
        required=False,
        default="8088",
    )
    parser.add_argument(
        "-a", "--stasis-app", type=str, help="Stasis app to register as", required=True
    )
    parser.add_argument(
        "-aU", "--ari-user", type=str, help="ARI user to authenticate as", required=True
    )
    parser.add_argument(
        "-aP", "--ari-password", type=str, help="Password for ARI user", required=True
    )
    args = parser.parse_args()
    if not args:
        sys.exit(1)

    try:
        asyncio.run(main(args))
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f"Error connecting to ARI: {e}")
        traceback.print_exc()
    sys.exit(0)
