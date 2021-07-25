import logging.config
import pathlib


PATH_LOG_CONF = str(pathlib.Path(
    __file__).resolve().parent / "log.conf")

logging.config.fileConfig(PATH_LOG_CONF)
