#!/usr/bin/env python3

import json
import logging

import cli_args as cli
from cli_args import setup_cli_args
from mqtt_connection import MqttConnection
from utils import mqtt_broker_info
from utils import setup_logging
from utils import sleep

HOSTNAME = "hostname"
PORT = "port"

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Parse CLI args
    args = setup_cli_args(cli.mqtt_host, cli.verbose)

    # Setup logging
    setup_logging(level=args["loglevel"])


    # Define MQTT callbacks
    def on_connect(client, userdata, flags, rc):
        logger.info(
            "{0} connecting to {1}:{2}".format("Success" if rc == 0 else "Failure", userdata[HOSTNAME], userdata[PORT]))
        client.subscribe("#")


    def on_disconnect(client, userdata, rc):
        logger.info("Disconnected with result code: {0}".format(rc))


    def on_subscribe(client, userdata, mid, granted_qos):
        logger.info("Subscribed with message id: {0} QOS: {1}".format(mid, granted_qos))


    def on_message(client, userdata, msg):
        # Decode json object payload
        try:
            json_val = json.loads(bytes.decode(msg.payload))
            logger.info("{0} : {1}".format(msg.topic, json_val))
        except BaseException as e:
            logger.info("{0} : {1}".format(msg.topic, msg.payload))


    # Create MQTT connection
    hostname, port = mqtt_broker_info(args["mqtt_host"])
    mqtt_conn = MqttConnection(hostname, port, userdata={HOSTNAME: hostname, PORT: port})
    mqtt_conn.client.on_connect = on_connect
    mqtt_conn.client.on_disconnect = on_disconnect
    mqtt_conn.client.on_subscribe = on_subscribe
    mqtt_conn.client.on_message = on_message
    mqtt_conn.connect()

    try:
        sleep()
    except KeyboardInterrupt:
        pass

    print("Exiting...")
