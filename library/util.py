import logging
import os
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

SENTINEL = object()



class Utils:

    @staticmethod
    def set_env_config(filepath: str = ".local.env"):
        path = Path(filepath)
        if not path.is_file():
            raise FileNotFoundError(f"Config file {filepath} not found")
        load_dotenv(path)
        logging.debug(f"envs are: {os.environ.items()}")

    @staticmethod
    def get_env_config():
        return {
            "base_url": os.getenv("BASE_URL"),
            "mockserver_url": os.getenv("MOCKSERVER_URL"),
            "env_name": os.getenv("ENV_NAME", "local")
        }
