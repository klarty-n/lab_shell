import shutil
from pathlib import Path
from src.errors import error

def add_trash(element: Path):
    """
    Перемещаем в trash файл или каталог
    :param element: путь к файлу/каталогу
    """
    trash_path = Path('src/commands/.trash').resolve()
    target = trash_path / element.name

    shutil.move(element, target)

def rm(path_of_curr_dir: Path, arguments: list) -> bool:
    """
    Осуществляет выполнение команды cp / копирование каталога (также рекурсивно)
    :param path_of_curr_dir: путь к текущему каталогу
    :param arguments: аргументы введенные с командой
    :return: True или False
    """

    # Флаг, показывает скопировались ли все элементы
    all_elements_removed = True

    if not arguments:
        error("rm: missing operand")
        return False

    else:
        if arguments[0] == '-r':
            recursive = True
            arguments = arguments[1:]
            if not arguments:
                error("rm: missing file operand")
                return False
        else:
            recursive = False

    # Формируем абсолютный путь до удаляемых файлов/каталогов
    deleting_element_path = [(path_of_curr_dir / relative_path).resolve() for relative_path in arguments]

    # Проходимся по каждому введенному файлу/каталогу
    for element in deleting_element_path:
        # Если такого не существует, выводим ошибку и переходим к следующему
        if not element.exists():
            error(f"rm: cannot remove {element.name}: No such file or directory")
            all_elements_removed = False
            continue

        # Вывод ошибки, при попытке удалить родительский каталог или корневой
        if element == Path("/").resolve() or str(element)[-2:] == "..":
            error("rm: dangerous operation — root or parent directory deletion blocked")
            continue

        try:
            if element.is_dir():
                if not recursive:
                    error(f"rm: cannot remove '{element.name}': Is a directory")
                    all_elements_removed = False
                    continue

                else:
                    # При удалении каталога просим подтверждение
                    confirmation = input(f"Remove directory '{element.name}' and all contents? (y/n): ").lower()
                    if confirmation != "y":
                        error("Cancelled")
                        all_elements_removed = False
                        continue

                    add_trash(element)

            else:
                add_trash(element)
            return True

        except Exception as e:
            error(f"rm: error: {e}")
            return False

    return all_elements_removed
