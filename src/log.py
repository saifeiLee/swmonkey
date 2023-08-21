import logging

def monkey_logger(log_file, log_level=logging.INFO):
    logger = logging.getLogger('monkey')
    logger.setLevel(log_level)
    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger

log_file = './out/monkey.log'
logger = monkey_logger(log_file)