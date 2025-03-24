class Assembler:

    def __init__(self):
        """
        Initializes the assembler with an empty symbol table and instructions mapping.
        Also initializes the location counter to track memory addresses.
        """
        self.symbol_table = {}
        self.location_counter = 0
        """" The following map (dictionary) will be  used during the second pass to get the binary code corresponding to a specific assembly instruction"""
        self.instructions = {
            # memory-reference instructions
            'AND': '0xxx',  # AND memory word to AC
            'ADD': '1xxx',  # Add memory word to AC
            'LDA': '2xxx',  # Load memory word to AC
            'STA': '3xxx',  # Store content of AC in memory
            'BUN': '4xxx',  # Branch unconditionally
            'BSA': '5xxx',  # Branch and save return address
            'ISZ': '6xxx',  # Increment and skip if zero

            # register-reference instructions
            'CLA': '7800',  # Clear AC
            'CLE': '7400',  # Clear E
            'CMA': '7200',  # Complement AC
            'CME': '7100',  # Complement E
            'CIR': '7080',  # Circulate right AC and E
            'CIL': '7040',  # Circulate left AC and E
            'INC': '7020',  # Increment AC
            'SPA': '7010',  # Skip next instruction if AC positive
            'SNA': '7008',  # Skip next instruction if AC negative
            'SZA': '7004',  # Skip next instruction if AC zero
            'SZE': '7002',  # Skip next instruction if E is 0
            'HLT': '7001',  # Halt computer

            # input/output instructions
            'INP': 'F800',  # Input character to AC
            'OUT': 'F400',  # Output character from AC
            'SKI': 'F200',  # Skip on input flag
            'SKO': 'F100',  # Skip on output flag
            'ION': 'F080',  # Interrupt on
            'IOF': 'F040',  # Interrupt off
        }

    def first_pass(self, code):
        """
        First pass: Scan the code to build the symbol table.
        The symbol table maps labels to their respective memory addresses.
        """
        for line in code.split('\n'):
            line = line.strip()
            if not line or line.startswith('/'):  # discard comments of the assembly code
                continue

            parts = line.split('/')
            instruction = parts[0].strip()

            if instruction.startswith('ORG'):
                self.location_counter = int(instruction.split()[1],
                                            16)  # initialize the location counter with the number after ORG
                continue

            if instruction == 'END':
                break

            if ',' in instruction:  # , specifies that the following text is a label
                label = instruction.split(',')[0].strip()
                self.symbol_table[label] = format(self.location_counter, '012b')

            self.location_counter += 1

    def convert_decimal(self, value):
        num = int(value)
        if num < 0:
            # Convert negative numbers to 16-bit binary (two's complement)
            num = (1 << 16) + num
        return format(num, '016b')

    def second_pass(self, code):
        """
        Second pass: Generate binary machine code by translating each instruction
        and resolving label addresses using the symbol table.
        """
        binary_code = []  # Initialize an empty list to store the binary instructions
        self.location_counter = 0  # Reset the location counter to 0

        for line_number, line in enumerate(code.split('\n'), start=1):
            line = line.strip()  # Remove leading/trailing whitespace
            if not line or line.startswith('/'):  # Skip empty lines and comments
                continue

            # Split the line to separate the instruction from any inline comments
            parts = line.split('/')
            instruction = parts[0].strip()  # Extract the actual instruction ( and discard the comment)

            # Check if the line contains the ORG directive
            if instruction.startswith('ORG'):
                # Update the location counter to the specified hexadecimal address (found after ORG)
                self.location_counter = int(instruction.split()[1], 16)
                continue

            if instruction == 'END':
                break

            if ',' in instruction:
                parts = instruction.split(',')
                if 'DEC' in parts[1]:  # Check if the line contains the DEC pseudo instruction
                    value = parts[1].replace('DEC', '').strip()  # Extract the value
                    binary = self.convert_decimal(value)  # Convert the decimal value to 16-bit binary
                    binary_code.append((format(self.location_counter, '012b'), binary))
            else:
                # actual instructions (opcodes)
                parts = instruction.split()  # Split the instruction into its components
                opcode = self.instructions.get(
                    parts[0])  # Look up the opcode in the instruction dictionary declared in the construction method
                if opcode:
                    # Convert the opcode's first hex digit to 4 bits
                    opcode_binary = format(int(opcode[0], 16), '04b')
                    address = '000000000000'  # Default 12-bit address for non-memory instructions (register-reference and i/o instructions)
                    if len(parts) > 1:  # If there's an operand (e.g., a label or value)
                        operand = parts[1]  # Extract the operand
                        if operand.startswith('I'):  # Check for indirect addressing
                            # Use the second hex digit of the opcode for indirect addressing
                            opcode_binary = format(int(opcode[1], 16), '04b')
                            operand = operand[1:]  # Remove the 'I' character from the operand
                        address = self.symbol_table.get(operand, '000000000000')
                    binary = opcode_binary + address          # Finally, the binary code for this instruction is ready
                    binary_code.append((format(self.location_counter, '012b'), binary))

            self.location_counter += 1

        return binary_code


def assemble(code):
    """
    Assembles the given assembly code into binary machine code.
    Performs two passes: the first to build the symbol table and the second to generate binary.
    """
    assembler = Assembler()
    assembler.first_pass(code)
    binary = assembler.second_pass(code)
    return binary


def main():
    try:
        # Read the assembly code from "asm.txt"
        with open("asm.txt", 'r') as input_file:
            assembly_code = input_file.read()

        # Assemble the code
        result = assemble(assembly_code)

        # Write the resulting binary code to "Machine_Code.txt"
        with open("Machine_Code.txt", 'w') as output_file:
            for address, binary in result:
                output_file.write(f"{address}  {binary}\n")

        print("Assembly successfully converted to machine code. Output written to 'Machine_Code.txt'.")

    except FileNotFoundError:
        print("Error: The file 'asm.txt' was not found.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":  # checks if the script is being run directly, not imported as a module.
    main()  # Calls the main function to execute the main logic of the script if it's being run directly.

