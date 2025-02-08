from app.main import parseInput


def test_no_quotes_basic():
    assert ["cd", ".."] == parseInput("cd ..")


def test_no_quotes_multiple():
    assert ["type", "cd", "pwd"] == parseInput("type cd pwd")


def test_quotes_multiple_inputs():
    assert ["type", "cd", "pwd"] == parseInput("type 'cd' 'pwd'")


def test_starting_quotes():
    assert ["cd", ".."] == parseInput("'cd' ..")


def test_trailing_whitespace():
    assert ["cd", "python"] == parseInput("cd python ")
