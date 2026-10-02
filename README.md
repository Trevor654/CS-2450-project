# CS-2450 Project - UVSim

UVSim is a simple CPU simulator written in Python. The program reads UVSim instructions from a text file, loads them into memory, and executes the instructions one at a time.

The simulator supports input and output, loading and storing values, arithmetic operations, branching, and halting. The project also includes a Tkinter graphical user interface for selecting a program file and running the simulator.

## Requirements

- Python 3
- Tkinter
- pytest (only required for running the unit tests)

Tkinter is included with most standard Python installations, so no additional GUI package is normally required.

## Running the Program

Run the main Python file:

`python main.py`

The program opens the Tkinter GUI. From the GUI:

1. Click **Open File**.
2. Select a `.txt` file containing UVSim instructions.
3. The selected file is used to create the CPU and load the program into memory.
4. On the program screen, click **Run** to execute the loaded instructions.
5. Use **Go back** to return to the first screen.

The current GUI also contains an input field and Enter button for continued input handling.

## Program File Format

UVSim programs are stored in text files. Each instruction must follow the format:

`+####` or `-####`

For example:

`+2010`

In `+2010`, `20` is the operation code and `10` is the memory address used by the operation.

The CPU contains 100 memory locations, numbered `00` through `99`. Program instructions are loaded into memory starting at location `00`. Unused memory locations are initialized to `+0000`.

## Supported Commands

The CPU currently supports the following commands:

- `10` - READ: Reads a value from the user and stores it in the specified memory location.
- `11` - WRITE: Displays the value stored in the specified memory location.
- `20` - LOAD: Loads a value from memory into the accumulator.
- `21` - STORE: Stores the current accumulator value in a memory location.
- `30` - ADD: Adds a value from memory to the accumulator.
- `31` - SUBTRACT: Subtracts a value in memory from the accumulator.
- `32` - DIVIDE: Divides the accumulator by a value stored in memory.
- `33` - MULTIPLY: Multiplies the accumulator by a value stored in memory.
- `40` - BRANCH: Moves execution to a specified memory location.
- `41` - BRANCHNEG: Moves execution to a specified memory location if the accumulator is negative.
- `42` - BRANCHZERO: Moves execution to a specified memory location if the accumulator is zero.
- `43` - HALT: Stops the program.

## READ Input

When the CPU reaches a READ command, it asks the user to enter a value.

The current accepted format is:

`+####` or `-####`

Examples:

`+1234`

`-1234`

The input must contain exactly five characters: a `+` or `-` sign followed by four digits.

If the input does not match this format, the program displays `Invalid input.` and asks the user to enter another value.

## WRITE Output

When the CPU reaches a WRITE command, it retrieves the value stored at the specified memory location and displays it.

For example, if the specified memory location contains:

`+1234`

The program will output:

`+1234`

## Math and Overflow

The CPU uses signed four-digit values.

The ADD, SUBTRACT, MULTIPLY, and DIVIDE operations perform calculations using the accumulator and values stored in memory.

If a math operation creates a value larger than four digits, the extra leading digits are truncated so the CPU can continue operating with a four-digit value.

For example:

`12345` becomes `+2345`

The same four-digit limitation is applied to negative results while preserving the negative sign.

The DIVIDE operation also checks for division by zero. Attempting to divide by zero will result in an error.

## Program Structure

The simulator is divided into several classes so that different parts of the program have separate responsibilities.

### CPU

The `CPU` class manages the simulator's memory, accumulator, instruction loading, and program execution. It reads each instruction and sends the operation to the appropriate unit.

### CommunicationUnit

The `CommunicationUnit` handles the following commands:

- READ
- WRITE

It uses the CPU's memory to store user input and retrieve values for output.

### ArithmeticUnit

The `ArithmeticUnit` handles the following commands:

- ADD
- SUBTRACT
- DIVIDE
- MULTIPLY

It performs calculations using the CPU's accumulator and memory.

### ControlUnit

The `ControlUnit` handles the following commands:

- LOAD
- STORE
- BRANCH
- BRANCHNEG
- BRANCHZERO
- HALT

It handles loading and storing values as well as controlling the execution flow of the program.

### Gui

The `Gui` class provides the graphical user interface using Tkinter. It handles file selection, screen navigation, starting CPU execution, displaying output and errors, and the GUI input controls.

## Error Handling

The program checks for errors when loading and executing a program.

Some errors that may occur include:

- The selected file does not exist or the filepath is invalid.
- The file contains an invalid command.
- An instruction is too long or too short.
- An instruction does not begin with `+` or `-`.
- An instruction contains invalid characters.
- The program attempts to access an invalid memory location.
- A DIVIDE operation attempts to divide by zero.
- A READ value does not use the required `+####` or `-####` format.

A missing or invalid filepath raises a `FileNotFoundError`.

Invalid instructions inside an existing file raise a `ValueError` identifying the invalid command.

## Testing

The project uses pytest for unit testing.

To run the tests:

`pytest`

The project includes tests covering:

- File validation
- Memory initialization
- READ and WRITE
- LOAD and STORE
- Arithmetic operations
- Arithmetic overflow
- Branching
- Halting

## Group Members

Trevor, Nate, Enoch, and Kiara