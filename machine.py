from lexer import Lexer
from my_parser import Instruction, Parser, InstructionType


class Machine:
    def __init__(self, program):
        self.program = program
        self.stack = []
        self.variables = {}
        self.ip = 0
        self.functions = {
            InstructionType.PUSH: self._push,
            InstructionType.POP: self._pop,
            InstructionType.PRINT: self._print,
            InstructionType.STORE: self._store,
            InstructionType.ASK: self._ask,
            InstructionType.DUP: self._dup,
            InstructionType.ADD: self._add,
            InstructionType.SUB: self._sub,
            InstructionType.MUL: self._mul,
            InstructionType.DIV: self._div,
            InstructionType.EQU: self._equ,
            InstructionType.LEQ: self._leq,
            InstructionType.JUMPT: self._jumpt,
            InstructionType.JUMPF: self._jumpf,
            InstructionType.JUMP: self._jump,
            InstructionType.STOP: self._stop,
            InstructionType.NOOP: self._noop,
        }
        self.running = True

    def run(self):
        while self.running:
            instr = self.get_instruction()
            if instr is None:
                break

            #print(f'$ - {instr}')
            func = self.functions[instr.type]
            advance = func(instr)
            if advance:
                self.ip += 1

    def get_instruction(self):
        if self.ip < len(self.program.instructions):
            return self.program.instructions[self.ip]
        else:
            return None
        
    def push(self, val):
        self.stack.append(val)

    def pop(self):
        if len(self.stack) == 0:
            raise Exception('Tried popping from empty stack')
        
        return self.stack.pop()
    
    def get_var(self, name):
        if name not in self.variables:
            raise Exception(f'Undefined variable: {name}')
        return self.variables[name]
    
    def set_var(self, name, val):
        self.variables[name] = val
        
    def jump_label(self, label):
        if label not in self.program.labels:
            raise Exception(f'Unknown label: {label}')
        self.ip = self.program.labels[label]

    def _push(self, instr: Instruction):
        val = instr.num
        if len(instr.var_or_label) > 0:
            val = self.get_var(instr.var_or_label)
        self.push(val)
        return True

    def _pop(self, instr: Instruction):
        self.pop()
        return True

    def _store(self, instr: Instruction):
        val = self.pop()
        self.set_var(instr.var_or_label, val)
        return True

    def _ask(self, instr: Instruction):
        val = int(input())
        self.push(val)
        return True

    def _dup(self, instr: Instruction):
        val = self.pop()
        self.push(val)
        self.push(val)
        return True

    def _add(self, instr: Instruction):
        a = self.pop()
        b = self.pop()
        self.push(a + b)
        return True
    
    def _sub(self, instr: Instruction):
        a = self.pop()
        b = self.pop()
        self.push(b - a)
        return True

    def _mul(self, instr: Instruction):
        a = self.pop()
        b = self.pop()
        self.push(a * b)
        return True

    def _div(self, instr: Instruction):
        a = self.pop()
        b = self.pop()
        self.push(b // a)
        return True

    def _equ(self, instr: Instruction):
        a = self.pop()
        b = self.pop()
        self.push(1 if b == a else 0)
        return True

    def _jumpt(self, instr: Instruction):
        val = self.pop()
        if val != 0:
            self.jump_label(instr.var_or_label)
            return False
        else:
            return True

    def _jumpf(self, instr: Instruction):
        val = self.pop()
        if val == 0:
            self.jump_label(instr.var_or_label)
            return False
        else:
            return True

    def _jump(self, instr: Instruction):
        self.jump_label(instr.var_or_label)
        return False
    
    def _noop(self, instr: Instruction):
        pass
        

    def _leq(self, instr: Instruction):
        a = self.pop()
        b = self.pop()
        self.push(1 if b <= a else 0)
        return True
        
    def _print(self, instr: Instruction):
        val = self.pop()
        print(val)
        return True
        
    def _stop(self, instr: Instruction):
        self.running = False
        return False

if __name__ == "__main__":
    lexer = Lexer()
    tokens = lexer.lex('code.stack')
    print(tokens)

    parser = Parser(tokens)
    program = parser.parse()
    
    machine = Machine(program)
    machine.run()
    
