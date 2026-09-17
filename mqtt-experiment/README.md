# MQTT experiment (companion to the TCP socket approach)

Same goal as `RoboServer.py`/`TestClient.py` in the parent repo — remotely triggering NAOqi robot actions over a network — but tried here with MQTT pub/sub (`paho-mqtt`) instead of raw TCP sockets.

## Files

- `MQTT_Connection.py` — connects to an MQTT broker (`127.0.0.1:1883` by default) and, on connect, opens an `ALMotion` proxy to the robot (`127.0.0.1:53922` — a local virtual robot) and runs a short head/body movement test, then speaks a completion message.
- `NAOQI_Commands.py` — the movement/speech helper functions (`move_head`, `rotate_body`, `move_body`, `say`, `list_joints`). Each one both calls the NAOqi motion proxy directly **and** publishes a status message to a matching MQTT topic (`robot/<name>/move/...`), so MQTT here is a status/telemetry channel rather than the actual control transport — the robot calls themselves still go straight through `ALProxy`.

## Status

Experimental / retired, like the rest of this repo. Left as-is for reference against the TCP socket version — worth comparing if picking remote NAO control back up, since neither approach here has an actual remote *listener* driving the robot from the MQTT side (the current code publishes telemetry but doesn't subscribe to commands).

## Note

`__pycache__/` and `.pyc` files from the original folder were left out — add a `.gitignore` with `__pycache__/` and `*.pyc` if the parent repo doesn't already have one.
