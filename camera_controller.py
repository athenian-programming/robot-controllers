#!/usr/bin/env python2

import argparse
import json
import logging
import time
from logging import info
from threading import Thread

from common_constants import LOGGING_ARGS
from common_utils import mqtt_broker_info
from common_utils import sleep
from constants import *
from location_client import LocationClient
from mqtt_connection import MqttConnection

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
        info("Connected with result code: {0}".format(rc))
        Thread(target=publish_locations, args=(client, userdata)).start()


    def on_disconnect(client, userdata, rc):
        info("Disconnected with result code: {0}".format(rc))


    def on_publish(client, userdata, mid):
        info("Published value to {0} with message id {1}".format(COMMAND_TOPIC, mid))


    def publish_locations(client, userdata):
        while True:
            x_loc, y_loc = locations.get_xy()
            if x_loc is None or y_loc is None:
                logging.error("Received an invalid xy value")
                time.sleep(1)
                continue
            x, width, increment = x_loc[:3]
            y, height = y_loc[:2]
            width_mid = width / 2
            height_mid = height / 2
            y_dist = height_mid - y
            x_dist = width_mid - x
            direction = None
            speed = 0
            if abs(y_dist) > increment:
                speed = abs(int((float(y_dist) / height_mid) * 10))
                if y > height_mid:
                    direction = BACKWARD
                else:
                    direction = FORWARD
            else:
                speed = 0
                direction = STOP

            if direction is None:
                continue

            # Encode payload into json object
            json_val = json.dumps({DIRECTION: direction, SPEED: speed})
            result, mid = mqtt_conn.client.publish(COMMAND_TOPIC, payload=json_val.encode('utf-8'))

    # Create MQTT connection
    mqtt_conn = MqttConnection(*mqtt_broker_info(args["mqtt"]))
    mqtt_conn.client.on_connect = on_connect
    mqtt_conn.client.on_disconnect = on_disconnect
    mqtt_conn.client.on_publish = on_publish
    mqtt_conn.connect()

    try:
        sleep()
    except KeyboardInterrupt:
        mqtt_conn.disconnect()
    finally:
        locations.stop()

    print("Exiting...")
