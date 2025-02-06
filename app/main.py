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
                sys.exit(int(strings[1]))  # exit returning the first arg
            case "echo":
                print(inString[5:])
            case _:
                print(f"{command}: command not found")


if __name__ == "__main__":
    main()
