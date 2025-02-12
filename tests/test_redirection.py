import shlex
from app.main import rearrange
from app.main import echo


def test_ls_redirect():
    input = shlex.split("ls ~/test > out.txt")
    rearrange(input)
    assert ["ls", "~/test"] == input


def test_stderr_redirection():
    input = shlex.split("echo 'Maria file cannot be found' 2> /tmp/quz/foo.md")
    rearrange(input)
    assert echo(input) == "Maria file cannot be found\n"
