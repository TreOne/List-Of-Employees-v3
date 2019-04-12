import configparser
from utility.resource_path import resource_path


class Settings:
    """
    Класс для считывания и записи настроек из конфигурационного файла.
    """

    def __init__(self):
        self.filename = resource_path('resources/settings.ini')
        self.config = configparser.ConfigParser()
        self.config.read(self.filename)

    def get(self, section, setting):
        value = self.config.get(section, setting)
        return value

    def set(self, section, setting, value):
        self.config.set(section, setting, value)
        with open(self.filename, "w") as config_file:
            self.config.write(config_file)
