#!/usr/bin/env python3

import argparse
import json
import logging
import sys

from common_constants import LOGGING_ARGS
from common_utils import is_python3, mqtt_broker_info
from constants import *
from mqtt_connection import MqttConnection

if is_python3():
    import tkinter as tk
else:
    import Tkinter as tk

HOSTNAME = "hostname"
PORT = "port"

# Execute on run

if __name__ == "__main__":
    # Publisher callbacks

    def on_publisher_connect(client, userdata, flags, rc):
        logging.info("[Publisher] Connected with result code: {0}".format(rc))


    def on_publisher_disconnect(client, userdata, rc):
        logging.info("[Publisher] Disconnected with result code: {0}".format(rc))


    def on_publisher_publish(client, userdata, mid):
        logging.info("[Publisher] Published value to {0} with message id {1}".format(COMMAND_TOPIC, mid))


    # Subscriber callbacks

    def on_subscriber_connect(client, userdata, flags, rc):
        logging.info("[Subscriber] {0} connecting to {1}:{2}".format("Success" if rc == 0 else "Failure",
                                                                     userdata[HOSTNAME],
                                                                     userdata[PORT]))
        client.subscribe(CONFIRM_TOPIC)


    def on_subscriber_disconnect(client, userdata, rc):
        logging.info("[Subscriber] Disconnected with result code: {0}".format(rc))


    def on_subscriber_subscribe(client, userdata, mid, granted_qos):
        logging.info("[Subscriber] Subscribed with message id: {0} QOS: {1}".format(mid, granted_qos))


    def on_subscriber_message(client, userdata, msg):
        # Decode json object payload
        json_val = json.loads(bytes.decode(msg.payload))
        print("[Subscriber] Topic {0} received {1}".format(msg.topic, json_val))
        global pub_direction, pub_speed, sub_direction, sub_speed
        sub_direction = json_val[DIRECTION]
        sub_speed = json_val[SPEED]
        update_display()


    # Parse CLI args

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mqtt", required=True, help="MQTT broker hostname")
    args = vars(parser.parse_args())

    # Setup logging

    logging.basicConfig(**LOGGING_ARGS)

    # Instantiate publisher and subscriber, start connecting asynchronously

    mqtt_pub = MqttConnection(*mqtt_broker_info(args["mqtt"]))
    mqtt_pub.client.on_connect = on_publisher_connect
    mqtt_pub.client.on_disconnect = on_publisher_disconnect
    mqtt_pub.client.on_publish = on_publisher_publish
    mqtt_pub.connect()

    hostname, port = mqtt_broker_info(args["mqtt"])
    mqtt_sub = MqttConnection(hostname, port, userdata={HOSTNAME: hostname, PORT: port})
    mqtt_sub.client.on_connect = on_subscriber_connect
    mqtt_sub.client.on_disconnect = on_subscriber_disconnect
    mqtt_sub.client.on_subscribe = on_subscriber_subscribe
    mqtt_sub.client.on_message = on_subscriber_message
    mqtt_sub.connect()


    # Set up interface callbacks

    def update_display():
        global pub_direction, pub_speed, sub_direction, sub_speed
        labels[DIRECTION]["text"] = "Direction: {0}".format(pub_direction)
        labels[SPEED]["text"] = "Speed: {0}".format(pub_speed)
        # Green = robot has verified commmand, Red = robot has not yet verified command (note: repetitions don't show)
        labels[DIRECTION]["bg"] = "green" if pub_direction == sub_direction else "red"
        labels[SPEED]["bg"] = "green" if pub_speed == sub_speed else "red"
        # Reloads all properties; in this case, it updates the color
        root.update()


    def publish_value():
        global pub_direction, pub_speed, sub_direction, sub_speed
        update_display()
        # Encode payload into json object
        json_val = json.dumps({DIRECTION: pub_direction, SPEED: pub_speed})
        result, mid = mqtt_pub.client.publish(COMMAND_TOPIC, payload=json_val.encode('utf-8'))


    def set_direction(cmd):
        global pub_direction
        pub_direction = cmd
        publish_value()


    def on_key(event):
        global pub_direction, pub_speed
        key_clicked = eval(repr(event.char))
        if key_clicked == "+" or key_clicked == "=":
            if pub_speed < 10:
                pub_speed += 1
                publish_value()
        elif key_clicked == "-" or key_clicked == "_":
            if pub_speed > 0:
                pub_speed -= 1
                publish_value()
        elif key_clicked == " ":
            pub_direction = STOP
            pub_speed = 0
            publish_value()
        elif key_clicked == "q":
            # Disconnect, kill the interface, then stop the program
            mqtt_pub.disconnect()
            mqtt_sub.disconnect()
            root.destroy()
            sys.exit()
        else:
            print("[Interface] Pressed {0}".format(key_clicked))


    def on_mouseclick(event):
        root.focus_set()
        print("[Interface] Clicked at {0},{1}".format(event.x, event.y))


    pub_direction = STOP
    pub_speed = 1

    sub_direction = STOP
    sub_speed = 1

    root = tk.Tk()
    root.title("Keyboard Controller (Bidirectional)")
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
    args = {"text": "", "bg": "green", "height": 2, "width": 20, "font": ('courier', 20, 'bold')}
    labels[DIRECTION] = tk.Label(canvas, args)
    labels[DIRECTION].pack(expand=tk.YES, fill=tk.BOTH)
    labels[SPEED] = tk.Label(canvas, args)
    labels[SPEED].pack(expand=tk.YES, fill=tk.BOTH)

    update_display()

    root.mainloop()
