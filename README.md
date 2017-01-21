# Robot Controllers

This package requires ../common_robotics_python and ../opencv_object_tracking to 
be added to the PYTHONPATH. 

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


