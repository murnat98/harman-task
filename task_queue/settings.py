import os


class Settings:
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
