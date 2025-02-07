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


def findQoutes(s: str) -> tuple[int]:
    """Returns a Tuple containing the indices of the first and last single quote '
    in the given string"""
    indices = [i for i, char in enumerate(s) if char == "'"]
    if len(indices) < 2:
        return None
    return (indices[0], indices[-1])
