from pathlib import Path
from src.commands.history import add_command, history

def test_add_command_to_history(fs):

    add_command("privet loool")

    hist_file = Path(".history")
    assert hist_file.exists()
    content = hist_file.read_text()
    assert "privet loool" in content


def test_history_command(fs):

    add_command("privet loool")
    add_command("cat i want sleeeepp")

    result = history([])
    assert result is True
