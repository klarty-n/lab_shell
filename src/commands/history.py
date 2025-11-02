from src.errors import error
from pathlib import Path

history_path = Path('src/commands/.history').resolve()

def add_command(command: str):
    """
    Добавляет команду в файл, контролируем, что в файле не больше 10 команд сохраняется
    :param command: введенная команда
    """
    try:
        with open(history_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            # Храним только 10 команд, первую команду удаляем, если команд стало больше 10
            if len(lines)>=10:
                lines = lines[1:]

    except Exception as e:
        error(f"history: mistake during unpacking file {e}")
        lines = []

    # Перезаписываем файл, без верхней команды
    with open(history_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    # Записываем новую введенную команду
    try:
        with open(history_path, "a", encoding="utf-8") as f:
            f.write(f"{command}\n")
    except Exception as e:
        error(f"can`t add command to .history: {e}")

def history(arguments: list) -> bool:
    """
    Осуществляет выполнение команды history / выводит последние n команд
    :param arguments: аргументы введенные с командой
    :return: True или False
    """

    # Выводим 10 команд, если не указано сколько
    if not arguments:
        n = 10
    elif len(arguments)>1:
        error("history: too many arguments")
        return False
    else:
        try:
            n = int(arguments[0])
        except ValueError:
            error("history: Enter a number")
            return False

    try:
        with open(history_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            # Пустые строки не выводим
            lines = [line for line in lines if line.strip()]

            # В писке будут лежать последние n команд
            lines = lines[-n:]

            for number_line, line in enumerate(lines, start=1):
                print(f"command: {number_line:<10} {line}")

    except Exception as e:
        error(f"history: {e}")
        return False

    return True
