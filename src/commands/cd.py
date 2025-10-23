from pathlib import Path

def cd(path_of_curr_dir: Path, arguments: list) -> Path|bool:
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

    if not new_path.exists():
        print(f"cd: {arguments[0]} no such file or directory")
        return False

    if not new_path.is_dir():
        print(f"cd:{arguments[0]} not a directory")
        return False

    return new_path

path = Path('/home/daria_nov')
print(cd(path,['~']))
