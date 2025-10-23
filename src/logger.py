import logging
logging.basicConfig(level=logging.INFO, filename="shell.log",filemode="w")

# Настройка логирования

def log_settings() -> None:
        logging.basicConfig(level=logging.INFO, filename="shell.log",
                    format= '%(asctime)s - %(message)s', filemode="w")
