import logging

def setup_logger():
    logger = logging.getLogger("my_logger")
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler("app.log", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

my_logger = setup_logger()