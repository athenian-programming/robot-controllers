import logging
import socket
import sys
from threading import Thread

import paho.mqtt.client as paho


class MqttConnection:
    def __init__(self, hostname, port):
        self.__hostname = hostname
        self.__port = port
        self.__connected = False
        self.__client = paho.Client()

    @property
    def client(self):
        return self.__client

    def connect(self):
        def connect_to_mqtt():
            try:
                # Connect to MQTT broker
                logging.info("Connecting to MQTT broker at {0}:{1}...".format(self.__hostname, self.__port))
                self.__client.connect(self.__hostname, port=self.__port, keepalive=60)
                self.__client.loop_forever()
            except socket.error:
                logging.error("Cannot connect to MQTT broker at: {0}:{1}".format(self.__hostname, self.__port))
                sys.exit()

        # Run connection in a thread
        Thread(target=connect_to_mqtt, args=()).start()
