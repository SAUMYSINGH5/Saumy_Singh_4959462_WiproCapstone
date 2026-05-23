import configparser
import os

# Resolve absolute path regardless of where behave is invoked from
_config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config", "config.ini")

config = configparser.RawConfigParser()
files_read = config.read(_config_path)

if not files_read:
    raise FileNotFoundError(f"config.ini not found at: {os.path.abspath(_config_path)}")


class ReadConfig:

    @staticmethod
    def get_application_url():
        return config.get("common info", "base_url")

    @staticmethod
    def get_browser():
        return config.get("common info", "browser")