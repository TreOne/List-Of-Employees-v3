import configparser
from utility.resource_path import resource_path


class Config:
    """
    Класс для считывания и записи настроек из конфигурационного файла.
    """

    def __init__(self):
        self.filename = resource_path('resources/settings.ini')

    def get_config(self):
        """
        Returns the config object
        """
        config = configparser.ConfigParser()
        config.read(self.filename)
        return config

    def get_setting(self, section, setting):
        """
        Print out a setting
        """
        config = self.get_config()
        value = config.get(section, setting)
        return value

    def update_setting(self, section, setting, value):
        """
        Update a setting
        """
        config = self.get_config()
        config.set(section, setting, value)
        with open(self.filename, "w") as config_file:
            config.write(config_file)
