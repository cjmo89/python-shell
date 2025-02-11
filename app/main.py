import sys
import os
import subprocess

from app.utils import parseQuotes
from app.utils import inPath

builtins = ["echo", "exit", "type", "pwd", "cd"]


def main():
    while True:
        sys.stdout.write("$ ")
        # Wait for user input
        try:
            inString = input()
        except EOFError:
            print("")
            break
        inputList = parseInput(inString)
        command = inputList[0]
        match command:
            case "exit":
                if len(inputList) > 1:
                    sys.exit(int(inputList[1]))  # exit returning the first arg
                sys.exit()
            case "echo":
                print(echo(inputList))
            case "type":
                type(inputList[1:])
            case "pwd":
                print(os.getcwd())
            case "cd":
                home = os.path.expanduser("~")
                if len(inputList) > 1:
                    if inputList[1] == "~":
                        os.chdir(home)
                    else:
                        try:
                            os.chdir(inputList[1])
                        except FileNotFoundError:
                            print(f"cd: {inputList[1]}: No such file or directory")
                else:
                    os.chdir(home)
            case _:
                isInPath, path = inPath(command)
                if isInPath:
                    subOutput = subprocess.run(inputList)
                    if subOutput.stdout:
                        print(subOutput.stdout)
                else:
                    print(f"{command}: command not found")


def type(args):
    for arg in args:
        if arg in builtins:
            print(f"{arg} is a shell builtin")
            continue
        result, path = inPath(arg)
        if result:
            print(f"{arg} is {path}/" + arg)
            continue
        print(f"{arg}: not found")


def echo(inputList: list[str]) -> str:
    out = ""
    if len(inputList) > 1:
        for i, s in enumerate(inputList[1:]):
            # -2 because we start from the second item
            if i == len(inputList) - 2:
                out += s
            else:
                out += s + " "
    return out


def parseInput(inString: str) -> list[str]:
    """Returns the command and parameters in the given prompt string
    as a list of strings"""
    totalQoutes = inString.count("'")
    totalDquotes = inString.count('"')
    if totalQoutes == 0 and totalDquotes == 0:
        return inString.split()  # There are no quotes so just split on whitspace

    if totalQoutes > 0 and totalDquotes == 0:
        return parseQuotes(inString, "'")  # There are only single quotes
    elif totalQoutes == 0 and totalDquotes > 0:
        return parseQuotes(inString, '"')  # There are only double quotes
    else:  # We have mixed single and double quotes
        if totalQoutes % 2 == 1:  # There's an odd number of single quotes
            # Treat them as normal characters and only consider the double quotes
            return parseQuotes(inString, '"')
        elif totalDquotes % 2 == 1:  # There's an odd number of double quotes
            # Treat them as normal characters and only consider the single quotes
            return parseQuotes(inString, "'")
        else:  # There is an even number of both quotes
            return parseQuotes(inString, "mixed")


if __name__ == "__main__":
    main()
