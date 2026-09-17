import paho.mqtt.client as mqtt
import time
import sys
from naoqi import ALProxy
import NAOQI_Commands  # Import robot movement and speech commands

# Configuration settings
MQTT_BROKER = "127.0.0.1"  # MQTT broker IP address
MQTT_PORT = 1883           # Default port for MQTT
ROBOT_IP = "127.0.0.1"     # Robot's IP address
ROBOT_PORT = 53922         # Robot's NAOqi port
ROBOT_NAME = "virtual_robot"  # Name of the virtual robot

# Debugging function to print messages with timestamps
def debug_log(message):
    """
    Prints debug messages with timestamp for easy tracking.
    """
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    print("[DEBUG] {0}: {1}".format(timestamp, message))

# Create a proxy to connect to the robot's motion server
def get_robot_proxy():
    """
    Connects to the robot's motion proxy and returns the proxy object.
    Exits the program if the connection fails.
    """
    try:
        debug_log("Connecting to the robot's motion proxy at {0}:{1}".format(ROBOT_IP, ROBOT_PORT))
        motion_proxy = ALProxy("ALMotion", ROBOT_IP, ROBOT_PORT)
        debug_log("Connected to the robot's motion proxy successfully!")
        return motion_proxy
    except Exception as e:
        debug_log("Failed to connect to the robot's motion proxy: {0}".format(e))
        sys.exit(1)

# Callback function for successful MQTT connection
def on_connect(client, userdata, flags, rc):
    """
    Called when the MQTT client successfully connects to the broker.
    Starts the robot movement sequence if connected successfully.
    """
    if rc == 0:
        debug_log("Connected to MQTT broker successfully!")
        start_time = time.time()  # Record start time for movement test
        motion_proxy = get_robot_proxy()

        # Test robot movements
        run_robot_movements(client, motion_proxy)

        # End movement test and log the time taken
        end_time = time.time()
        debug_log("Movement Test Completed. Time taken: {0:.2f} seconds".format(end_time - start_time))

        # Send a speech command after the movements
        NAOQI_Commands.say(client, ROBOT_NAME, "Movement test complete!")

    else:
        debug_log("Failed to connect to MQTT broker. Return code: {0}".format(rc))

# Function to measure time taken to connect to the MQTT broker
def measure_mqtt_connection():
    """
    Measures the time it takes to connect to the MQTT broker.
    """
    start_time = time.time()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    end_time = time.time()
    debug_log("Connected to MQTT broker in {0:.2f} seconds".format(end_time - start_time))

# Function to initialize and configure the MQTT client
def initialize_mqtt_client():
    """
    Initializes and configures the MQTT client with necessary callbacks.
    """
    client = mqtt.Client()
    client.on_connect = on_connect
    return client

# Function to execute robot movements (head, body, etc.)
def run_robot_movements(client, motion_proxy):
    """
    Executes a series of robot movements and logs debug messages for each.
    """
    # Head movement tests
    NAOQI_Commands.move_head(client, ROBOT_NAME, "up", motion_proxy)
    time.sleep(2)
    NAOQI_Commands.move_head(client, ROBOT_NAME, "down", motion_proxy)
    time.sleep(2)

    # Body rotation tests
    NAOQI_Commands.rotate_body(client, ROBOT_NAME, "left", motion_proxy)
    time.sleep(2)
    NAOQI_Commands.rotate_body(client, ROBOT_NAME, "right", motion_proxy)
    time.sleep(2)

    # Body forward movement
    NAOQI_Commands.move_body(client, ROBOT_NAME, "forward", motion_proxy)
    time.sleep(3)

# Main program execution
if __name__ == "__main__":
    debug_log("Starting MQTT connection process...")

    # Initialize MQTT client
    client = initialize_mqtt_client()

    # Measure and log connection time to the MQTT broker
    measure_mqtt_connection()

    # Start MQTT client loop to maintain connection
    client.loop_start()

    # Keep the program running to maintain connection
    try:
        while True:
            time.sleep(1)  # Keeps the script alive
    except KeyboardInterrupt:
        debug_log("Disconnected from the MQTT broker.")
        client.loop_stop()  # Gracefully stop the MQTT loop
