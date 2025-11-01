from pathlib import Path
from src.errors import error
import shutil


def unzip_untar(path_of_curr_dir: Path, arguments: list, extension: str) -> bool:
    """
    Осуществялет выполнение команды unzip или untar/ распаковка архива
    При распаковке пустого архива не произойдет,
    так как в нем нет файлов для извлечения
    :param path_of_curr_dir: путь к текущему каталогу
    :param arguments: аргументы введенные с командой
     :param extension: тип расширения
    :return: True или False, в зависимости от успеха выполнения
    """
    if not arguments:
        error(f"un{extension}: missing operand")
        return False

    if len(arguments) >2:
        error(f"un{extension}: too much operand")
        return False

    archive = arguments[0]

    archive_path = (path_of_curr_dir / archive).resolve()

    if not archive_path.exists():
        error(f"{archive}: No such file or directory")
        return False

    try:
        shutil.unpack_archive(archive_path, path_of_curr_dir ,f"{extension}")
        return True

    except Exception as e:
        error(f"Error during unpacking archive: {e}")
        return False
