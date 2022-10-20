import os
import logging
import configparser

from annot8.settings.base import BASE_DIR

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

config_file = BASE_DIR / "mysql.cnf"
if config_file.is_file():
    config = configparser.ConfigParser()
    config.read(config_file)

    HOST = config["client"]["host"]
    PORT = config["client"]["port"]
    DB = config["client"]["database"]
    USER = config["client"]["user"]
    PW = config["client"]["password"]
else:
    logging.warning("No mysql config file was found. Settings will be read from environment variables")
    HOST = os.environ.get("MYSQL_HOST")
    PORT = os.environ.get("MYSQL_PORT", 3306)
    DB = os.environ.get("MYSQL_DATABASE")
    USER = os.environ.get("MYSQL_USER")
    PW = os.environ.get("MYSQL_PASSWORD")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
        'HOST': HOST,
        'NAME': DB,
        'USER': USER,
        'PASSWORD': PW,
        'PORT': PORT,
        'TEST': {
            "NAME": "annot8_tests"
        }
    }
}

