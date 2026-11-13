from gui import Gui
from functions import *

class CPU:

    ###  ------ CPU Initialization ------ ###

    def __init__(self, filename: str, gui: Gui = None):
        self.gui = gui          # The GUI for the CPU

        self.maxFileSize = 250
        self.memory = {}                                # Main memory dictionary
        self._fileFormat = 'six-digit'                  # Format for the input file (default = 'six-digit' format, the other option is 'four-digit')
        self._fileHandler = FileHandler(self)           ## File Handler Object that handles file checking.
        self._fileHandler.loadDataFromFile(filename)    ## Throws errors depending if the file is not found or is malformed. Also changes the code to 4 digit if that's what the user inputs.

        # Other variables
        self._accumulator = '+000000' if self._fileFormat == 'six-digit' else '+0000'
        self._communicationUnit = CommunicationUnit(self)
        self._arithmeticUnit = ArithmeticUnit(self)
        self._controlUnit = ControlUnit(self)
        
    ###  ------ CPU Methods ------ ###

    ## Public Methods ##
    def output(self, message):
        if self.gui is not None:
            self.gui.print_output(message)
        else:
            print(message)

    def run(self, pointer=0, gui_input=''):
        halted = False
        need_input = False
        print_val = None

        while not halted:
            if pointer >= self.maxFileSize:
                raise ValueError(f"Program ran past address {self.maxFileSize - 1} without a HALT command")
            fullCommandString = self.memory[pointer]      # This goes through the commands one by one
            command = fullCommandString[1:4] if self._fileFormat == "six-digit" else fullCommandString[1:3]             # The command in from '+####' or '+######'. 
            value = fullCommandString[4:7] if self._fileFormat == "six-digit" else fullCommandString[3:5]               # The last two or three numbers of the command, AKA the value of the command

            commandCheck = command
            if self._fileFormat == "four-digit":
                commandCheck = "0" + commandCheck

            if commandCheck in ['010','011','020','021','030','031','032','033','040','041','042'] and int(value) >= self.maxFileSize:
                raise ValueError(f"Invalid address {value} at line {pointer:03d} ({fullCommandString}). Addresses must be between 000 and {self.maxFileSize - 1}")

            match commandCheck:
                case '010':
                    got_input = self._communicationUnit.READ(value,gui_input)
                    if got_input == True:
                        need_input = False
                        pointer += 1
                        return (halted, pointer, need_input, print_val)
                    else:
                        if (self._fileFormat == "six-digit"):
                            print_val = "Please Enter a value in this format: +/-000000: "
                        elif (self._fileFormat == "four-digit"):
                            print_val = "Please Enter a value in this format: +/-0000: "
                        need_input = True
                        return (halted, pointer, need_input, print_val)

                case '011':
                    self._communicationUnit.WRITE(value)
                    
                case '020':
                    self._controlUnit.LOAD(value)

                case '021':
                    self._controlUnit.STORE(value)

                case '030':
                    self._arithmeticUnit.ADD(value)

                case '031':
                    self._arithmeticUnit.SUBTRACT(value)

                case '032':
                    self._arithmeticUnit.DIVIDE(value)

                case '033':
                    self._arithmeticUnit.MULTIPLY(value)

                case '040':
                    pointer = self._controlUnit.BRANCH(value)

                case '041':
                    branch_val = self._controlUnit.BRANCHNEG(value)
                    if type(branch_val) == int:
                        pointer = branch_val

                case '042':

                    branch_val = self._controlUnit.BRANCHZERO(value)
                    if type(branch_val) == int:
                        pointer = branch_val

                case '043':
                    halted = self._controlUnit.HALT(commandCheck)

                case _:
                    raise ValueError("Command '" + command + "' is not a valid command")

            pointer += 1
            return (halted, pointer, need_input, print_val)

###---------------------- SUBCLASSES ----------------------###

