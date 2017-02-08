#!/usr/bin/env python3

import json
import logging
import sys

import cli_args as cli
from cli_args import setup_cli_args
from mqtt_connection import MqttConnection
from utils import is_python3
from utils import mqtt_broker_info
from utils import setup_logging

from constants import *

if is_python3():
    import tkinter as tk
else:
    import Tkinter as tk

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Parse CLI args
    args = setup_cli_args(cli.mqtt_host, cli.verbose)

    # Setup logging
    setup_logging(level=args["loglevel"])


    # Define MQTT callbacks
    def on_connect(client, userdata, flags, rc):
        logger.info("Connected with result code: {0}".format(rc))


    def on_disconnect(client, userdata, rc):
        logger.info("Disconnected with result code: {0}".format(rc))


    def on_publish(client, userdata, mid):
        logger.info("Published value to {0} with message id {1}".format(COMMAND_TOPIC, mid))


    # Create MQTT connection
    mqtt_conn = MqttConnection(*mqtt_broker_info(args["mqtt_host"]))
    mqtt_conn.client.on_connect = on_connect
    mqtt_conn.client.on_disconnect = on_disconnect
    mqtt_conn.client.on_publish = on_publish
    mqtt_conn.connect()


    # Define TK callbacks
    def update_display(direction, speed):
        labels[DIRECTION]["text"] = "Direction: {0}".format(direction)
        labels[SPEED]["text"] = "Speed: {0}".format(speed)


    def publish_value():
        global direction, speed
        update_display(direction, speed)
        # Encode payload into json object
        json_val = json.dumps({DIRECTION: direction, SPEED: speed})
        result, mid = mqtt_conn.client.publish(COMMAND_TOPIC, payload=json_val.encode('utf-8'))


    def set_direction(cmd):
        global direction
        direction = cmd
        publish_value()


    def on_key(event):
        global direction, speed
        key_clicked = eval(repr(event.char))
        if key_clicked == "+" or key_clicked == "=":
            if speed < 10:
                speed += 1
                publish_value()
        elif key_clicked == "-" or key_clicked == "_":
            if speed > 0:
                speed -= 1
                publish_value()
        elif key_clicked == " ":
            direction = STOP
            speed = 0
            publish_value()
        elif key_clicked == "q":
            mqtt_conn.disconnect()
            sys.exit()
        else:
            print("Pressed {0}".format(key_clicked))


    def on_mouseclick(event):
        root.focus_set()
        print("Clicked at {0},{1}".format(event.x, event.y))


    direction = STOP
    speed = 1

    root = tk.Tk()
    root.title("Keyboard Controller")
    root.focus()
    # For bind() details, see: http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
    # root.bind("<Button-1>", on_mouseclick)
    root.bind("<Key>", on_key)
    root.bind("<Left>", lambda event: set_direction(LEFT))
    root.bind("<Right>", lambda event: set_direction(RIGHT))
    root.bind("<Up>", lambda event: set_direction(FORWARD))
    root.bind("<Down>", lambda event: set_direction(BACKWARD))

    canvas = tk.Canvas(root, bg="white", width=200, height=150)
    canvas.pack()

    labels = {}
    args = {"text": "", "bg": "red", "height": 2, "width": 20, "font": ('courier', 20, 'bold')}
    labels[DIRECTION] = tk.Label(canvas, args)
    labels[DIRECTION].pack(expand=tk.YES, fill=tk.BOTH)
    labels[SPEED] = tk.Label(canvas, args)
    labels[SPEED].pack(expand=tk.YES, fill=tk.BOTH)

    update_display(direction, speed)

    root.mainloop()
