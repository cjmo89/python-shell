import sys
import os
import subprocess

import app.utils

builtins = ["echo", "exit", "type", "pwd", "cd"]


def main():
    while True:
        sys.stdout.write("$ ")
        # Wait for user input
        inString = input()
        inputList = parseInput(inString)
        command = inputList[0]
        match command:
            case "exit":
                if len(inputList) > 1:
                    sys.exit(int(inputList[1]))  # exit returning the first arg
                sys.exit()
            case "echo":
                out = ""
                if len(inputList) > 1:
                    for i, s in enumerate(inputList[1:]):
                        # -2 because we start from the second item
                        if i == len(inputList) - 2:
                            out += s
                        else:
                            out += s + " "
                print(out)
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
                isInPath, path = app.utils.inPath(command)
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
        result, path = app.utils.inPath(arg)
        if result:
            print(f"{arg} is {path}/" + arg)
        print(f"{arg}: not found")


def parseInput(inString: str) -> list[str]:
    """Returns the commands and parameters in the given prompt string
    as a list of strings"""
    quotesIndices = app.utils.findQoutes(inString)
    if not quotesIndices:
        return inString.split()
    commands = inString[: quotesIndices[0]].split()
    for i in range(0, len(quotesIndices), 2):
        # Append each quoted phrase, starting at the beginning of the word,
        # +1 so the starting quote itself isn't appended
        commands.append(inString[quotesIndices[i] + 1 : quotesIndices[i + 1]])
    return commands


if __name__ == "__main__":
    main()
