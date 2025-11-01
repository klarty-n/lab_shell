from pathlib import Path


def test_rm_file(fs):

    file_path = Path("file.txt")
    file_path.write_text("hell")

    from src.commands.rm import rm
    result = rm(Path(""), ["file.txt"])

    assert result is True
    assert not file_path.exists()

def test_rm_nonexistent_file(fs):

    from src.commands.rm import rm
    result = rm(Path(""), ["notexistent.txt"])
    assert result is False
