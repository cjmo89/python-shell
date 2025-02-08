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


def test_continuous_quotes():
    input = parseInput("echo 'test     world' 'shell''hello'")
    assert "test     world shellhello" == echo(input)
