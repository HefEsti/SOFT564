# Import libraries
import json


class ConfigHandler():
    """
    The ConfigHandler module will retrieve all the configurations
    that were placed in the "mqtt.json" file.
    """

    def __init__(self):
        self.data = ""
        self.settings = {}
        self.read_json()

    def read_json(self):
        """
        This method will read all the configurations from the "mqtt.json"configuration files.
        The settings will be placed in a hash.
        """
        with open('mqtt.json') as data_mqtt:
            self.data = json.load(data_mqtt)

            self.settings["mqtt_broker"] = self.check_data('MQTT_BROKER') # broker address
            self.settings["mqtt_port"] = self.check_data('MQTT_PORT') # port number
            self.settings["default_log_mode"] = self.check_data('DEFAULT_LOG_MODE') # default logging mode
            self.settings["log_mode_topic"] = self.check_data('LOG_MODE_TOPIC') # topic to recieve mode changes
            self.settings["robot_info_topic"] = self.check_data('ROBOT_INFO_TOPIC') # topic to recieve robots location
            self.settings["robot_movement_topic"] = self.check_data('ROBOT_MOVEMENT_TOPIC')  # topic for robot movement

    def get_setting_by_key(self, key):
        """
        This method needs one argument:
            - key: the name of the hash containing the value of the setting.

        This method will return the setting that goes with the key that was made in method \"read_json(self)\".
        """
        return self.settings.get(key)

    def check_data(self, setting):
        """
        This method needs one argument:
            - setting: refers to the name of the attribute given in the json file.

        This method will return "False" if the setting doesn't exist in the files.
        """
        try:
            return self.data[setting]
        except:
            return False