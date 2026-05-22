import os
import configparser


class ConfigReader:

    config = configparser.ConfigParser()

    config_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "config",
        "config.properties"
    )

    config.read(config_path)

    @staticmethod
    def get_url():
        return ConfigReader.config.get("DEFAULT", "url")

    @staticmethod
    def get_browser():
        return ConfigReader.config.get("DEFAULT", "browser")

    @staticmethod
    def get_implicit_wait():
        return ConfigReader.config.get("DEFAULT", "implicit_wait")

    @staticmethod
    def get_explicit_wait():
        return ConfigReader.config.get("DEFAULT", "explicit_wait")