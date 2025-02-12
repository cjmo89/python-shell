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
        stdout, stderr = "", ""
        if ">" in inputList or "1>" in inputList or "2>" in inputList:
            stdout, stderr = rearrange(inputList)
            if ((">" in inputList or "1>" in inputList) and not stdout) or (
                "2>" in inputList and not stderr
            ):
                print("Parse error")
                continue
        command = inputList[0]
        match command:
            case "exit":
                if len(inputList) > 1:
                    sys.exit(int(inputList[1]))  # exit returning the first arg
                sys.exit()
            case "echo":
                echo(inputList, stdout, stderr)
            case "type":
                type(inputList[1:], stdout)
            case "pwd":
                if stdout:
                    printToFile(stdout, os.getcwd())
                else:
                    printToFile(outContent=os.getcwd() + "\n")
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
                    if stdout and stderr:
                        with open(stdout, "w") as fOut, open(stderr, "w") as fErr:
                            subprocess.run(inputList, stdout=fOut, stderr=fErr)
                    elif stdout:
                        with open(stdout, "w") as f:
                            subprocess.run(inputList, stdout=f)
                    elif stderr:
                        with open(stderr, "w") as f:
                            subprocess.run(inputList, stderr=f)
                    else:
                        subOutput = subprocess.run(inputList)
                        if subOutput.stdout:
                            print(subOutput.stdout)
                else:
                    if stderr:
                        printToFile(
                            stderr=stderr, errContent=f"{command}: command not found"
                        )
                    else:
                        printToFile(
                            stderr="stderr", errContent=f"{command}: command not found"
                        )


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
    if not out:
        out = "stdout"
    s += "\n"
    printToFile(out, s)
    return s  # For testing


def echo(inputList: list[str], out: str = "stdout", err: str = "stderr") -> None:
    sOut = ""
    if len(inputList) > 1:
        for i, s in enumerate(inputList[1:]):
            # -2 because we start from the second item
            if i == len(inputList) - 2:
                sOut += s
            else:
                sOut += s + " "
    sOut += "\n"
    if not out:
        out = "stdout"  # echo doesn't output to stderr
    if out and err:
        printToFile(out, sOut, err)
    else:
        printToFile(out, sOut)
    return sOut  # For testing


def rearrange(inputList: list[str]) -> tuple[str, str]:
    """Extracts the files for std output and std error redirection
    and returns them"""
    if inputList[-1] == ">" or inputList[-1] == "1>":
        print("Parse error")
        return "", ""
    if inputList.count(">") > 1 or inputList.count("1>") > 1:
        print("Only single file output redirection is supported")
        return "", ""
    stdout = ""
    stderr = ""
    if ">" in inputList:
        i = inputList.index(">")
        stdout = inputList[i + 1]
        inputList.remove(">")
        inputList.remove(stdout)
    elif "1>" in inputList:
        i = inputList.index("1>")
        stdout = inputList[i + 1]
        inputList.remove("1>")
        inputList.remove(stdout)
    if "2>" in inputList:
        i = inputList.index("2>")
        stderr = inputList[i + 1]
        inputList.remove("2>")
        inputList.remove(stderr)
    return stdout, stderr


if __name__ == "__main__":
    main()
