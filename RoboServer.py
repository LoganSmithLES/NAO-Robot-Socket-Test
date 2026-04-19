import sys
import time
import socket
import threading
import logging
from naoqi import ALProxy  # Import NAOqi API for robot control

# === CONFIGURATION: Update these as needed ===
ROBOT_IP = "127.0.0.1"  # Change this to your robot's actual IP
ROBOT_PORT = 53922      # Change this to the robot's port (53922 as per Choregraphe)
# ==============================================

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def testFunc():
    """Executes a test function on the NAO robot."""
    try:
        start_time = time.time()
        logging.info("Running testFunc()...")

        # Initialize NAOqi Proxies for speech and movement
        logging.info("Connecting to NAOqi at {}:{}...".format(ROBOT_IP, ROBOT_PORT))
        tts = ALProxy("ALTextToSpeech", ROBOT_IP, ROBOT_PORT)
        motion = ALProxy("ALMotion", ROBOT_IP, ROBOT_PORT)

        # Wake up the robot
        logging.info("Waking up robot...")
        motion.wakeUp()

        # Make the robot speak
        logging.info("Speaking: 'Function Test Complete'")
        tts.say("Function Test Complete")

        # Move the robot forward by 0.5 meters
        logging.info("Moving forward 0.5 meters...")
        motion.moveTo(0.5, 0, 0)

        # Relax the robot joints
        logging.info("Relaxing joints...")
        motion.rest()

        end_time = time.time()
        logging.info("testFunc completed in {:.2f} seconds".format(end_time - start_time))

        return "testFunc executed successfully!"

    except Exception as e:
        logging.error("Error in testFunc: {}".format(e))
        return "Error in testFunc"

def handle_client(client_socket, addr):
    """Handles a client connection."""
    try:
        logging.info("Connection received from: {}".format(addr))
        command = client_socket.recv(1024).decode('utf-8')
        logging.info("Received command: {}".format(command))

        if command == "testFunc":
            response = testFunc()
        else:
            response = "Unknown command"

        client_socket.sendall(response.encode('utf-8'))
        logging.info("Response sent.")

    except Exception as e:
        logging.error("Error handling client: {}".format(e))
    finally:
        client_socket.close()
        logging.info("Connection closed.")

def start_server():
    """Starts a socket server to listen for commands."""
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ROBOT_IP, ROBOT_PORT))
        server_socket.listen(5)
        logging.info("Listening on {}:{}...".format(ROBOT_IP, ROBOT_PORT))

        while True:
            client_socket, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.start()

    except Exception as e:
        logging.error("Server Error: {}".format(e))
    finally:
        server_socket.close()
        logging.info("Server shut down.")

if __name__ == "__main__":
    start_server()
