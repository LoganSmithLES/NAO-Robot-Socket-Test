import socket
import time
import logging

# === CONFIGURATION: Update these as needed ===
ROBOT_IP = "127.0.0.1"  # Change this to your robot's actual IP
ROBOT_PORT = 53922       # Change this to the robot's port
# ==============================================

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def send_command_to_robot(command):
    """ Sends a command to the NAO robot server. """
    max_retries = 5
    for attempt in range(max_retries):
        try:
            # Create a socket and connect to the robot
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)  # Set a 5-second timeout
            logging.info("Connecting to {}:{} (attempt {}/{})".format(ROBOT_IP, ROBOT_PORT, attempt + 1, max_retries))
            s.connect((ROBOT_IP, ROBOT_PORT))

            # Send the command as plain text
            logging.info("Sending command: {}".format(command))
            s.sendall(command.encode('utf-8'))

            # Receive the response
            data = s.recv(1024)
            logging.info("Response from robot server: {}".format(data.decode('utf-8')))
            s.close()
            return  # Exit after successful execution

        except socket.timeout:
            logging.warning("Connection timed out, retrying in {}s...".format(2 ** attempt))
        except socket.error as e:
            logging.warning("Connection failed: {}".format(e))
            logging.warning("Retrying in {}s...".format(2 ** attempt))
        finally:
            if 's' in locals():
                s.close()
        time.sleep(2 ** attempt)  # Exponential backoff

    logging.error("Failed to connect after {} attempts.".format(max_retries))

if __name__ == "__main__":
    start_time = time.time()
    send_command_to_robot("testFunc")  # Send command
    logging.info("Total communication time: {:.2f} seconds".format(time.time() - start_time))
