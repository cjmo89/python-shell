import sys
import os
import subprocess

import app.utils

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
            continue
        result, path = app.utils.inPath(arg)
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
    if totalQoutes == 0 or totalQoutes % 2 == 1:
        return inString.split()  # Treat uneven quotes as normal characters
    parseList = []
    indices = app.utils.findQoutes(inString)

    # First parse anything that might appear before the quotes
    if indices[0] > 0:
        parseList = inString[
            : indices[0]
        ].split()  # Add everything that isn't quoted to the parseList

    # Next add the quoted strings
    for i in range(0, len(indices), 2):
        # i is the opening quote i + 1 is the closing one
        if (
            i > 0 and inString[indices[i] - 1] == "'"
        ):  # If the previous character was a quote, we're dealing with continuous quotes
            parseList[len(parseList) - 1] += inString[
                indices[i] + 1 : indices[i + 1]
            ]  # In this case, concatenate the next string onto the previous one
        else:  # Add a new string to the list as usual
            parseList.append(inString[indices[i] + 1 : indices[i + 1]])

    # Finally, add anything that comes after the quotes
    if len(inString) > indices[-1] + 1:
        parseList += inString[indices[-1] + 1 :].split()
    return parseList


if __name__ == "__main__":
    main()
