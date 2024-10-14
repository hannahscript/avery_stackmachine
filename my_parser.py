from dataclasses import dataclass
from enum import Enum

from lexer import Token, TokenType, Lexer


class InstructionType(Enum):
    PRINT = 'print'
    PUSH = 'push'
    POP = 'pop'
    STORE = 'store'
    ASK = 'ask'
    DUP = 'dup'
    ADD = 'add'
    SUB = 'sub'
    MUL = 'mul'
    DIV = 'div'
    EQU = 'equ'
    LEQ = 'leq'
    JUMPT = 'jumpt'
    JUMPF = 'jumpf'
    JUMP = 'jump'
    STOP = 'stop'
    NOOP = 'noop'


@dataclass
class Instruction:
    type: InstructionType
    var_or_label: str
    num: int = -1

    def __repr__(self):
        if len(self.var_or_label) > 0:
            return f'{self.type}({self.var_or_label})'
        elif self.type == InstructionType.PUSH:
            return f'{self.type}(#{self.num})'
        else:
            return str(self.type)


@dataclass
class Program:
    instructions: list[Instruction]
    labels: dict[str, int]


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.instructions = []
        self.labels = {}

    def parse(self):
        while self.has_next():
            self.labeled_instr()

        return Program(self.instructions, self.labels)

    def labeled_instr(self):
        token = self.consume()
        if self.peek().type == TokenType.COLON:
            self.consume()
            self.labels[token.literal] = len(self.instructions)
            token = self.consume()
        self.instructions.append(self.instr(token))

    def instr(self, token):
        try:
            instr_type = InstructionType(token.literal)
            result: Instruction
            if instr_type == InstructionType.PUSH:
                token = self.consume()
                result = Instruction(instr_type, '', token.value) if token.type == TokenType.NUMBER else Instruction(
                    instr_type, token.literal)
            elif instr_type in [InstructionType.STORE, InstructionType.JUMP, InstructionType.JUMPF,
                                InstructionType.JUMPT]:
                var = self.var_or_label()
                result = Instruction(instr_type, var)
            else:
                result = Instruction(instr_type, '')

            self.expect(TokenType.SEMICOLON)
            return result
        except ValueError:
            raise Exception(f'Unknown instruction type: {token.literal}')

    def var_or_label(self):
        token = self.consume()
        # todo verify variable name is good
        return token.literal

    def has_next(self):
        return self.index < len(self.tokens)

    def expect(self, token_type):
        t = self.consume()
        if t.type != token_type:
            raise Exception(f'Unexpected token: {t}')
        return t

    def consume(self):
        if not self.has_next():
            return Token(TokenType.EOF, '')

        token = self.tokens[self.index]
        self.index += 1
        return token

    def peek(self):
        if not self.has_next():
            return Token(TokenType.EOF, '')

        return self.tokens[self.index]


if __name__ == "__main__":
    lexer = Lexer()
    tokens = lexer.lex('code.stack')
    print(tokens)

    parser = Parser(tokens)
    parser.parse()
