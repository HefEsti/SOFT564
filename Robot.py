# Import libraries
import json
import random
import paho.mqtt.client as mqtt
from time import sleep
from random import randint
from datetime import datetime

class RobotCode:
    """
    The RobotCode module will imitate the code that would run on a buggy.
    It will create a connection with the broker, subscribe to the given topics
    so it can send its location and time of message to the PC.
    It also recieves movement instructions from the Android app and after "completing the movement"
    sends a message to the pc of the finished movement.
    """

    def __init__(self):
        self.broker_ip = "broker.hivemq.com"
        self.broker_port=1883
        self.robot_instruction_topic ="robot/instruction"
        self.robot_info_topic= "robot/info"
        self.robot_movement_topic = "robot/movement"

    def sending(self):
        """
        This method simulates how a robot would pass sensors while moving around in a space.
        It takes a random room name and send a signal after a random interval (between 5-10 seconds) and sends
        a json file with those information on the "robot/info" topic.
        """

        sleep(randint(5, 10))
        # Selecting random room
        placeOptions = ["Livingroom", "Bathroom", "Bedroom", "Kitchen", "Office", "Garden"]
        robot_location = random.choice(placeOptions)
        # Getting time
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        brokers_out = {"place": robot_location,
                       "time": current_time,
                       }
        data_out = json.dumps(brokers_out)

        print ("I'm in the " + robot_location)
        self.client.publish("robot/info", data_out)

    def MQTTconnect(self):
        """
        This method will create the client for the robot and connect to the broker specified
        in the _init_ function.
        """
        self.client = mqtt.Client("robot", True, None, mqtt.MQTTv31)

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        try:
            # Establish connection
            self.client.connect(self.broker_ip, self.broker_port)
            print ("Trying to establish connection with broker")
        except Exception:
            print ("Connection can't be established with broker")
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        """
        This method will be called when the client successfully connected to the broker.
        After the connection, it will subscribe to the topics specified in the _init_ function.
        """
        print ("Connection to broker is done")
        self.client.subscribe(self.robot_instruction_topic, 1)
        self.client.publish(self.robot_info_topic, "Robot connected to PC")

    def on_message(self, client, userdata, message):
        """
        This method is called when the robot client recieves a message.
        If the message topic is the same as the one specified in  'self.robot_instruction_topic' the payload
        will contain movement instructions. Depending on the instruction the imaginary robot will move
        to the specified direction and publish a message on the topic specified in 'self.robot_movement_topic'
        to let the pc know it moved.

        """

        self.payload = str(message.payload)
        if (message.topic == self.robot_instruction_topic):
            out_payload = ("moved " + self.payload)

            if self.payload == "forward":
                print ("I moved forward")
                self.client.publish(self.robot_movement_topic, out_payload)
            elif self.payload == "left":
                print ("I turned left")
                self.client.publish(self.robot_movement_topic, out_payload)
            elif self.payload == "right":
                print ("I turned right")
                self.client.publish(self.robot_movement_topic, out_payload)
            elif self.payload == "back":
                print ("I moved backwards")
                self.client.publish(self.robot_movement_topic, out_payload)
            else:
                print ("Unrecognised command. I didn't move")
                self.client.publish(self.robot_movement_topic, "recieved unrecognised command from user and didn't move")

    def on_disconnect(self, userdata, rc):
        """
        This method is called when the robot client is disconnected from the broker.
        This method attempts to reconnect.
        """
        print("I'm disconnected from PC")
        # Attempt to reconnect
        self.MQTTconnect()




def main():
    run = RobotCode()
    run.MQTTconnect()

    while 1:
        run.sending()


if __name__ == "__main__":
    main()
