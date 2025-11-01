import tempfile
import shutil
from pathlib import Path
import pytest # type: ignore
from pyfakefs.fake_filesystem import FakeFilesystem # type: ignore


@pytest.fixture
def temp_dir():
    """
    Создаёт временную папку и удаляет её после теста
    """
    path = Path(tempfile.mkdtemp())
    yield path
    shutil.rmtree(path)


@pytest.fixture
def fake_fs():
    """
    Возвращает фейковую файловую систему для тестов
    """
    return FakeFilesystem()
