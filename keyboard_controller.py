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

TOPIC = "/roborio/keyboard/command"
STOP = "STOP"

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
        print("Published value to {0} with message id {1}".format(TOPIC, mid))


    # Create MQTT connection
    mqtt_conn = MqttConnection(*mqtt_broker_info(args["mqtt"]))
    mqtt_conn.client.on_connect = on_connect
    mqtt_conn.client.on_disconnect = on_disconnect
    mqtt_conn.client.on_publish = on_publish
    mqtt_conn.connect()


    def update_display(direction, speed):
        labels["direction"]["text"] = "Direction: {0}".format(direction)
        labels["speed"]["text"] = "Speed: {0}".format(speed)


    def publish_value():
        global direction
        global speed
        update_display(direction, speed)
        # Encode payload into json object
        json_val = json.dumps({"command": direction, "speed": speed})
        result, mid = mqtt_conn.client.publish(TOPIC, payload=json_val.encode('utf-8'))


    def set_direction(cmd):
        global direction
        direction = cmd
        publish_value()

    def on_key(event):
        global direction
        global speed
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
    # For bind() details, see: http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
    # root.bind("<Button-1>", on_mouseclick)
    root.bind("<Key>", on_key)
    root.bind("<Left>", lambda event: set_direction("LEFT"))
    root.bind("<Right>", lambda event: set_direction("RIGHT"))
    root.bind("<Up>", lambda event: set_direction("FORWARD"))
    root.bind("<Down>", lambda event: set_direction("BACKWARD"))

    canvas = tk.Canvas(root, bg="white", width=200, height=150)
    labels = {}
    labels["direction"] = tk.Label(canvas, text='', bg='red', font=('courier', 20, 'bold'), height=2, width=20)
    labels["direction"].pack(expand=tk.YES, fill=tk.BOTH)
    labels["speed"] = tk.Label(canvas, text='', bg='red', font=('courier', 20, 'bold'), height=2, width=20)
    labels["speed"].pack(expand=tk.YES, fill=tk.BOTH)
    canvas.pack()

    update_display(direction, speed)

    root.mainloop()
