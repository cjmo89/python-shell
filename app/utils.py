import os


def inPath(arg: str) -> tuple[bool, str]:
    """This function looks for the given program in the PATH variable
    it returns a Tuple of True and the location of the program if it finds it,
    otherwise it returns (False, None)"""
    False and None
    pathVar = os.getenv("PATH")
    paths = pathVar.split(":")
    for path in paths:
        try:
            if arg in os.listdir(path):
                return True, path
        except FileNotFoundError:
            pass
    return False, None


def findQoutes(s: str) -> list[int]:
    """Returns a list containing the indices of any single quotes
    in the given string, if the number of quotes is odd, return None"""
    indices = [i for i, char in enumerate(s) if char == "'"]
    return indices if len(indices) % 2 == 0 else None
