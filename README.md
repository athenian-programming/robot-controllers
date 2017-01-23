# Robot Controllers

Modules in this package reference modules in the 
*../common-robotics* and *../color-tracking* packages.
Specify these dependencies in PyCharm by first clicking on 
Preferences-->Project:robot-controllers-->Project Structure.
Then click on `+Add Content Root` 
and add *../common-robotics* and *../color-tracking*.


## Package Dependencies

Install the following Python packages: 

* [gRPC](http://www.grpc.io/docs/guides/index.html) 
as described [here](http://www.athenian-robotics.org/grpc/)

* [OpenCV](http://opencv.org) 
as described [here](http://www.athenian-robotics.org/opencv/)

* [imutils](https://github.com/jrosebr1/imutils)
as described [here](http://www.athenian-robotics.org/imutils/)

* [MQTT](http://mqtt.org) client 
as describer [here](http://www.athenian-robotics.org/mqtt-client/)

## Keyboard Controller

keyboard_controller.py is used to drive a robot via keystrokes. 


### Usage 

```bash
$ ./keyboard_controller.py 
```

### CLI Options

| Option         | Description                                        | Default |
|:---------------|----------------------------------------------------|---------|
| -m, --mqtt     | MQTT broker hostname                               |         |
| -h, --help     | Summary of options                                 |         |


### Keystrokes

| Keystroke   | Action                                             |
|:-----------:|----------------------------------------------------|
| Up-Arrow    | Move robot forward                                 |
| Down-Arrow  | Move robot backward                                |
| Left-Arrow  | Move robot left                                    |
| Right-Arrow | Move robot right                                   |
| +           | Increase speed 1 unit                              |
| -           | Decrease speed 1 unit                              |
| space       | Sets speed to 0                                    |
| q           | Quit                                               |

## Camera Controller

camera_controller.py requires python2 because of OpenCV.

### CLI Options

| Option         | Description                                        | Default |
|:---------------|----------------------------------------------------|---------|
| -g, --grpc     | gRPC server hostname                               |         |
| -m, --mqtt     | MQTT broker hostname                               |         |
| -h, --help     | Summary of options                                 |         |




## Broker Listener

broker_listener.py is used to view all messages publised to broker. 

### Usage 

```bash
$ ./broker_listener.py 
```

### CLI Options

| Option         | Description                                        | Default |
|:---------------|----------------------------------------------------|---------|
| -m, --mqtt     | MQTT broker hostname                               |         |
| -h, --help     | Summary of options                                 |         |


