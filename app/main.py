import sys
import os
import subprocess
import shlex
import readline

from app.utils import inPath, printToFile

builtins = ["echo", "exit", "type", "pwd", "cd"]
customs = []


def main():
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")
    while True:
        # sys.stdout.write("$ ")
        # Wait for user input
        try:
            inString = input("$ ")
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
        try:
            stdout, stderr, stdoutAppend, stderrAppend = parseRedirects(inputList)
        except ValueError as e:
            print(e)
            continue
        command = inputList[0]
        match command:
            case "exit":
                if len(inputList) > 1:
                    sys.exit(int(inputList[1]))  # exit returning the first arg
                sys.exit()
            case "echo":
                echo(inputList[1:], stdout, stderr, stdoutAppend, stderrAppend)
            case "type":
                typeCommand(inputList[1:], stdout, stderr, stdoutAppend, stderrAppend)
            case "pwd":
                pwd(stdout, stderr, stdoutAppend, stderrAppend)
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
                    outMode = "a" if stdoutAppend else "w"
                    errMode = "a" if stderrAppend else "w"
                    if stdout and stderr:
                        with (
                            open(stdout, outMode) as fOut,
                            open(stderr, errMode) as fErr,
                        ):
                            subprocess.run(inputList, stdout=fOut, stderr=fErr)
                    elif stdout:
                        with open(stdout, outMode) as f:
                            subprocess.run(inputList, stdout=f)
                    elif stderr:
                        with open(stderr, errMode) as f:
                            subprocess.run(inputList, stderr=f)
                    else:
                        subOutput = subprocess.run(inputList)
                        if subOutput.stdout:
                            print(subOutput.stdout)
                else:
                    if stderr:
                        printToFile(
                            stderr=stderr,
                            errContent=f"{command}: command not found",
                            errAppend=stderrAppend,
                        )
                    else:
                        printToFile(
                            stderr="stderr",
                            errContent=f"{command}: command not found",
                            errAppend=stderrAppend,
                        )


def typeCommand(
    inputList, out="stdout", err="stderr", outAppend=False, errAppend=False
):
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
    if not out:
        out = "stdout"
    if out and err:
        printToFile(out, s, err, "", outAppend, errAppend)
    else:
        printToFile(out, s, outAppend=outAppend)
    return s  # For testing


def echo(
    inputList: list[str],
    out: str = "stdout",
    err: str = "stderr",
    outAppend: bool = False,
    errAppend: bool = False,
) -> None:
    sOut = ""
    for i, s in enumerate(inputList):
        if i == len(inputList) - 1:
            sOut += s
        else:
            sOut += s + " "
    sOut += "\n"
    if not out:
        out = "stdout"  # echo doesn't output to stderr
    if out and err:
        printToFile(out, sOut, err, "", outAppend, errAppend)
    else:
        printToFile(out, sOut, outAppend=outAppend)
    return sOut  # For testing


def pwd(stdout, stderr, outAppend, errAppend):
    if not stdout:
        stdout = "stdout"
    if stdout and stderr:
        printToFile(stdout, os.getcwd(), stderr, "", outAppend, errAppend)
    else:
        printToFile(outContent=os.getcwd() + "\n", outAppend=outAppend)


def parseRedirects(inputList: list[str]) -> tuple[str, str, bool, bool]:
    if inputList[-1] == ">" or inputList[-1] == "1>":
        raise ValueError("Parse error, no file specified")
    if (
        inputList.count(">") > 1
        or inputList.count("1>") > 1
        or inputList.count("2>") > 1
        or inputList.count(">>") > 1
        or inputList.count("1>>") > 1
        or inputList.count("2>>") > 1
    ):
        raise ValueError("Only single file output redirection is supported")
    stdout = ""
    stderr = ""
    stdoutAppend = False
    stderrAppend = False
    if ">" in inputList:
        i = inputList.index(">")
        stdout = inputList[i + 1]
        inputList.remove(">")
        inputList.remove(stdout)
    elif "1>" in inputList:
        if stdout:
            raise ValueError("Only single file output redirection is supported")
        i = inputList.index("1>")
        stdout = inputList[i + 1]
        inputList.remove("1>")
        inputList.remove(stdout)
    if "2>" in inputList:
        i = inputList.index("2>")
        stderr = inputList[i + 1]
        inputList.remove("2>")
        inputList.remove(stderr)
    if ">>" in inputList:
        if stdout:
            raise ValueError("Only single file output redirection is supported")
        i = inputList.index(">>")
        stdout = inputList[i + 1]
        inputList.remove(">>")
        inputList.remove(stdout)
        stdoutAppend = True
    if "1>>" in inputList:
        if stdout:
            raise ValueError("Only single file output redirection is supported")
        i = inputList.index("1>>")
        stdout = inputList[i + 1]
        inputList.remove("1>>")
        inputList.remove(stdout)
        stdoutAppend = True
    if "2>>" in inputList:
        if stderr:
            raise ValueError("Only single file output redirection is supported")
        i = inputList.index("2>>")
        stderr = inputList[i + 1]
        inputList.remove("2>>")
        inputList.remove(stderr)
        stderrAppend = True
    return stdout, stderr, stdoutAppend, stderrAppend


def completer(text, state):
    completions = builtins + customs
    completions = list(set(completions))
    # Filter commands based on the current text input
    matches = [cmd for cmd in completions if cmd.startswith(text)]
    if state < len(matches):
        if len(matches) == 1:
            return matches[state] + " "
        return matches[state]
    return None


if __name__ == "__main__":
    pathVar = os.getenv("PATH")
    paths = pathVar.split(":")
    for path in paths:
        try:
            customs += os.listdir(path)
        except FileNotFoundError:
            pass
    main()
