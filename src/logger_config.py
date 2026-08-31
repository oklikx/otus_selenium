import logging


def setup_logger(name="AutomationFramework"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] (%(name)s) %(message)s')

        # 1. Запись в файл
        file_handler = logging.FileHandler(
            'automation_suite.log', encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 2. Запись в консоль
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
