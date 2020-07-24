"""CPU functionality."""

import sys
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
AND = 0b10101000
OR = 0b10101010
XOR = 0b10101011
NOT = 0b01101001
SHL = 0b10101100
SHR = 0b10101101
MOD = 0b10100100


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.set_pc = False
        self.reg[7] = 0xf4
        self.sp = self.reg[7]
        self.fl = None
        self.ir = {
            'LDI': 0b10000010,
            'PRN': 0b01000111,
            'HLT': 0b00000001,
            'MUL': 0b10100010,
            'CALL': 0b01010000,
            'RET': 0b00010001,
            'PUSH': 0b01000101,
            'POP': 0b01000110,
            'CALL': 0b01010000,
            'RET': 0b00010001,
            'ADD': 0b10100000,
            'CMP': 0b10100111,
            'JMP': 0b01010100,
            'JEQ': 0b01010101,
            'JNE': 0b01010110,
            'AND': 0b10101000,
            'OR': 0b10101010,
            'XOR': 0b10101011,
            'NOT': 0b01101001,
            'SHL': 0b10101100,
            'SHR': 0b10101101,
            'MOD': 0b10100100
        }
        self.branchtable = {}
        self.branchtable[HLT] = self.hlt
        self.branchtable[LDI] = self.ldi
        self.branchtable[PRN] = self.prn
        self.branchtable[MUL] = self.mul
        self.branchtable[PUSH] = self.push
        self.branchtable[POP] = self.pop
        self.branchtable[ADD] = self.add
        self.branchtable[CALL] = self.call
        self.branchtable[RET] = self.ret
        self.branchtable[CMP] = self.cmp
        self.branchtable[JMP] = self.jmp
        self.branchtable[JEQ] = self.jeq
        self.branchtable[JNE] = self.jne
        self.branchtable[AND] = self.and_op
        self.branchtable[OR] = self.or_op
        self.branchtable[XOR] = self.xor_op
        self.branchtable[NOT] = self.not_op
        self.branchtable[SHL] = self.shl_op
        self.branchtable[SHR] = self.shr_op
        self.branchtable[MOD] = self.mod_op

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        cleaned = []
        for line in filename:
            line1 = line.strip()
            if not line1.startswith('#') and line1.strip():
                line2 = line1.split('#', 1)[0]
                cleaned.append(int(line2, 2))
                # print(line2)

        for instruction in cleaned:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == 'MUL':
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
        elif op == 'CMP':
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 'E'
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 'G'
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 'L'
            else:
                self.fl = 0
        elif op == 'AND':
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
        elif op == 'OR':
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        elif op == 'XOR':
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
        elif op == 'NOT':
            self.reg[reg_a] = ~self.reg[reg_a]
        elif op == 'SHL':
            self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
        elif op == 'SHR':
            self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]
        elif op == 'MOD':
            if self.reg[reg_b] != 0:
                self.reg[reg_a] = self.reg[reg_a] // self.reg[reg_b]
            else:
                print('Second input cannot be 0')
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    # ALU OPS

    def cmp(self, a, b):
        self.alu('CMP', a, b)

    def mul(self, a, b):
        self.alu('MUL', a, b)
        # self.pc += 3

    def add(self, a, b):
        self.alu('ADD', a, b)

    def and_op(self, a, b):
        self.alu('AND', a, b)

    def or_op(self, a, b):
        self.alu('OR', a, b)

    def xor_op(self, a, b):
        self.alu('XOR', a, b)

    def not_op(self, a, b):
        self.alu('NOT', a, b)

    def shl_op(self, a, b):
        self.alu('SHL', a, b)

    def shr_op(self, a, b):
        self.alu('SHR', a, b)

    def mod_op(self, a, b):
        self.alu('MOD', a, b)

    # CPU OPS

    def jmp(self, x, y):
        self.pc = self.reg[x]

    def jeq(self, x, y):
        if self.fl == 'E':
            self.pc = self.reg[x]
        else:
            self.pc += 2

    def jne(self, x, y):
        if self.fl != 'E':
            self.pc = self.reg[x]
        else:
            self.pc += 2

    def ldi(self, register, value):
        self.reg[register] = value
        # self.pc += 3

    def prn(self, register, x):
        print(self.reg[register])
        # self.pc += 2

    def hlt(self, x, y):
        sys.exit(0)
        # self.pc += 1

    def call(self, x, y):
        # get address of NEXT instruction
        return_address = self.pc + 2

        self.sp -= 1
        self.ram_write(self.sp, return_address)

        # set PC to subroutine address
        reg_val = self.ram[self.pc + 1]
        subroutine_address = self.reg[reg_val]

        self.pc = subroutine_address

    def ret(self, x, y):
        # pop_address = self.reg[self.sp]
        return_address = self.ram_read(self.sp)
        self.sp += 1

        self.pc = return_address

    def push(self, operand_a, operand_b):
        self.sp -= 1
        # self.reg[self.sp] &= 0xff
        val = self.reg[operand_a]
        self.ram_write(self.sp, val)
        # self.pc += 2

    def pop(self, operand_a, operand_b):
        self.reg[operand_a] = self.ram_read(self.sp)
        # self.pc += 2
        self.sp += 1

    def run(self):
        """Run the CPU."""
        running = True
        # self.trace()
        while running is True:
            # self.trace()
            inst_reg = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)

            # print('inst_reg: ', inst_reg)
            for k, v in self.ir.items():
                # print('v', v)
                if inst_reg == v:
                    # print('something')
                    inst = bin(v)
                    # print('inst: ', inst)
            inst_size = ((inst_reg >> 6) & 0b11) + 1
            self.set_pc = ((inst_reg >> 4) & 0b1) == 1
            # If the instruction didn't set the PC, just move to the next instruction
            if not self.set_pc:
                # could replace inst_size with op if using the commented out lines
                self.pc += inst_size

            if inst_reg in self.branchtable:
                self.branchtable[inst_reg](operand_a, operand_b)

        # print(self.ir['LDI'])