class FileHandler:
    def __init__(self, cpu):
        self.cpu = cpu

    def loadDataFromFile(self, filename):
        # If the filename doesn't exist, throw an error. If it does, edit the memory 
        try:
            file = open(filename, 'r')
            filecontent = file.read()
            commands = filecontent.split('\n')
        except:
            raise FileNotFoundError("File '" + filename + "' does not exist or the filepath is invalid")

        while len(commands) > 1 and commands[-1].strip() == '':
            commands.pop()

        # See what the file format is and change it to 'four-digit' if the user inputs a 4-digit command
        defaultCommand = '+000000'
        if len(commands) > 0:
            if len(commands[0]) == 5:
                self.cpu._fileFormat = "four-digit"
                defaultCommand = '+0000'

        # Load in the default memory slots
        for i in range(self.cpu.maxFileSize):
            self.cpu.memory[i] = defaultCommand

        # Memory only has 250 spots (000 - 249), so the file can't have more than 250 lines
        if len(commands) > self.cpu.maxFileSize:
            raise ValueError(f"File is over the max size of {self.cpu.maxFileSize} entries")

        expectedLength = 7 if self.cpu._fileFormat == "six-digit" else 5
        for i in range(len(commands)):
            if len(commands[i]) in [5, 7] and len(commands[i]) != expectedLength:
                raise ValueError(f"File mixes four-digit and six-digit words (line {i + 1}: {commands[i]}). A file must use only one format")

        # Loading in the commands from the file into the dictionary
        validCommands = ['010','011','020','021','030','031','032','033','040','041','042','043']
        validateInputSigned = checkValidInput7chars if self.cpu._fileFormat == "six-digit" else checkValidInput5chars
        halted = False
        for i in range(len(commands)):
            command = commands[i][1:4] if self.cpu._fileFormat == "six-digit" else "0" + commands[i][1:3]
            # If there has already been a halt command, the user can input whatever values they like, as long as they fit the '+/- ####' format
            if halted:
                if (validateInputSigned(commands[i]) == False):
                    errors = []
                    for k in range(i,len(commands)):
                        if validateInputSigned(commands[k]) == False:
                            errors.append(commands[k])
                    errorString = "Invalid command(s) in the given file: "
                    errorStringList = ", ".join(errors)
                    errorString += errorStringList
                    raise ValueError(errorString)
                self.cpu.memory[i] = commands[i]
            else:
                # First make sure that each command is valid. If there are any invalid commands, raise an error
                if ((validateInputSigned(commands[i]) == False) or (command not in validCommands)):
                    errors = []
                    for k in range(i,len(commands)):
                        if validateInputSigned(commands[k]) == False:
                            errors.append(commands[k])
                    errorString = "Invalid command(s) in the given file: "
                    errorStringList = ", ".join(errors)
                    errorString += errorStringList
                    raise ValueError(errorString)
                if self.cpu._fileFormat == "six-digit" and command != '043' and int(commands[i][4:7]) >= self.cpu.maxFileSize:
                    raise ValueError(f"Invalid address in the given file (line {i + 1}: {commands[i]}). Addresses must be between 000 and {self.cpu.maxFileSize - 1}")
                # Command Valid, continue
                self.cpu.memory[i] = commands[i]
                if command == '043':
                    halted = True

class CommunicationUnit:

    def __init__(self, cpu):
        self.cpu = cpu
        
    def READ(self, address, input_val='No Gui'):

        validateInputSigned = checkValidInput7chars if self.cpu._fileFormat == "six-digit" else checkValidInput5chars
        validateInputUnsigned = checkValidInput6chars if self.cpu._fileFormat == "six-digit" else checkValidInput4chars
            
        if input_val == 'No Gui':
            while True:
                user_input = ""

                if self.cpu._fileFormat == "six-digit":
                    user_input = input("Enter a value (format +/-######): ")
                    user_input = convertNumToCommand(user_input, self.cpu._fileFormat)
                    
                elif self.cpu._fileFormat == "four-digit":
                    user_input = input("Enter a value (format +/-####): ")
                    user_input = convertNumToCommand(user_input, self.cpu._fileFormat)

                if validateInputSigned(user_input):
                    self.cpu.memory[int(address)] = user_input
                    break
                elif validateInputUnsigned(user_input):
                    self.cpu.memory[int(address)] = ('+' + user_input)
                    break
                print("Invalid input.")
        else:
            user_input = input_val
            if validateInputSigned(user_input):
                self.cpu.memory[int(address)] = user_input
                return True
            elif validateInputUnsigned(user_input):
                self.cpu.memory[int(address)] = ('+' + user_input)
                return True
            return False
    
    def WRITE(self, address):
        value = self.cpu.memory[int(address)]
        self.cpu.output(value)

