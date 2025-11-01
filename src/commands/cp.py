import shutil
from pathlib import Path
from src.errors import error

def cp(path_of_curr_dir: Path, arguments: list) -> bool:
    """
    Осуществляет выполнение команды cp / копирование каталога (также рекурсивно) или файлы
    :param path_of_curr_dir: путь к текущему каталогу
    :param arguments: аргументы введенные с командой
    :return:True или False
    """

    # Флаг, показывает скопировались ли все элементы
    all_elements_copied = True

    if not arguments:
        error("cp: missing file operand")
        return False

    else:
        if arguments[0] == '-r':
            recursive = True
            arguments = arguments[1:]
            if len (arguments)<2:
                error("cp: missing file operand")
                return False
        else:
            recursive = False
    # Исходный файл
    source_file = arguments[:-1]
    source_path = [(path_of_curr_dir / relative_path).resolve() for relative_path in source_file]

    # Целевой файл
    target_file = arguments[-1]
    target_path = (path_of_curr_dir / target_file).resolve()

    for element in source_path:
        if not element.exists():
            error(f"cp: cannot stat {element.name}: No such file or directory")
            all_elements_copied = False
            source_path = source_path[1:]


    # Если два файла / каталога
    if len(source_path)==1:
        source = source_path[0]

        if source.is_dir():
            if not recursive:
                error(f"cp: -r not specified; omitting directory {source.name}")
                return False

            else:
                # Если целевой каталог существует, то копируем исходный в него
                if target_path.is_dir() and target_path.exists():
                    # Путь, куда копируем исходный
                    copy_path = target_path / source.name

                # Если целевой каталог не существует, то просто создаем новый каталог
                else:
                    copy_path = target_path

                try:
                    shutil.copytree(source, copy_path)
                    return True
                except Exception as e:
                    error(f"cp: cannot copy '{source.name}' to '{copy_path.name}': {e}")
                    return False

        else:
            if target_path.is_dir():
                copy_path = target_path / source.name
            else:
                copy_path = target_path


            try:
                shutil.copy2(source, copy_path)
            except Exception as e:
                error(f"cp: cannot copy '{source.name}' to '{copy_path.name}': {e}")
                return False

    # Если больше 2, копирование возможно только если последним стоит каталог
    else:
        if not target_path.is_dir():
            error(f"cp: target {target_path.name}: No such file or directory")
            return False

        if not target_path.exists():
            error(f"cp: target {target_path.name}: No such file or directory")
            return False

        for source in source_path:
            if source.is_dir():
                if not recursive:
                    error(f"cp: -r not specified; omitting directory {source.name}")
                    all_elements_copied = False
                    continue

                else:
                    copy_path = target_path / source.name
                    try:
                        shutil.copytree(source, copy_path)
                    except Exception as e:
                        error(f"cp: cannot copy directory '{source.name}': {e}")
                        all_elements_copied = False
                        continue

            else:
                copy_path = target_path / source.name
                try:
                    shutil.copy2(source, copy_path)
                except Exception as e:
                    error(f"cp: cannot copy directory '{source.name}': {e}")
                    all_elements_copied = False

    return all_elements_copied
