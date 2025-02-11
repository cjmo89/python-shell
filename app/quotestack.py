"""Small class representing a stack of quotes to use when evaluating input"""


class QuoteStack:
    def __init__(self):
        self.stack = []

    def pop(self):
        if len(self.stack) > 0:
            return self.stack.pop()
        else:
            raise IndexError("No elements in the Stack")

    def push(self, char):
        self.stack.append(char)

    def peek(self, depth=0):
        return self.stack[-1 + depth]

    def isFull(self):
        return len(self.stack) == 2

    def isEmpty(self):
        return len(self.stack) == 0
