from pathlib import Path
import stat

# Чтобы отформатировать время
import datetime


def permissions(path: Path) -> str:
    """
    Формируем строку прав доступа в нужном формате
    :param path: путь к файлу/каталогу
    :return:строка из 10 символов, права доступа
    """
    status = path.stat()
    # Формируем права владельца
    owner_permissions = (('r' if status.st_mode & stat.S_IRUSR else "-")+
                        ("w" if status.st_mode & stat.S_IWUSR else "-")+
                        ("x" if status.st_mode & stat.S_IXUSR else "-"))

    # Формируем права группы
    group_permissions = (('r' if status.st_mode & stat.S_IRGRP else "-")+
                        ("w" if status.st_mode & stat.S_IWGRP else "-")+
                        ("x" if status.st_mode & stat.S_IXGRP else "-"))

    # Формируем права остальные
    other_permissions = (('r' if status.st_mode & stat.S_IROTH else "-")+
                        ("w" if status.st_mode & stat.S_IWOTH else "-")+
                        ("x" if status.st_mode & stat.S_IXOTH else "-"))

    dir_or_file = "d" if path.is_dir() else "-"

    return dir_or_file + owner_permissions + group_permissions + other_permissions

def ls(path_of_curr_dir: Path, arguments: list) -> bool:
    """
    Осуществляет выполнение команды ls
    :param path_of_curr_dir: путь к текущему каталогу
    :param arguments: аргументы введенные с командой
    :return: True если выполнение бещ ошибок, иначе False
    """
    # Отвечает за путь введенный пользователем как аргумент
    arguments_path = "."
    if path.is_dir():
        print('lfe')
    # Отвечает за то, длинная форма вывода или нет
    l_form = 0
    # Смотрим на аргументы
    if len(arguments)>0:
        if arguments[0] == '-l':
            l_form = 1
            if len(arguments) >1:
                arguments_path = arguments[1]
            else:
                arguments_path = "."
        else:
            arguments_path = "."

    # Строим полный путь
    absolut_path = (path_of_curr_dir/arguments_path).resolve()

    # Проверяем существует ли такой путь
    if not absolut_path.exists():
        print(f"ls: cannot access '{arguments_path}': No such file or directory")

    # Если это директория
    if absolut_path.is_dir():
        try:
            if l_form:
                for element in sorted(absolut_path.iterdir()):
                    permission = permissions(element)
                    size = element.stat().st_size if element.is_file() else 4096
                    time_not_formated = element.stat().st_mtime
                    formated_time = datetime.datetime.fromtimestamp(time_not_formated).strftime("%Y %B %d %H:%M")
                    print(f"{permission} {size:6} {formated_time} {element.name}")
            else:
                for element in sorted(absolut_path.iterdir()):
                    print(element.name)

        except PermissionError:
            print(f"ls: cannot open directory '{absolut_path}': Permission denied")
            return False

    # Если это файл
    else:
        if l_form:
            permission = permissions(absolut_path)
            size = absolut_path.stat().st_size
            time_not_formated = absolut_path.stat().st_mtime
            formated_time = datetime.datetime.fromtimestamp(time_not_formated).strftime("%Y %B %d %H:%M")
            print(f"{permission} {size:6} {formated_time} {absolut_path.name}")
        else:
            print(absolut_path.name)
    return True


path = Path('/home/daria_nov/c_lab/main')
print(ls(path,['-l']))
