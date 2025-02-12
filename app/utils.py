import os
import sys


def inPath(arg: str) -> tuple[bool, str]:
    """This function looks for the given program in the PATH variable
    it returns a Tuple of True and the location of the program if it finds it,
    otherwise it returns (False, "")"""
    pathVar = os.getenv("PATH")
    paths = pathVar.split(":")
    for path in paths:
        try:
            if arg in os.listdir(path):
                return True, path
        except FileNotFoundError:
            pass
    return False, ""


def printToFile(stdout="stdout", outContent="", stderr="stderr", errContent=""):
    if stdout == "stdout":
        sys.stdout.write(outContent)
    else:
        with open(stdout, "w") as f:
            f.write(outContent)
    if stderr == "stderr" and errContent:
        print(errContent, file=sys.stderr)
    else:
        with open(stderr, "w") as f:
            f.write(errContent)
