# Assembler Project

## Overview
This repository contains an assembler implemented in Python, designed to convert assembly code into machine code. The assembler follows a two-pass process:
1. **First Pass**: Generates a symbol table and determines memory layout.
2. **Second Pass**: Translates the instructions into binary format and resolves labels.

## Files Included
- **Assembler.py**: The main Python script implementing the assembler.
- **Assembler.pdf**: A detailed report explaining the assembler's design, functionality, and implementation.
- **asm.txt** (expected input): The assembly code file to be processed.
- **Machine_Code.txt** (output): The generated machine code file.

## How It Works
1. The assembler reads the assembly code from `asm.txt`.
2. It processes the code in two passes:
   - The first pass builds a symbol table.
   - The second pass converts instructions into binary machine code.
3. The final machine code is written to `Machine_Code.txt`.

## Running the Assembler
To use the assembler, follow these steps:
1. Ensure that `asm.txt` contains the assembly code.
2. Run the Python script:
3. The machine code will be generated in `Machine_Code.txt`.

## Requirements
- Python 3.x

## Features
- Supports a predefined set of instructions for a basic computer architecture.
- Handles labels and memory references.
- Implements ORG and END directives for memory management.
- Converts decimal values into 16-bit binary format.
- Uses an object-oriented approach for better code organization.

## Author
- **Sara Basheer Mohamed**
- CSE 311: Computer Organization

## License
This project is for educational purposes and follows academic integrity guidelines.
