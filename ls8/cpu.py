"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.fl = 0

    def load(self):
        """Load a program into memory."""

        try:
            program = sys.argv[1]
        except:
            print("Provide the filepath to the program you want to run...")
            sys.exit(1)

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    #Access RAM
    def ram_read(self, mar):
        # mar = Memory Address Register (MAR) and the Memory Data Register (MDR).
        # The MAR contains the address that is being read or written to.
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        # mdr = Memory Data Register (MDR)
        # The MDR contains the data that was read or the data to write.
        self.ram[mar] = mdr

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        HLT  = 0b00000001 # Halt the CPU (and exit the emulator).
        LDI  = 0b10000010 # Set the value of a register to an integer.
        PRN  = 0b01000111 # Print numeric value stored in the given register.
        MUL  = 0b10100010 # Multiply the values in two registers together and store the result in registerA.
        running = True

        while running:
            # Initialize The Instruction Register
            # The next 2 values are stored just in case they are needed to perform an operation
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == PRN:
                print(self.reg[operand_a])
                self.pc += 2            
            elif ir == MUL:
                self.reg[operand_a] *= self.reg[operand_b]
                self.pc += 3
            elif ir == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif ir == HLT:
                running = False
                sys.exit(1)
