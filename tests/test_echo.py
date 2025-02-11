from app.main import echo, parseInput


def test_no_quotes_basic():
    input = parseInput("echo good job")
    assert "good job" == echo(input)


def test_no_quotes_spaces():
    input = parseInput("echo waste   of   space")
    assert "waste of space" == echo(input)


def test_odd_quotes():
    input = parseInput("echo 'tis o'couse f'ed")
    assert "'tis o'couse f'ed" == echo(input)


def test_odd_quotes_spaces():
    input = parseInput("echo i'm    way 2    long")
    assert "i'm way 2 long" == echo(input)


def test_quotes():
    input = parseInput("echo 'this is' 'great'")
    assert "this is great" == echo(input)


def test_empty_quotes():
    input = parseInput("echo ''")
    assert "" == echo(input)


def test_continuous_quotes():
    input = parseInput("echo 'test     world' 'shell''hello'")
    assert "test     world shellhello" == echo(input)


def test_double_quotes():
    input = parseInput('echo "quz  hello"  "bar"')
    assert "quz  hello bar" == echo(input)


def test_mixed_quotes_two():
    input = parseInput("echo \"not 'great' is it?\"")
    assert "not 'great' is it?" == echo(input)


def test_unquoted_intermediates():
    input = parseInput("echo 'aa' bb 'cc'")
    assert "aa bb cc" == echo(input)
