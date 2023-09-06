import logging
import os
from logging import handlers

from com.loadconf import Config


def configure_logging(level, filename, when, backupCount, interval):
    if not os.path.exists(Config.log_path):
        os.makedirs(Config.log_path)
    orig_record_factory = logging.getLogRecordFactory()
    log_colors = {
        logging.DEBUG: "\033[1;34m",  # blue
        logging.INFO: "\033[1;32m",  # green
        logging.WARNING: "\033[1;35m",  # magenta
        logging.ERROR: "\033[1;41m",  # red
        logging.CRITICAL: "\033[1;41m",  # red reverted
    }

    def record_factory(*args, **kwargs):
        record = orig_record_factory(*args, **kwargs)
        record.levelname_c = "{}{}{}".format(log_colors[record.levelno], record.levelname, "\033[0m")
        return record

    logging.setLogRecordFactory(record_factory)
    format = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname_c)s: %(message)s')
    stderr_handler = logging.StreamHandler()
    stderr_handler.setLevel(level)
    stderr_handler.setFormatter(format)
    time_handler = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backupCount,
                                                     interval=interval, encoding='utf-8')
    time_handler.setLevel(level)
    time_handler.setFormatter(format)
    root_logger = logging.getLogger(filename)
    root_logger.setLevel(level)
    root_logger.addHandler(stderr_handler)
    root_logger.addHandler(time_handler)


logger = logging.getLogger((Config.log_path if Config.log_path.endswith('/') else Config.log_path + '/') + 'gitsync.log')
configure_logging(logging.DEBUG, (Config.log_path if Config.log_path.endswith('/') else Config.log_path + '/') + 'gitsync.log', 'midnight', 6,
                  1)
# S秒、M分、H小时、D天、W每星期(interval=0星期一)、midnight每天凌晨
