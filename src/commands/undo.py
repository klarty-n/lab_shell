import shlex
from pathlib import Path
import os
import shutil
from src.errors import error

def undo_cp(path_of_curr_dir: Path, parsed: list) -> bool:
    """
    Отменяет команду cp
    :param path_of_curr_dir:  путь к текущему каталогу
    :param parsed: Запаршеная строка
    :return: True / False в зависимости от успеха выполнения
    """
    # Удаляем файл скопированный, тот который был указан последним элементом
    if len(parsed) < 3:
        error("undo: invalid cp command")
        return False

    target = parsed[-1]

    target_path = (path_of_curr_dir / target).resolve()

    if target_path.exists():
        if target_path.is_file():
            os.remove(target_path)
        elif target_path.is_dir():
            shutil.rmtree(target_path)
        print(f"undo: removed {target}")
        return True
    else:
        error(f"undo: {target} does not exist")
        return False

def undo_mv(path_of_curr_dir: Path, parsed: list) -> bool:
    """
    Отменяет команду mv
    :param path_of_curr_dir:  путь к текущему каталогу
    :param parsed: Запаршеная строка
    :return: True / False в зависимости от успеха выполнения
    """
    if len(parsed) < 3:
        error("undo: invalid mv command")
        return False

    all_removed = True

    sources = parsed[1:-1]
    target = parsed[-1]

    target_path = (path_of_curr_dir / target).resolve()

    # Если просто файл переименовали
    if len(sources) == 1 and not target_path.is_dir():
        source = sources[0]

        source_path = (path_of_curr_dir / source).resolve()
        target_path = (path_of_curr_dir / target).resolve()

        if target_path.exists():
            shutil.move(target_path, source_path)
            print(f"undo: renamed {target} back to {source}")
            return True
        else:
            error(f"undo: {target} does not exist")
            return False

    # Если переместили папку
    elif target_path.is_dir():

        all_removed = True

        for file in sources:
            file_path = (path_of_curr_dir / file).resolve()
            moved_to = target_path / file_path.name

            if moved_to.exists():
                shutil.move(moved_to, file_path)
                print(f"undo: moved {target} back to {file}")
                return True
            else:
                error(f"undo: {moved_to} does not exist")
                all_removed = False

    return all_removed


def undo_rm(path_of_curr_dir: Path, parsed: list) -> bool:
    """
    Отменяет команду rm
    :param path_of_curr_dir:  путь к текущему каталогу
    :param parsed: Запаршеная строка
    :return: True / False в зависимости от успеха выполнения
    """
    if len(parsed)<2:
        error("undo: invalid rm command")
        return False

    files = parsed[1:]
    trash_path = Path('src/commands/.trash').resolve()

    all_canceled = True
    for file in files:
        file_path = (path_of_curr_dir / file).resolve()
        file_trash = (trash_path / file).resolve()

        if file_trash.exists():
            # Обратно перемещаем
            shutil.move(file_trash, file_path)
            print(f"undo: {file} unremoved")
        else:
            error(f"undo: {file} not found in .trash")
            all_canceled = False

    return all_canceled



def undo(path_of_curr_dir: Path, arguments: list) -> bool:
    """
    Осуществляет выполнение команды grep / поиск строк, соответсвующих шаблону
    :param path_of_curr_dir: путь к текущему каталогу
    :param arguments: аргументы введенные с командой
    :return: True или False, в зависимости от успеха выполнения
    """

    # Если введено что-то кроме undo, лишние аргументы
    if arguments:
        error("undo: too many arguments")
        return False

    try:
        # Считываем команды из истории
        try:
            with open('.history', "r", encoding="utf-8") as f:
                lines = f.readlines()
                print(lines)
        except Exception as e:
            error(f"undo: mistake during unpacking file {e}")
            return False

        if not lines:
            error("undo: history is empty")
            return False

        last_command = lines[-2].strip()
        print(last_command)

        parsed = shlex.split(last_command)

        if not parsed:
            error("undo: no command")
            return False

        command = parsed[0]

        if command not in ["cp", "mv", "rm"]:
            error(f"undo: command '{command}' cannot be undone, can be undone only cp mv rm")
            return False

        if command == "mv":
            undo_mv(path_of_curr_dir, parsed)

        if command == "cp":
            undo_cp(path_of_curr_dir, parsed)

        if command == "rm":
            undo_rm(path_of_curr_dir, parsed)

    except Exception as e:
        error(f"undo: {e}")
        return False
    # Удаляем последнюю команду в истории
    new_lines = lines[:-1]
    # Перезаписываем историю без отмененной команды
    try:
        with open('.history', "w", encoding="utf-8") as f:
            f.writelines(new_lines)
    except Exception as e:
        error(f"undo: could not rewrite history: {e}")

    return True
