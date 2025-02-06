import sys
import os
import subprocess


def main():
    while True:
        sys.stdout.write("$ ")
        # Wait for user input
        inString = input()
        strings = inString.split()
        command = strings[0]
        match command:
            case "exit":
                if len(strings) > 1:
                    sys.exit(int(strings[1]))  # exit returning the first arg
                sys.exit()
            case "echo":
                print(inString[5:])
            case "type":
                print(type(strings[1]))
            case "pwd":
                print(os.getcwd())
            case _:
                result, path = inPath(command)
                if result:
                    subOutput = subprocess.run(strings)
                    if subOutput.stdout:
                        print(subOutput.stdout)
                else:
                    print(f"{command}: command not found")


def type(arg):
    builtins = ["echo", "exit", "type", "pwd"]
    if arg in builtins:
        return f"{arg} is a shell builtin"
    result, path = inPath(arg)
    if result:
        return f"{arg} is {path}/" + arg
    return f"{arg}: not found"


def inPath(arg):
    pathVar = os.getenv("PATH")
    paths = pathVar.split(":")
    for path in paths:
        try:
            if arg in os.listdir(path):
                return True, path
        except FileNotFoundError:
            pass
    return False, None


if __name__ == "__main__":
    main()
