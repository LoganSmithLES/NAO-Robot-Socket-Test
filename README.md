Minimal TCP client/server test for triggering NAOqi robot actions remotely

RoboServer.py
the “robot server” that waits for incoming commands and, when asked, runs a demo robot action (wake up, speak, move, rest).

TestClient.py
the “test client” that connects to that server, sends the command (testFunc), and retries if connection fails.

THIS PROJECT IS RETIRED
