from pathlib import Path
import shutil
from src.errors import error


def mv(path_of_curr_dir: Path, arguments: list) -> bool:
    """
    Осуществялет выполнение команды mv / перемещает или переименовывает файл/каталог
    :param path_of_curr_dir: путь к текущему каталогу
    :param arguments: аргументы введенные с командой
    :return: True или False, в зависимости от успеха выполнения
    """

    # Флаг, указывает правильно ли обработались все аргументы
    all_elements_true = True

    if not arguments:
        error("mv: missing file operand")
        return False

    if len(arguments)<2:
        error(f"mv: missing destination file operand after {arguments}")
        return False

    else:

        moving_file = arguments[:-1]
        moving_file_path = [(path_of_curr_dir / relative_path).resolve() for relative_path in moving_file]

        moved_to = arguments[-1]
        moved_to_path = (path_of_curr_dir / moved_to).resolve()

    # Проверяем существование файлов
    for element in moving_file_path:
        if not element.exists():
            error(f"mv: cannot stat {element.name}: No such file or directory")
            all_elements_true = False
            moving_file_path = moving_file_path[1:]

    # Если дано 2 аргумента
    if len(moving_file_path) ==1:
        moving = moving_file_path[0]

        if not moving.exists():
            error(f"mv: cannot stat {arguments}: No such file or directory")
            return False

        # Если вторым аргументом название папки, то копируем в эту папку0
        if moved_to_path.is_dir() and moved_to_path.exists():
            # Перемещаем файл/каталог в папку
            final_copy_path = moved_to_path / moving.name

        else:
            final_copy_path = moved_to_path

        try:
            shutil.move(moving, final_copy_path)
            return True
        except Exception as e:
            error(f"mv: cannot  move '{moving.name}' to '{final_copy_path}': {e}")
            return False

    # Если дано больше 2 аргументов, последним должен быть указан каталог
    else:
        if not moved_to_path.is_dir():
            error(f"mv: target {moved_to_path.name}: Not a directory")
            return False

        if not moved_to_path.exists():
            error(f"mv: target {moved_to_path.name}: No such file or directory")
            return False

        for file in moving_file_path:
            final_copy_path = moved_to_path / file.name

            try:
                shutil.move(file, final_copy_path)

            except Exception as e:
                error(f"mv: cannot  move '{file.name}' to '{final_copy_path}': {e}")
                all_elements_true = False

    return all_elements_true
