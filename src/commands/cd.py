from pathlib import Path
from src.errors import error

def cd(path_of_curr_dir: Path, arguments: list) -> Path|None:
    """
    Осуществляет выполнение команды cd
    :param path_of_curr_dir: путь к текущему каталогу
    :param arguments: аргументы введенные с командой
    :return: Новый путь если выполнение без ошибок, иначе None
    """
    if not arguments or arguments[0] in ("","~"):
        # Попадаем в домашнюю директорию
        new_path = Path.home()

    else:
        relative_path = arguments[0]
        # Формируем абсолютный путь к новому файлу
        new_path = (path_of_curr_dir / relative_path).resolve()

    if not new_path.is_dir():
        error(f"cd:{arguments[0]} not a directory")
        return None

    if not new_path.exists():
        error(f"cd: {arguments[0]} no such file or directory")
        return None

    return new_path
