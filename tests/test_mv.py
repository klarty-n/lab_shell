from pathlib import Path
from src.commands.mv import mv

def test_mv_file_to_new_name(fs):

    source = Path("source.txt")
    source.write_text("lol")

    result = mv(Path(""), ["source.txt", "target.txt"])

    assert result is True

    target = Path("target.txt")
    assert target.exists()
    assert target.read_text() == "lol"
    assert not source.exists()

def test_mv_file_to_directory(fs):

    source = Path("source.txt")
    source.write_text("lol")
    target_dir = Path("target_dir")
    target_dir.mkdir()

    result = mv(Path(""), ["source.txt", "target_dir"])

    assert result is True
    moved_file = target_dir / "source.txt"
    assert moved_file.exists()
    assert moved_file.read_text() == "lol"
    assert not source.exists()

def test_mv_nonexistent_file(fs):

    result = mv(Path(""), ["nonexistent.txt", "target.txt"])
    assert result is False
