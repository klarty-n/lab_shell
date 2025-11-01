from src.logger import log_error

def error(error_msg: str) -> None:
    print(error_msg)
    log_error(error_msg)
