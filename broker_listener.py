#!/usr/bin/env python3

import argparse
import json
import logging
from logging import info

from common_constants import LOGGING_ARGS
from common_utils import mqtt_broker_info
from common_utils import sleep
from mqtt_connection import MqttConnection

HOSTNAME = "hostname"
PORT = "port"


def on_connect(client, userdata, flags, rc):
    info("{0} connecting to {1}:{2}".format("Success" if rc == 0 else "Failure", userdata[HOSTNAME], userdata[PORT]))
    client.subscribe("#")


def on_disconnect(client, userdata, rc):
    info("Disconnected with result code: {0}".format(rc))


def on_subscribe(client, userdata, mid, granted_qos):
    info("Subscribed with message id: {0} QOS: {1}".format(mid, granted_qos))


def on_message(client, userdata, msg):
    # Decode json object payload
    try:
        json_val = json.loads(bytes.decode(msg.payload))
        info("{0} : {1}".format(msg.topic, json_val))
    except BaseException as e:
        info("{0} : {1}".format(msg.topic, msg.payload))



if __name__ == "__main__":
    # Parse CLI args
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mqtt", required=True, help="MQTT broker hostname")
    args = vars(parser.parse_args())

    # Setup logging
    logging.basicConfig(**LOGGING_ARGS)

    # Create MQTT connection
    hostname, port = mqtt_broker_info(args["mqtt"])
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
