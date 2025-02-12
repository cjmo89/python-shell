import shlex
from app.main import echo


def test_no_quotes_basic():
    input = shlex.split("echo good job")
    assert echo(input) == "good job"


def test_no_quotes_spaces():
    input = shlex.split("echo waste   of   space")
    assert echo(input) == "waste of space"


def test_quotes():
    input = shlex.split("echo 'this is' 'great'")
    assert echo(input) == "this is great"


def test_empty_quotes():
    input = shlex.split("echo ''")
    assert echo(input) == ""


def test_continuous_quotes():
    input = shlex.split("echo 'test     world' 'shell''hello'")
    assert echo(input) == "test     world shellhello"


def test_double_quotes():
    input = shlex.split('echo "quz  hello"  "bar"')
    assert echo(input) == "quz  hello bar"


def test_mixed_quotes_two():
    input = shlex.split("echo \"not 'great' is it?\"")
    assert echo(input) == "not 'great' is it?"


def test_unquoted_intermediates():
    input = shlex.split("echo 'aa' bb 'cc'")
    assert echo(input) == "aa bb cc"


def test_quoted_backslash():
    input = shlex.split('echo "before\   after"')
    assert echo(input) == "before\   after"


def test_unquoted_backslashed():
    input = shlex.split("echo world\ \ \ \ \ \ script")
    assert echo(input) == "world      script"
