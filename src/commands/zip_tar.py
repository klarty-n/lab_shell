from pathlib import Path
from src.errors import error
import shutil


def zip_tar(path_of_curr_dir: Path, arguments: list, extension: str) -> bool:
    """
    Осуществялет выполнение команды zip или tar, в зависимости от ввода / создание архива из каталога
    :param path_of_curr_dir: путь к текущему каталогу
    :param arguments: аргументы введенные с командой
    :param extension: тип расширения
    :return: True или False, в зависимости от успеха выполнения
    """
    if len(arguments) != 2:
        error(f"{extension}: missing operand")
        return False

    folder = arguments[0]
    archive = arguments[1]

    folder_path = (path_of_curr_dir / folder).resolve()
    archive_path = (path_of_curr_dir / archive).resolve()

    if not folder_path.exists():
        error(f"{folder}: No such file or directory")
        return False

    try:
        shutil.make_archive(archive_path,f"{extension}",folder_path)
        return True

    except Exception as e:
        error(f"Error during creating archive: {e}")
        return False
