import shlex
from app.main import echo


def test_no_quotes_basic():
    input = shlex.split("echo good job")
    assert "good job" == echo(input)


def test_no_quotes_spaces():
    input = shlex.split("echo waste   of   space")
    assert "waste of space" == echo(input)


def test_quotes():
    input = shlex.split("echo 'this is' 'great'")
    assert "this is great" == echo(input)


def test_empty_quotes():
    input = shlex.split("echo ''")
    assert "" == echo(input)


def test_continuous_quotes():
    input = shlex.split("echo 'test     world' 'shell''hello'")
    assert "test     world shellhello" == echo(input)


def test_double_quotes():
    input = shlex.split('echo "quz  hello"  "bar"')
    assert "quz  hello bar" == echo(input)


def test_mixed_quotes_two():
    input = shlex.split("echo \"not 'great' is it?\"")
    assert "not 'great' is it?" == echo(input)


def test_unquoted_intermediates():
    input = shlex.split("echo 'aa' bb 'cc'")
    assert "aa bb cc" == echo(input)


def test_quoted_backslash():
    input = shlex.split('echo "before\   after"')
    assert "before\   after" == echo(input)


def test_unquoted_backslashed():
    input = shlex.split("echo world\ \ \ \ \ \ script")
    assert "world      script" == echo(input)
