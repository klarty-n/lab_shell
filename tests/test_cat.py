from pathlib import Path
from src.commands.cat import cat

def test_cat_existing_file(fs):

    file_path = Path("test.txt")
    file_path.write_text("HI BRO ")

    result = cat(Path(""), ["test.txt"])
    assert result is True

def test_cat_notexistent_file(fs):

    result = cat(Path(""), ["notexistent.txt"])
    assert result is False


def test_cat_directory_as_file(fs):

    dir_path = Path("test_dir")
    dir_path.mkdir()

    result = cat(Path(""), ["test_dir"])
    assert result is False


def test_cat_multiple_files(fs):

    file1 = Path("file1.txt")
    file2 = Path("file2.txt")
    file1.write_text("Pashalka")
    file2.write_text("I_want_sleep")

    result = cat(Path(""), ["file1.txt", "file2.txt"])
    assert result is True
