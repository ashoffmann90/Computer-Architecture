"""CPU functionality."""

import sys
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.ir = {
            'LDI': 0b10000010,
            'PRN': 0b01000111,
            'HLT': 0b00000001
        }
        self.branchtable = {}
        self.branchtable[HLT] = self.hlt
        self.branchtable[LDI] = self.ldi
        self.branchtable[PRN] = self.prn

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        # open file
        # print(sys.argv)
        # with open(sys.argv[1]) as f:
        #     for line in f:
        #         try:
        #             line2 = line.split('#')[0].strip()
        #             if line2 == '':
        #                 continue
        #         except ValueError:
        #             pass

        #         line3 = int(line2, 2)
        #         self.ram[address] = line3
        #         address += 1

        # For now, we've just hardcoded a program:

        program = '''
        # Print the number 8

        # This comment and blank line is here to make sure
        # they are handled correctly by the file reading        code.

        10000010 # LDI R0,8
        00000000
        00001000
        01000111 # PRN R0
        00000000
        00000001 # HLT
        '''
        # print(program)
        # print(program.split('\n'))
        split = program.split('\n')
        cleaned = []
        for line in filename:
            line1 = line.strip()
            if not line1.startswith('#') and line1.strip():
                line2 = line1.split('#', 1)[0]
                cleaned.append(int(line2, 2))
                print(line2)

        # for line in program:
        #     try:
        #         line2 = line.split('#')[0].strip()
        #         if line2 == '':
        #             continue
        #     except ValueError:
        #         pass
        #     line3 = int(line2, 2)
        #     self.ram[address] = line3
        #     address += 1
        # program = [
        #     # # From print8.ls8
        #     # 0b10000010,  # LDI R0,8
        #     # 0b00000000,
        #     # 0b00001000,
        #     # 0b01000111,  # PRN R0
        #     # 0b00000000,
        #     # 0b00000001,  # HLT

        # ]

        for instruction in cleaned:
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
        self.pc += 3

    def prn(self, register, x):
        print(self.reg[register])
        self.pc += 2

    def hlt(self, x, y):
        sys.exit(0)
        self.pc += 1

    def run(self):
        """Run the CPU."""
        # number of operands = inst value & 0b11000000 >> 6
        # inst length = number of operands + 1
        # LDI = 0b10000010
        # PRN = 0b01000111
        # HLT = 0b00000001

        running = True
        # self.trace()
        while running is True:
            inst_reg = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)
            if inst_reg in self.branchtable:
                self.branchtable[inst_reg](operand_a, operand_b)

        # print(self.ir['LDI'])
