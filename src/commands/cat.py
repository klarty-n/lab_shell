from pathlib import Path
from src.errors import error

def cat(path_of_curr_dir: Path, arguments: list) -> bool:
    """
    Осуществялет выполнение команды cat / выводит содержимое файла
    :param path_of_curr_dir: путь к текущему каталогу
    :param arguments: аргументы введенные с командой
    :return: True или False, в зависимости от успеха выполнения
    """
    # Флаг (вывелись ли все файлы успешно)
    all_files_true = True

    if arguments:
        for element in arguments:
            file_path = (path_of_curr_dir / element).resolve()

            if not file_path.exists():
                error(f"cat: {arguments}: No such file or directory")
                all_files_true = False
                continue

            if file_path.is_dir():
                error(f"cat: {arguments}: is a directory")
                all_files_true = False
                continue

            try:
                with open(file_path,"r", encoding="utf-8") as file:
                    print(file.read(),end ="")

            except Exception as e:
                error(f"cat:{element}: {e}")
                all_files_true = False

    else:
        error("cat: you did not enter filename")
        return False

    return all_files_true
