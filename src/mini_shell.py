from pathlib import Path
import shlex
from src.logger import log_error, log_command
from src.commands.ls import ls
from src.commands.cd import cd
from src.commands.cat import cat
from src.commands.cp import cp
from src.commands.mv import mv
from src.commands.rm import rm
from src.commands.zip_tar import zip_tar
from src.commands.unzip_untar import unzip_untar
from src.commands.grep import grep
from src.commands.undo import undo
from src.commands.history import history, add_command


class mini_shell:

    def __init__(self):
        # Путь к текущей директории
        self.current_dir = Path.cwd()

    def run(self):
        """
        Запускает оболочку
        :return
        """
        print("Для выхода ведите exit (－_－) zzZ")

        while True:
            try:
                enter_command = input(f"{self.current_dir}$ ")
                if "exit" in enter_command:
                    print("(－_－) zzZ")
                    break
                if not enter_command:
                    continue

                add_command(enter_command)
                log_command(enter_command)

                try:
                    arguments = shlex.split(enter_command)
                except Exception as e:
                    log_error(f"Mistake during parsing: {e}")
                    continue

                command = arguments[0]

                if command == "ls":
                    ls(self.current_dir, arguments[1:])

                elif command == "cat":
                    cat(self.current_dir, arguments[1:])

                elif command == "cp":
                    cp(self.current_dir, arguments[1:])

                elif command == "mv":
                    mv(self.current_dir, arguments[1:])

                elif command == "rm":
                    rm(self.current_dir, arguments[1:])

                elif command == "zip":
                    zip_tar(self.current_dir, arguments[1:], "zip")

                elif command == "unzip":
                    unzip_untar(self.current_dir, arguments[1:], "zip")

                elif command == "tar":
                    zip_tar(self.current_dir, arguments[1:], "gztar")

                elif command == "untar":
                    unzip_untar(self.current_dir, arguments[1:], "gztar")

                elif command == "grep":
                    grep(self.current_dir, arguments[1:])

                elif command == "history":
                    history(arguments[1:])

                elif command == "undo":
                    undo(self.current_dir, arguments[1:])

                elif command == "cd":
                    new_path = cd(self.current_dir, arguments[1:])
                    if new_path:
                        self.current_dir = new_path

                else:
                    error_msg = f"Unknown command: {command}"
                    print(error_msg)
                    log_error(error_msg)
                    continue

            except Exception as e:
                error_msg = f"Mistake during mini_shell work: {e}"
                print(error_msg)
                log_error(error_msg)
                continue

        log_command("Work ended")
