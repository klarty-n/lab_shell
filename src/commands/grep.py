import re
from pathlib import Path
from src.errors import error

def grep(path_of_curr_dir: Path, arguments: list) -> bool:
    """
    Осуществляет выполнение команды grep / поиск строк, соответсвующих шаблону
    :param path_of_curr_dir: путь к текущему каталогу
    :param arguments: аргументы введенные с командой
    :return: True или False, в зависимости от успеха выполнения
    """

    ignore = False
    if len(arguments) < 2:
        error("grep [OPTION]... PATTERNS [FILE]...")
        return False

    else:
        if arguments[0] or arguments[1] == '-r':
            recursive = True
            arguments = arguments[1:]

        elif arguments[0] or arguments[1] == '-i':
            # Игнорируем регистр при поиске по паттерну, если введен -i
            ignore = re.IGNORECASE  # type: ignore
            arguments = arguments[1:]

        else:
            recursive = False

    # Если в arguments ничего не осталось, когда оттуда убрали опции, то при вводе были указаны только -r/-i
    if not arguments:
        error("grep [OPTION]... PATTERNS [FILE]...")
        return False

    pattern = arguments[0]
    file_paths = [(path_of_curr_dir / file).resolve() for file in arguments[1:]]

    for path in file_paths:
        if path.is_dir():
            if recursive:
                # Если это папка и есть флаг -r
                # перебираем все файлы внутри нее и внутри подкаталогов, поиск будет в них
                search_files = [file for file in path.rglob("*") if file.is_file()]
            else:
                error(f"{path.name}: Is a directory")
                continue

        elif path.is_file():
            # Иначе поиск по файлу указанному
            search_files = [path]

        else:
            error(f"{path.name}: No such file or directory")
            continue

    # Флаг, показывает нашлось ли что-то
    found_smth = False

    # Поиск совпадений с паттерном по файлам
    for file in search_files:
        try:
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                # Номеруем строки в файле, начиная с 1
                for number_line, line in enumerate(f,1):
                    if re.search(pattern, line, ignore):
                        print(f"{file.name} line:{number_line:<8} {line}")
                        found_smth = True
        except Exception as e:
            error(f"{file.name}: {e}")

    return found_smth
