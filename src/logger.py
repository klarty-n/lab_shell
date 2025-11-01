import logging

logging.basicConfig(
    level=logging.INFO,
    filename="shell.log",
    filemode="a",
    datefmt="%Y-%m-%d %H:%M:%S",
    format="[%(asctime)s] %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger()

def log_command(command: str) -> None:
    """
    Логирует введенную команду
    :param command: вводимая команда
    :return: None
    """
    logger.info(command)

def log_error(message: str) -> None:
    """
    Логирует ошибки
    :param message: общение об ошибке
    :return:
    """
    logger.info(f"ERROR: {message}")
