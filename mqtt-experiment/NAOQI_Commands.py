import paho.mqtt.client as mqtt
from naoqi import ALProxy

# Function to list available joints for debugging purposes
def list_joints(motion_proxy):
    """
    Lists the available joint names of the robot.
    Helps in debugging by displaying the joints.
    """
    try:
        joints = motion_proxy.getBodyNames("Body")  # Get body joints
        print("[DEBUG] Available joints:")
        for joint in joints:
            print(joint)
    except Exception as e:
        print("[ERROR] Failed to list joints: {0}".format(e))

# Function to move the robot's head
def move_head(client, robot_name, movement_command, motion_proxy):
    """
    Moves the robot's head (up or down) based on the provided command.
    """
    command_topic = "robot/{0}/move/head".format(robot_name)
    client.publish(command_topic, movement_command)

    try:
        if movement_command == "up":
            motion_proxy.setAngles("HeadPitch", -0.5, 0.2)  # Move head up
        elif movement_command == "down":
            motion_proxy.setAngles("HeadPitch", 0.5, 0.2)  # Move head down
        print("[DEBUG] Moving {0}: {1}".format(robot_name, movement_command))
    except Exception as e:
        print("[ERROR] Failed to move head: {0}".format(e))

# Function to rotate the robot's body (left or right)
def rotate_body(client, robot_name, rotation_command, motion_proxy):
    """
    Rotates the robot's body to the left or right based on the provided command.
    """
    command_topic = "robot/{0}/move/body/rotate".format(robot_name)
    client.publish(command_topic, rotation_command)

    try:
        # Debug: Print available joints
        list_joints(motion_proxy)

        if rotation_command == "left":
            motion_proxy.setAngles("HipRoll", 1.0, 0.2)  # Rotate left
        elif rotation_command == "right":
            motion_proxy.setAngles("HipRoll", -1.0, 0.2)  # Rotate right
        print("[DEBUG] Rotating {0}: {1}".format(robot_name, rotation_command))
    except Exception as e:
        print("[ERROR] Failed to rotate body: {0}".format(e))

# Function to move the robot's body (forward/backward)
def move_body(client, robot_name, movement_command, motion_proxy):
    """
    Moves the robot's body forward or backward based on the provided command.
    """
    command_topic = "robot/{0}/move/body".format(robot_name)
    client.publish(command_topic, movement_command)

    try:
        if movement_command == "forward":
            motion_proxy.moveTo(1.0, 0.0, 0.0)  # Move forward
        elif movement_command == "backward":
            motion_proxy.moveTo(-1.0, 0.0, 0.0)  # Move backward
        print("[DEBUG] Moving {0}: {1}".format(robot_name, movement_command))
    except Exception as e:
        print("[ERROR] Failed to move body: {0}".format(e))

# Function to make the robot speak a message
def say(client, robot_name, message):
    """
    Sends a speech command to the robot to speak the provided message.
    """
    command_topic = "robot/{0}/say".format(robot_name)
    client.publish(command_topic, message)
    print("[DEBUG] Sending speech command to {0}: {1}".format(robot_name, message))
