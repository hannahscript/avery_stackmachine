from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    SYMBOL = 0
    SEMICOLON = 1
    COLON = 2
    NUMBER = 3
    EOF = 4


@dataclass
class Token:
    type: TokenType
    literal: str
    value: int = 0

    def __repr__(self):
        if self.type == TokenType.NUMBER:
            return f'#{self.value}'
        elif self.type == TokenType.SYMBOL:
            return f'({self.literal})'
        else:
            return self.literal


class Lexer:
    def __init__(self):
        self.index = 0
        self.source = ''
        self.buffer = ''
        self.tokens = []

    def lex(self, filename):
        f = open(filename, 'r')
        self.source = f.read()

        while self.has_next():
            c = self.consume()
            if c in [';', ':']:
                self.push_buffer()
                self.buffer = c
                self.push_buffer()
            elif c.isspace():
                self.push_buffer()
            elif c == '/' and self.source[self.index] == '/':
                self.push_buffer()
                while self.has_next() and c != '\n':
                    c = self.consume()
            else:
                self.buffer += c
        self.push_buffer()
        return self.tokens

    def push_buffer(self):
        if len(self.buffer) > 0:
            self.tokens.append(self.reify())
            self.buffer = ''

    def reify(self):
        if self.buffer[0].isdigit():
            return Token(TokenType.NUMBER, self.buffer, int(self.buffer))
        elif self.buffer == ';':
            return Token(TokenType.SEMICOLON, self.buffer)
        elif self.buffer == ':':
            return Token(TokenType.COLON, self.buffer)
        else:
            return Token(TokenType.SYMBOL, self.buffer)

    def consume(self):
        c = self.source[self.index]
        self.index += 1
        return c

    def has_next(self):
        return self.index < len(self.source)


if __name__ == "__main__":
    lexer = Lexer()
    tokens = lexer.lex('code.stack')
    print(tokens)
