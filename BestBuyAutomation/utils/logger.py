import logging
import os


class LogGen:

    @staticmethod
    def loggen(name=__name__):

        # Create logs folder if not exists
        if not os.path.exists("logs"):
            os.makedirs("logs")

        # Create named logger (IMPORTANT FIX)
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        # Prevent duplicate handlers
        if not logger.handlers:

            file_handler = logging.FileHandler("logs/automation.log")

            formatter = logging.Formatter(
                "%(asctime)s : %(levelname)s : %(name)s : %(message)s"
            )

            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger