#!/usr/bin/env python3

import argparse
import json
import logging
import sys
import time

from mqtt_connection import MqttConnection
from utils import FORMAT_DEFAULT
from utils import mqtt_broker_info


def on_connect(client, userdata, flags, rc):
    logging.info("{0} connecting to {1}:{2}".format("Success" if rc == 0 else "Failure",
                                                    userdata["hostname"],
                                                    userdata["port"]))
    client.subscribe("/#")


def on_disconnect(client, userdata, rc):
    print("Disconnected with result code: {0}".format(rc))


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed with message id: {0} QOS: {1}".format(mid, granted_qos))


def on_message(client, userdata, msg):
    json_val = json.loads(bytes.decode(msg.payload))
    print("{0} : {1}".format(msg.topic, json_val))


if __name__ == "__main__":
    # Parse CLI args
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mqtt", required=True, help="MQTT broker hostname")
    args = vars(parser.parse_args())

    # Setup logging
    logging.basicConfig(stream=sys.stderr, level=logging.INFO, format=FORMAT_DEFAULT)

    # Create MQTT connection
    mqtt_conn = MqttConnection(*mqtt_broker_info(args["mqtt"]))
    mqtt_conn.client.on_connect = on_connect
    mqtt_conn.client.on_disconnect = on_disconnect
    mqtt_conn.client.on_subscribe = on_subscribe
    mqtt_conn.client.on_message = on_message
    mqtt_conn.connect()

    time.sleep(1000)

    print("Exiting...")
