import shlex
from app.main import typeCommand


def test_type_builtin():
    input = shlex.split("type echo")
    assert typeCommand(input[1:]) == "echo is a shell builtin\n"


def test_type_not_found():
    input = shlex.split("type nonexistentcommand")
    assert typeCommand(input[1:]) == "nonexistentcommand: not found\n"
