import os
from app.quotestack import QuoteStack


def inPath(arg: str) -> tuple[bool, str]:
    """This function looks for the given program in the PATH variable
    it returns a Tuple of True and the location of the program if it finds it,
    otherwise it returns (False, None)"""
    False and None
    pathVar = os.getenv("PATH")
    paths = pathVar.split(":")
    for path in paths:
        try:
            if arg in os.listdir(path):
                return True, path
        except FileNotFoundError:
            pass
    return False, None


def parseQuotes(inString: str, quoteType: str) -> list[str]:
    parseList = []
    if quoteType == "'" or quoteType == '"':
        if inString.count(quoteType) % 2 == 1:
            return inString.split()
        indices = [i for i, char in enumerate(inString) if char == quoteType]

        # First parse anything that might appear before the quotes
        if indices[0] > 0:
            parseList += inString[: indices[0]].split()

        # Next add the quoted strings
        quoteStack = QuoteStack()
        for i in range(0, len(indices)):
            if not quoteStack.isEmpty():  # If it's a closing quote
                quoteStack.pop()
                if i + 1 < len(indices):
                    parseList += inString[indices[i] + 1 : indices[i + 1]].split()
            else:
                quoteStack.push(quoteType)
                if indices[i] > 0 and inString[indices[i] - 1] == " ":
                    # If the last character was space, append a new arg
                    parseList.append(inString[indices[i] + 1 : indices[i + 1]])
                else:
                    if len(parseList) == 0:
                        # The command itself is quoted so there's nothing in the parseList yet
                        parseList.append(inString[indices[i] + 1 : indices[i + 1]])
                    else:  # Else append to the previous one
                        parseList[-1] += inString[indices[i] + 1 : indices[i + 1]]

        # Finally, add anything that comes after the quotes
        if len(inString) > indices[-1] + 1:
            parseList += inString[indices[-1] + 1 :].split()
        return parseList
    else:  # We have a mix of double and single quotes
        quotesStack = QuoteStack()
        indices = [i for i, char in enumerate(inString) if char == "'" or char == '"']

        # First parse anything that might appear before the quotes
        if indices[0] > 0:
            parseList += inString[: indices[0]].split()

        # Next add the quoted strings
        for i in range(len(indices)):
            currentQuote = inString[indices[i]]
            if quotesStack.isEmpty():
                quotesStack.push(currentQuote)
                if inString[indices[i + 1]] == currentQuote:
                    # A closing quote is coming, append until met
                    parseList.append(inString[indices[i] + 1 : indices[i + 1]])
                else:  # A nested quote is coming later
                    # Append a new string to the list, ending at the quote
                    parseList.append(inString[indices[i] + 1 : indices[i + 1]])
            else:
                if quotesStack.peek() == currentQuote:  # Is it a closing quote?
                    quotesStack.pop()  # Pop the opening quote and append from the quote itself
                    if i + 1 < len(indices):  # If there are quotes left to be processed
                        if quotesStack.isEmpty():  # It was a top level closing quote
                            # Add anything that might come in between the quotes
                            parseList += inString[
                                indices[i] + 1 : indices[i + 1]
                            ].split()
                        else:  # We're still in quoting mode
                            parseList[-1] += inString[indices[i] : indices[i + 1]]
                else:  # It's an opening quote
                    quotesStack.push(currentQuote)
                    # Apeend to the current string until we find the closing quote
                    parseList[-1] += inString[indices[i] : indices[i + 1]]

        # Finally, add anything that comes after the quotes
        if len(inString) > indices[-1] + 1:
            parseList += inString[indices[-1] + 1 :].split()
        return parseList
