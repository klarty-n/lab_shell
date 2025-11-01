from pathlib import Path
import stat
import datetime
from src.errors import error

def time_formater(path:Path) -> str:
    """
    Форматирует время в нужный вид
    :param path: путь к файлу, время изменения которого отслеживается
    :return: отформатированное время
    """
    time_not_formated = path.stat().st_mtime
    formated_time = datetime.datetime.fromtimestamp(time_not_formated).strftime("%Y %B %d %H:%M")
    return formated_time

def get_permissions(path: Path) -> str:
    """
    Получаем строку прав доступа
    :param path: путь к каталогу/файлу
    :return: строка из 10 символов, права доступа / False
    """
    # Получаем права в цифровом виде
    permissions = path.stat().st_mode
    # Преобразуем права в нужный вид
    formated_permissions = stat.filemode(permissions)
    return formated_permissions

def detailed_list(element: Path) -> str:
    """
    Реализация аргумента -l, подробного вывода
    :param element: путь к файлу/каталогу
    :return: строка, подробный вывод
    """
    permissions = get_permissions(element)
    size = element.stat().st_size if element.is_file() else 4096
    time = time_formater(element)
    return f"{permissions} {size:6} {time} {element.name}"


def ls(path_of_curr_dir: Path, arguments: list) -> bool:
    """
    Осуществляет выполнение команды ls
    :param path_of_curr_dir: путь к текущему каталогу
    :param arguments: аргументы введенные с командой
    :return: True если выполнение бещ ошибок, иначе False
    """
    arguments_path = "."

    # Отвечает за то, подробный вывод или нет
    detailed_form = False

    # Работаем с аргументами
    if len(arguments)>0:
        if arguments[0] == '-l':
            detailed_form = True
            if len(arguments) >1:
                arguments_path = arguments[1]
            else:
                arguments_path = "."
        else:
            arguments_path = "."

    # Строим полный путь
    absolut_path = (path_of_curr_dir/arguments_path).resolve()

    if not absolut_path.exists():
        error(f"ls: cannot access '{arguments_path}': No such file or directory")

    # Если это директория
    if absolut_path.is_dir():
        try:
            if detailed_form:
                for element in sorted(absolut_path.iterdir()):
                    print(detailed_list(element))
            else:
                for element in sorted(absolut_path.iterdir()):
                    print(element.name)

        except PermissionError:
            error(f"ls: cannot open directory '{absolut_path}': Permission denied")
            return False

    # Если это файл
    else:
        if detailed_form:
            print(detailed_list(absolut_path))
        else:
            print(absolut_path.name)
    return True