class ArithmeticUnit:

    def __init__(self, cpu):
        self.cpu = cpu

    #adds value in memory to the accumulator & then stores it
    #oh and mem_value is memory value and acc_value is the accumulator value :) 
    def ADD(self, address):
        mem_value = int(self.cpu.memory[int(address)])
        acc_value = int(self.cpu._accumulator)
        result = acc_value + mem_value

        overflow_limit = 1000000 if self.cpu._fileFormat == "six-digit" else 10000
        overflow_result = abs(result) % overflow_limit

        # For testing
        # print(f"address: {address}\nmem_val: {mem_value}\nacc_val: {acc_value}\nresult: {result}\noverflow_result: {overflow_result}")

        fill_val = 6 if self.cpu._fileFormat == "six-digit" else 4

        if result >= 0:
            self.cpu._accumulator = '+' + str(overflow_result).zfill(fill_val)
        else:
            self.cpu._accumulator = '-' + str(overflow_result).zfill(fill_val)
    
    #subtracts value in memory from the accumulator & then stores it
        
    def SUBTRACT(self, address):
        mem_value = int(self.cpu.memory[int(address)])
        acc_value = int(self.cpu._accumulator)
        result = acc_value - mem_value

        overflow_limit = 1000000 if self.cpu._fileFormat == "six-digit" else 10000
        overflow_result = abs(result) % overflow_limit
        fill_val = 6 if self.cpu._fileFormat == "six-digit" else 4

        if result >= 0:
            self.cpu._accumulator = '+' + str(overflow_result).zfill(fill_val)
        else:
            self.cpu._accumulator = '-' + str(overflow_result).zfill(fill_val)

    #divides value in memory from the accumulator & then stores it

    def DIVIDE(self, address):
        mem_value = int(self.cpu.memory[int(address)])
        if mem_value == 0:
            raise ValueError("Division by zero")
        acc_value = int(self.cpu._accumulator)
        result = int(acc_value / mem_value)

        overflow_limit = 1000000 if self.cpu._fileFormat == "six-digit" else 10000
        overflow_result = abs(result) % overflow_limit
        fill_val = 6 if self.cpu._fileFormat == "six-digit" else 4

        if result >= 0:
            self.cpu._accumulator = '+' + str(overflow_result).zfill(fill_val)
        else:
            self.cpu._accumulator = '-' + str(overflow_result).zfill(fill_val)

    #multiplies value in memory from the accumulator & then stores it

    def MULTIPLY(self, address):
        mem_value = int(self.cpu.memory[int(address)])
        acc_value = int(self.cpu._accumulator)
        result = acc_value * mem_value
        
        overflow_limit = 1000000 if self.cpu._fileFormat == "six-digit" else 10000
        overflow_result = abs(result) % overflow_limit
        fill_val = 6 if self.cpu._fileFormat == "six-digit" else 4

        if result >= 0:
            self.cpu._accumulator = '+' + str(overflow_result).zfill(fill_val)
        else:
            self.cpu._accumulator = '-' + str(overflow_result).zfill(fill_val)

class ControlUnit:

    def __init__(self, cpu):
        self.cpu = cpu
    
    def LOAD(self, address):
        self.cpu._accumulator = self.cpu.memory[int(address)]
        
    def STORE(self, address):
        self.cpu.memory[int(address)] = self.cpu._accumulator

    def BRANCH(self, value):
        '''branches to a specified point in memory'''
        try:
            value = int(value)
            if 0 <= value < self.cpu.maxFileSize:
                return int(value) - 1        #subtract one here, because one will be added at the end of the run loop by default
            else:
                self.cpu.output(f'Pick a value less than {self.cpu.maxFileSize}, but more than -1 to branch to')
                return False
        except:
            self.cpu.output('Only can branch to an integer')
            return False

    #branches to a specified point in memory

    def BRANCHNEG(self, value):
        '''branches to a specified point in memory, but only if the accumulator is negative'''
        if self.cpu._accumulator[0] == '-':
            return self.BRANCH(value)
        else:
            return False

    #branches to a specified point in memory, but only if the accumulator is negative

    def BRANCHZERO(self, value):
        '''branches to a specified point in memory, but only if the accumulator is positive'''
        if int(self.cpu._accumulator) == 0:
            return self.BRANCH(value)
        else:
            return False
        
    #branches to a specified point in memory, but only if the accumulator is positive

    def HALT(self, command='043'):
        '''halts the program if the command given to it is the string 043'''
        if command == '043':
            self.cpu.output('Halted')
            self.cpu.output('')
            return True
        else:
            return False


if __name__ == '__main__':
    Gui(CPU)
 
