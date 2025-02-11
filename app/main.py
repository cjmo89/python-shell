import sys
import os
import subprocess
import shlex

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
        try:
            inputList = shlex.split(inString)
        except ValueError as e:
            print("Error: ", e)
            continue
        if len(inputList) == 0:
            continue
        file = "stdout"
        if ">" in inputList:
            file = rearrange(inputList)
            if not file:
                continue
        command = inputList[0]
        match command:
            case "exit":
                if len(inputList) > 1:
                    sys.exit(int(inputList[1]))  # exit returning the first arg
                sys.exit()
            case "echo":
                echo(inputList, file)
            case "type":
                type(inputList[1:], file)
            case "pwd":
                if file == "stdout":
                    print(os.getcwd)
                else:
                    with open(file, "w") as f:
                        f.write(os.getcwd)
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
                        if file == "stdout":
                            print(subOutput.stdout)
                        else:
                            with open(file, "w") as f:
                                f.write(subOutput.stdout)
                else:
                    print(f"{command}: command not found")


def type(inputList, out="stdout"):
    s = ""
    for arg in inputList:
        if arg in builtins:
            s += f"{arg} is a shell builtin"
            continue
        result, path = inPath(arg)
        if result:
            s += f"{arg} is {path}/" + arg
            continue
        s += f"{arg}: not found"
    if out == "stdout":
        print(s)
    else:
        with open(out, "w") as f:
            f.write(s + "\n")


def echo(inputList: list[str], out: str = "stdout") -> None:
    sOut = ""
    if len(inputList) > 1:
        for i, s in enumerate(inputList[1:]):
            # -2 because we start from the second item
            if i == len(inputList) - 2:
                sOut += s
            else:
                sOut += s + " "
    if out == "stdout":
        print(sOut)
    else:
        with open(out, "w") as f:
            f.write(sOut + "\n")


def rearrange(inputList: list[str]) -> str:
    """rearranges the input list to have all the args after the command
    and returns the given file name"""
    if inputList[-1] == ">":
        print("Parse error")
        return None
    if inputList.count(">") > 1:
        print("Only single file output redirection is supported")
        return None
    i = inputList.index(">")
    file = inputList[i + 1]
    inputList.remove(">")
    inputList.remove(file)
    return file


if __name__ == "__main__":
    main()
