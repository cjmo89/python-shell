import sys


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
            case _:
                print(f"{command}: command not found")


def type(arg):
    builtins = ["echo", "exit"]
    if arg in builtins:
        return f"{arg} is a shell builtin"
    else:
        return f"{arg}: not found"


if __name__ == "__main__":
    main()
