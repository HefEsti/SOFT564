# Import libraries
import json
import logging
import paho.mqtt.client as mqtt
from ConfigHandler import ConfigHandler


class PcCode:
    """
    The PcCode method is responsible for logging all incoming robot information and setting the Logging mode
    from the Android app.
    """

    def __init__(self):
        # Reading in data from the config file
        config_handler = ConfigHandler()
        self.broker = str(config_handler.get_setting_by_key("mqtt_broker"))
        self.broker_port= str(config_handler.get_setting_by_key("mqtt_port"))
        self.log_mode = int(config_handler.get_setting_by_key("default_log_mode"))
        self.log_mode_topic = str(config_handler.get_setting_by_key("log_mode_topic"))
        self.robot_info_topic = str(config_handler.get_setting_by_key("robot_info_topic"))
        self.robot_movement_topic = str(config_handler.get_setting_by_key("robot_movement_topic"))

        # Initialising Logging file
        logging.basicConfig(filename='app.log', level=logging.INFO)
        logging.info("Started Logging in mode %d", self.log_mode)

    def mqtt_connect(self):
        """
        This method will create the client for the computer and connect to the broker specified
        in the configuration files.
        """

        #Initializing client
        self.client = mqtt.Client("computer", True, None, mqtt.MQTTv31)

        # Bounding functions
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        #Establish connection
        try:
            self.client.connect(self.broker, self.broker_port)
            print ("trying")
        except Exception:
            print ("Connection can't be established with", self.broker, self.broker_port)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        """
        This method will be called when the client succesfully connected to the broker.
        After the connection, it will subscribe to the topics specified in the configuration files.
        """

        print ("connection done")

        self.client.subscribe(self.robot_info_topic, 1)
        self.client.subscribe(self.log_mode_topic, 1)
        self.client.subscribe(self.robot_movement_topic, 1)

    def on_message(self, client, userdata, message):
        """
        This method is called when the robot client recieves a message.
        If the method recieves a message from the robot on the topic specified in the config file under the
            - "ROBOT_INFO_TOPIC" it will call 'self.logging_robot_info()' to log the message
            - "LOG_MODE_TOPIC" it will call 'self.mode_selection()' to set the logging mode
            - "ROBOT_MOVEMENT_TOPIC" it will log the robots movement
        """

        #print (self.log_mode)
        self.payload = str(message.payload)
        #print (self.payload)
        if (message.topic == self.log_mode_topic):
            self.mode_selection(self.payload)
        elif (message.topic == self.robot_info_topic):
            self.logging_robot_info(self.payload)
        elif (message.topic == self.robot_movement_topic):
            logging.info("Robot %s", self.payload)

    def mode_selection (self, payload):
        """
        This method will set the logging mode according to the incoming instruction and logs the mode change.
            - payload "m1" - Mode 1: log Time and Location
            - payload "m2" - Mode 2: log Location only
            - payload "m3" - Mode 3: Log Time only
        If an instruction is the same as the current state, it will not do anything.
        """
        self.payload= payload
        if self.payload == "m1":
            if self.log_mode == 1:
                pass
            else:
                self.log_mode = 1
                logging.info("Mode changed to 1. Now logging both Location and Time.")
        elif self.payload == "m2":
            if self.log_mode == 2:
                pass
            else:
                self.log_mode = 2
                logging.info("Mode changed to 2. Now logging Location only.")
        elif self.payload == "m3":
            if self.log_mode == 3:
                pass
            else:
                self.log_mode = 3
                logging.info("Mode changed to 3. Now logging Time only.")

    def logging_robot_info (self, payload):
        """
        This method will log the incoming payload according to the Logging mode.
        """

        robot_data = json.loads(payload)
        if self.log_mode == 1:
            logging.info("Robot was in the %s at %s", robot_data['place'], robot_data['time'])
        elif self.log_mode == 2:
            logging.info("Robot was in the %s", robot_data['place'] )
        elif self.log_mode == 3:
            logging.info("Robot last communicated with PC at %s", robot_data['time'] )
        else:
            logging.info(payload)



def main():
    test = PcCode()
    test.mqtt_connect()
    while 1:
        pass


if __name__ == "__main__":
    main()
