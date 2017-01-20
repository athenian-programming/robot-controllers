# Robot Controllers

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


