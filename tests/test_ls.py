from pathlib import Path
from src.commands.ls import ls

def test_ls_empty_directory(fake_fs):
    path = Path("empty_dir")
    fake_fs.create_dir(path)

    result = ls(path, [])
    assert result is True

def test_ls_with_files(fake_fs):
    path = Path("test_dir")
    fake_fs.create_dir(path)
    fake_fs.create_file((path / "file1.txt"), contents="content1")
    fake_fs.create_file((path / "file2.txt"), contents="content2")

    result = ls(path, [])
    assert result is True
