# CS-2450-project

The program is a simple CPU simulator written in Python that reads commands from a text file, loads them into memory, and executes them one at a time. The CPU supports commands for reading and writing values, loading and storing memory, basic math operations, branching, and halting the program.

# Steps for Running the Program

1. Run the main Python file:

`python main.py`

2. The program will ask for the path to a text file containing the commands you want the CPU to run.

Example:

`Testing_files/testfile.txt`

You can enter a relative file path like the example above if the file is located within the project. You can also enter the full path to the file on your computer.

3. The program will read the file, validate the commands, load them into memory, and begin executing them.

If the file path does not exist, the program will display an error instead of trying to run the file.

If the file exists but contains an invalid command, the program will display an error explaining that the file contains invalid instructions. Invalid files can include commands that are too long or too short, blank lines, invalid characters, or commands that do not follow the required format.

# Command Format

Each command in the input file should follow the `+/-####` format.

The first character is either `+` or `-`, followed by four digits.

Example:

`+2010`

The first two digits represent the operation code and the last two digits represent the memory location used by the command.

# Supported Commands

The CPU currently supports the following commands:

- `10` - READ: Asks the user to enter a value and stores it in the specified memory location.
- `11` - WRITE: Displays the value stored in the specified memory location.
- `20` - LOAD: Loads a value from memory into the accumulator.
- `21` - STORE: Stores the current accumulator value into a memory location.
- `30` - ADD: Adds a value from memory to the accumulator.
- `31` - SUBTRACT: Subtracts a value in memory from the accumulator.
- `32` - DIVIDE: Divides the accumulator by a value stored in memory.
- `33` - MULTIPLY: Multiplies the accumulator by a value stored in memory.
- `40` - BRANCH: Moves execution to a specified memory location.
- `41` - BRANCHNEG: Moves execution to a specified memory location if the accumulator is negative.
- `42` - BRANCHZERO: Moves execution to a specified memory location if the accumulator is zero.
- `43` - HALT: Stops the program.

# READ Input

When the CPU reaches a READ command, it will ask the user to enter a number.

Positive numbers can be entered without manually adding a `+` sign.

Example:

`1234`

Negative numbers should include the `-` sign.

Example:

`-1234`

The value must contain no more than four digits. The CPU will store positive values using the `+####` format internally.

# WRITE Output

When the CPU reaches a WRITE command, it retrieves the value from the specified memory location and displays it to the user.

For example, if the specified memory location contains `+1234`, the program will output:

`+1234`

# Math and Overflow

The CPU uses four-digit values. If a math operation creates a value larger than four digits, the extra leading digits are truncated so the CPU can continue operating with a four-digit value.

For example:

`12345` becomes `2345`

The same four-digit limitation is applied to negative results.

# Errors

The program checks for errors before and while executing commands.

Some errors that may occur include:

- The file path does not exist.
- The file contains an invalid command.
- A command contains invalid characters.
- A command is too long or too short.
- The file contains a blank or improperly formatted line.
- The program attempts to access an invalid memory location.
- A DIVIDE command attempts to divide by zero.
- A READ value is not in the accepted format.

If an error occurs, the program will display an error message describing the problem.

# Pytest Testing

We are using pytest for testing. The project includes unit tests for file validation, memory initialization, reading and writing values, loading and storing memory, math operations, branching, and halting.

To run the tests:

`pytest`

# Group Members

Trevor, Nate, Enoch, and Kiara