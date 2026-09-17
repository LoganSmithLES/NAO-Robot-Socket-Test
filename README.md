# NAO-Robot-Socket-Test

Undergraduate experiments in remotely triggering NAOqi robot actions (wake up, speak, move, rest, head/body movement) over a network, rather than running the control code directly on the robot. Two different transports were tried; neither is known to be the "final" or more current version — they're kept side by side as separate attempts at the same problem.

**THIS PROJECT IS RETIRED**

## Approaches

### TCP sockets — `RoboServer.py` / `TestClient.py`

The original approach: a minimal TCP client/server pair.

- `RoboServer.py` — the "robot server" that waits for incoming commands and, when asked, runs a demo robot action.
- `TestClient.py` — the "test client" that connects to that server, sends a command, and retries on connection failure.

### MQTT — `mqtt-experiment/`

A pub/sub alternative to the raw TCP approach, using `paho-mqtt` against a local broker (`127.0.0.1:1883`) alongside a direct `ALMotion` proxy connection to a virtual robot (`127.0.0.1:53922`).

- `mqtt-experiment/MQTT_Connection.py` — connects to the MQTT broker and the robot's motion proxy, then runs a short head/body movement test on connect.
- `mqtt-experiment/NAOQI_Commands.py` — movement/speech helper functions (`move_head`, `rotate_body`, `move_body`, `say`). Each one calls the NAOqi motion proxy directly *and* publishes a status message to a matching MQTT topic (`robot/<name>/move/...`) — so in this version MQTT is a telemetry/status channel, not the actual control transport; nothing subscribes to MQTT to drive the robot from that side.

See `mqtt-experiment/README.md` for more detail on that piece.

## Status

Retired / exploratory. Both approaches stop short of a real remote-control loop — the TCP version is a single fire-and-retry command, and the MQTT version doesn't yet have anything consuming commands over MQTT. Useful as reference if remote NAO control is picked back up, to compare transports rather than starting from scratch.
