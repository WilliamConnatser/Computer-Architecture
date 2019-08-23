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
        self.heap = 0

    def load(self):
        """Load a program into memory."""
        #Get filepath as a parameter
        try:
            filepath = sys.argv[1]
        except:
            print("Provide the filepath to the program you want to run...")
            sys.exit(1)

        # Read the source code
        source_code = open(filepath, 'r')
        line = source_code.readline()
        address = 0
        while line:
            # Filter out empty lines and lines which only contain comments
            if len(line.strip()) != 0 and not line.strip().startswith("#"):
                #Filter out in-line comments
                if "#" in line:
                    line = line[:line.index("#")]
                self.ram_write(address,line)
                address += 1
                self.heap += 1
            line = source_code.readline()

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

        # Convert binary string to int
        try:
            return int(self.ram[mar],2)
        except:
            return 0

    def ram_write(self, mar, mdr):
        # mdr = Memory Data Register (MDR)
        # The MDR contains the data that was read or the data to write.
        self.ram[mar] = mdr

    def push(self,value):
        self.reg[7] -= 1
        ram_loc = 0xF4 - self.reg[7]
        # If application instructions are stored in this ram location
        # Then a stack overflow has ocurred
        if self.ram[ram_loc] != 0:
            print("Stack Overflow..")
            sys.exit(1)
        else:
            self.ram[ram_loc] = value

    def pop(self):
        # If R7 is 0 then the stack is empty
        if self.reg[7] < 0:
            ram_loc = 0xF4 - self.reg[7]
            return_value = self.ram[ram_loc]
            self.ram[ram_loc] = 0
            self.reg[7] += 1
        else:
            return_value = None        
        return return_value

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
        ADD = 0b10100000 # Add the value in two registers and store the result in registerA.
        HLT  = 0b00000001 # Halt the CPU (and exit the emulator).
        LDI  = 0b10000010 # Set the value of a register to an integer.
        PRN  = 0b01000111 # Print numeric value stored in the given register.
        MUL  = 0b10100010 # Multiply the values in two registers together and store the result in registerA.
        PUSH = 0b01000101 # Push the value in the given register on the stack.
        POP = 0b01000110 # Pop the value at the top of the stack into the given register.
        CALL = 0b01010000 # Calls a subroutine (function) at the address stored in the register.
        RET = 0b00010001 # Pop the value from the top of the stack and store it in the PC.
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
            elif ir == ADD:
                self.reg[operand_a] += self.reg[operand_b]
                self.pc += 3       
            elif ir == MUL:
                self.reg[operand_a] *= self.reg[operand_b]
                self.pc += 3
            elif ir == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif ir == PUSH:
                self.push(self.reg[operand_a])
                self.pc += 2
            elif ir == POP:
                self.reg[operand_a] = self.pop()
                self.pc += 2
            elif ir == CALL:
                self.push(self.pc+2)
                self.pc = self.reg[operand_a]
            elif ir == RET:
                self.pc = self.pop()
            elif ir == HLT:
                running = False
                sys.exit(1)
