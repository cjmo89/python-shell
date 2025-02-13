import shlex
from app.main import parseRedirects
from app.main import echo


def test_ls_redirect():
    inputList = shlex.split("ls ~/test > out.txt")
    parseRedirects(inputList)
    assert ["ls", "~/test"] == inputList


def test_stderr_redirection():
    inputList = shlex.split("echo 'Maria file cannot be found' 2> test.txt")
    out, err, outAppend, errAppend = parseRedirects(inputList)
    assert (
        echo(inputList[1:], out, err, outAppend, errAppend)
        == "Maria file cannot be found\n"
    )
