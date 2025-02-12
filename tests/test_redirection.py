import shlex
from app.main import rearrange


def test_ls_redirect():
    input = shlex.split("ls ~/test > out.txt")
    rearrange(input)
    assert ["ls", "~/test", ">", "out.txt"] == input
