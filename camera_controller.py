#!/usr/bin/env python2

import json
import logging
import time
from threading import Thread

import arc852.cli_args as cli
from arc852.cli_args import setup_cli_args
from arc852.mqtt_connection import MqttConnection
from arc852.utils import mqtt_broker_info
from arc852.utils import setup_logging
from arc852.utils import sleep
from location_client import LocationClient

from constants import *

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Parse CLI args
    args = setup_cli_args(cli.mqtt_host, cli.grpc_host, cli.log_level)

    # Setup logging
    setup_logging(level=args["loglevel"])

    # Start location reader in thread
    locations = LocationClient(args["grpc_host"])
    locations.start()


    # Setup MQTT
    def on_connect(client, userdata, flags, rc):
        logger.info("Connected with result code: {0}".format(rc))
        Thread(target=publish_locations, args=(client, userdata)).start()


    def on_disconnect(client, userdata, rc):
        logger.info("Disconnected with result code: {0}".format(rc))


    def on_publish(client, userdata, mid):
        logger.info("Published value to {0} with message id {1}".format(COMMAND_TOPIC, mid))


    def publish_locations(client, userdata):
        while True:
            x_loc, y_loc = locations.get_xy()
            if x_loc is None or y_loc is None:
                logger.error("Received an invalid xy value")
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
    mqtt_conn = MqttConnection(*mqtt_broker_info(args["mqtt_host"]))
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
