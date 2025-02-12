import sys
import os
import subprocess
import shlex

from app.utils import inPath, printToFile

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
        if ">" in inputList or "1>" in inputList:
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
                printToFile(file, os.getcwd())
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
                    if file != "stdout":
                        with open(file, "w") as f:
                            subprocess.run(inputList, stdout=f)
                    else:
                        subOutput = subprocess.run(inputList)
                        if subOutput.stdout:
                            print(subOutput.stdout)
                else:
                    printToFile(file, f"{command}: command not found")


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
    printToFile(s)


def echo(inputList: list[str], out: str = "stdout") -> None:
    sOut = ""
    if len(inputList) > 1:
        for i, s in enumerate(inputList[1:]):
            # -2 because we start from the second item
            if i == len(inputList) - 2:
                sOut += s
            else:
                sOut += s + " "
    printToFile(out, sOut)


def rearrange(inputList: list[str]) -> str:
    """rearranges the input list to have all the args after the command
    and returns the given file name"""
    if inputList[-1] == ">" or inputList[-1] == "1>":
        print("Parse error")
        return None
    if inputList.count(">") > 1 or inputList.count("1>") > 1:
        print("Only single file output redirection is supported")
        return None
    if ">" in inputList:
        i = inputList.index(">")
        file = inputList[i + 1]
        inputList.remove(">")
    else:
        i = inputList.index("1>")
        file = inputList[i + 1]
        inputList.remove("1>")
    inputList.remove(file)
    return file


if __name__ == "__main__":
    main()
