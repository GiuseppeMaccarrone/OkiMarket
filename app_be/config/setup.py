from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()


class Configuration(BaseSettings):

    app_name: str = os.getenv("APP_NAME", "prototype-app")

    # LOGGING
    log_level: str = "DEBUG" if os.getenv('LOG_LEVEL') == "DEBUG" else "INFO"
    log_dir: str = "log/"
    log_file: str = f"{log_dir}{app_name}.log"



config = Configuration()