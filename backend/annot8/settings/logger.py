import logging

from annot8.settings.base import DEBUG
from annot8.settings.base import BASE_DIR

LOGFILE = None
FMT = '%(levelname)s - [%(asctime)s] %(filename)s:%(lineno)d [%(funcName)s]: %(message)s'

if DEBUG:
    level = logging.DEBUG
else:
    level = logging.INFO

level = logging.INFO
logging.basicConfig(format=FMT, level=level, filename=LOGFILE, filemode="w")


logging.info("Running in {} mode".format("DEBUG" if DEBUG else "PRODUCTION"))
logging.info(f"{BASE_DIR=}")
