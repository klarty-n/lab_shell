from src.mini_shell import mini_shell

def main() -> None:
    """
    Точка входа программы
    :return: ничего не возвращает
    """
    shell = mini_shell()
    shell.run()

if __name__ == "__main__":
    main()
