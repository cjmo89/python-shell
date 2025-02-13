import shlex
from app.main import echo


def test_no_quotes_basic():
    inputList = shlex.split("echo good job")
    assert echo(inputList[1:]) == "good job\n"


def test_no_quotes_spaces():
    inputList = shlex.split("echo waste   of   space")
    assert echo(inputList[1:]) == "waste of space\n"


def test_quotes():
    inputList = shlex.split("echo 'this is' 'great'")
    assert echo(inputList[1:]) == "this is great\n"


def test_empty():
    assert echo([]) == "\n"


def test_empty_quotes():
    inputList = shlex.split("echo ''")
    assert echo(inputList[1:]) == "\n"


def test_continuous_quotes():
    inputList = shlex.split("echo 'test     world' 'shell''hello'")
    assert echo(inputList[1:]) == "test     world shellhello\n"


def test_double_quotes():
    inputList = shlex.split('echo "quz  hello"  "bar"')
    assert echo(inputList[1:]) == "quz  hello bar\n"


def test_mixed_quotes_two():
    inputList = shlex.split("echo \"not 'great' is it?\"")
    assert echo(inputList[1:]) == "not 'great' is it?\n"


def test_unquoted_intermediates():
    inputList = shlex.split("echo 'aa' bb 'cc'")
    assert echo(inputList[1:]) == "aa bb cc\n"


def test_quoted_backslash():
    inputList = shlex.split('echo "before\   after"')
    assert echo(inputList[1:]) == "before\   after\n"


def test_unquoted_backslashed():
    inputList = shlex.split("echo world\ \ \ \ \ \ script")
    assert echo(inputList[1:]) == "world      script\n"
