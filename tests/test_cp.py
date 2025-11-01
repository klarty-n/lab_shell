from pathlib import Path
from src.commands.cp import cp

def test_cp_file_to_file(fs):
    source = Path("source.txt")
    source.write_text("hi brooo")
    target = Path("target.txt")

    result = cp(Path(""), ["source.txt", "target.txt"])

    assert result is None
    assert target.exists()
    assert target.read_text() == "hi brooo"


def test_cp_nonexistent_file(fs):

    result = cp(Path(""), ["nonexistent.txt", "dest.txt"])
    assert result is False


def test_cp_directory_without_r_flag(fs):

    dir_path = Path("source_dir")
    dir_path.mkdir()

    result = cp(Path(""), ["source_dir", "dest_dir"])
    assert result is False


def test_cp_directory_with_r_flag(fs):

    source_dir = Path("source_dir")
    source_dir.mkdir()
    (source_dir / "file.txt").write_text("hello")

    result = cp(Path(""), ["-r", "source_dir", "dest_dir"])

    assert result is True
    dest_dir = Path("/dest_dir")
    assert dest_dir.exists()
    assert (dest_dir / "file.txt").exists()
    assert (dest_dir / "file.txt").read_text() == "hello"
