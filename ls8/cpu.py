"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8
        # self.ir = {
        #     0b10000010: 'LDI',
        #     0b01000111: 'PRN',
        #     0b00000001: 'HLT'
        # }
        # self.ir = {
        #     'LDI': 0b10000010,
        #     'PRN': 0b01000111,
        #     'HLT': 0b00000001
        # }

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
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

    def ldi(self, register, value):
        self.reg[register] = value

    def prn(self, index):
        print(self.reg[index])

    def hlt(self):
        sys.exit(0)

    def run(self):
        """Run the CPU."""
        # number of operands = inst value & 0b11000000 >> 6
        # inst length = number of operands + 1
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        running = True
        # self.trace()
        while running is True:
            inst_reg = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)
            if inst_reg == LDI:
                # print('LDI')
                # self.reg[operand_a] = operand_b
                self.ldi(operand_a, operand_b)
                self.pc += 3
            elif inst_reg == PRN:
                self.prn(operand_a)
                self.pc += 2
            elif inst_reg == HLT:
                self.hlt()
                self.pc += 1
                running = False

        # print(self.ir['LDI'])
