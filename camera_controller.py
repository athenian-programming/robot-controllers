#!/usr/bin/env python3

import argparse
import logging

from mqtt_connection import MqttConnection
from ..common_robotics_python.utils import LOGGING_ARGS
from ..common_robotics_python.utils import TOPIC
from ..common_robotics_python.utils import mqtt_broker_info
from ..opencv_object_tracking.location_client import LocationClient

if __name__ == "__main__":
    # Parse CLI args
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--grpc", required=True, help="gRPC location server hostname")
    parser.add_argument("-m", "--mqtt", required=True, help="MQTT broker hostname")
    args = vars(parser.parse_args())

    # Setup logging
    logging.basicConfig(**LOGGING_ARGS)

    # Start location reader in thread
    locations = LocationClient(args["grpc"])
    locations.start()


    # Setup MQTT
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code: {0}".format(rc))


    def on_disconnect(client, userdata, rc):
        print("Disconnected with result code: {0}".format(rc))


    def on_publish(client, userdata, mid):
        print("Published value to {0} with message id {1}".format(TOPIC, mid))


    # Create MQTT connection
    mqtt_conn = MqttConnection(*mqtt_broker_info(args["mqtt"]))
    mqtt_conn.client.on_connect = on_connect
    mqtt_conn.client.on_disconnect = on_disconnect
    mqtt_conn.client.on_publish = on_publish
    mqtt_conn.connect()
