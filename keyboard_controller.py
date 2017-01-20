#!/usr/bin/env python3

import argparse
import json
import logging
import sys

from mqtt_connection import MqttConnection
from utils import FORMAT_DEFAULT
from utils import is_python3
from utils import mqtt_broker_info

if is_python3():
    import tkinter as tk
else:
    import Tkinter as tk

COMMAND = "/roborio/keyboard/command"
LEFT = "LEFT"
RIGHT = "RIGHT"
FORWARD = "FORWARD"
BACKWARD = "BACKWARD"

if __name__ == "__main__":
    # Parse CLI args
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mqtt", required=True, help="MQTT broker hostname")
    args = vars(parser.parse_args())

    # Setup logging
    logging.basicConfig(stream=sys.stderr, level=logging.INFO, format=FORMAT_DEFAULT)


    # Setup MQTT
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code: {0}".format(rc))


    def on_disconnect(client, userdata, rc):
        print("Disconnected with result code: {0}".format(rc))


    def on_publish(client, userdata, mid):
        print("Published value to {0} with message id {1}".format(COMMAND, mid))


    # Create MQTT connection
    mqtt_conn = MqttConnection(*mqtt_broker_info(args["mqtt"]))
    mqtt_conn.client.on_connect = on_connect
    mqtt_conn.client.on_disconnect = on_disconnect
    mqtt_conn.client.on_publish = on_publish
    mqtt_conn.connect()


    # Setup tkinter
    def publish(cmd):
        label["text"] = cmd
        json_val = json.dumps({"command": cmd, "speed": 10, "time": 5})
        result, mid = mqtt_conn.client.publish(COMMAND, payload=json_val.encode('utf-8'))


    def on_key(event):
        key_clicked = repr(event.char)
        label["text"] = "Pressed {0}".format(key_clicked)
        if key_clicked == "'q'":
            mqtt_conn.disconnect()
            sys.exit()


    def on_mouseclick(event):
        root.focus_set()
        if event.y >= 0:
            label["text"] = "Clicked at {0},{1}".format(event.x, event.y)


    root = tk.Tk()
    # For bind() details, see: http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
    root.bind("<Button-1>", on_mouseclick)
    root.bind("<Key>", on_key)
    root.bind('<Left>', lambda event: publish(LEFT))
    root.bind('<Right>', lambda event: publish(RIGHT))
    root.bind('<Up>', lambda event: publish(FORWARD))
    root.bind('<Down>', lambda event: publish(BACKWARD))

    canvas = tk.Canvas(root, bg="white", width=200, height=150)
    label = tk.Label(canvas, text='', bg='red', font=('courier', 20, 'bold'), height=5, width=20)
    label.pack(expand=tk.YES, fill=tk.BOTH)
    canvas.pack()

    root.mainloop()
