import logging


def setup_logger(log_file: str = "bot.log") -> logging.Logger:
    """
    Настраивает и возвращает объект логгера.
    :param log_file: str - Имя файла для записи логов 
    (по умолчанию "bot.log");
    :return: logging.Logger - Настроенный объект логгера.
    """
    logger = logging.getLogger("GeelyBot")

    # Проверка, если уже добавлены обработчики
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)

        # Формат для логов
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # Логирование в файл
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Логирование в консоль
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger