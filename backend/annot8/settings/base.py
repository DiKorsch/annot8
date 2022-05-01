import os
import base64

from pathlib import Path

APP_NAME = "annot8"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SOCKETIO_PORT = os.environ.get("ANNOT8_SOCKETIO_PORT", 5000)

DEBUG = os.environ.get("ANNOT8_DEBUG", True)

if isinstance(DEBUG, str):
    if DEBUG.isdigit():
        DEBUG = bool(int(DEBUG))
    else:
        DEBUG = DEBUG == "True"

