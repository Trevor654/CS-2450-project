from gui import Gui
from functions import *

class CPU:

    ###  ------ CPU Initialization ------ ###

    def __init__(self, filename: str, gui=None):

        self.gui = gui

        # If the filename doesn't exist, throw an error. If it does, edit the memory 
        try:
            file = open(filename, 'r')
            filecontent = file.read()
            commands = filecontent.split('\n')
        except:
            raise FileNotFoundError("File '" + filename + "' does not exist or the filepath is invalid")

        # Other variables
        self._accumulator = '+0000'
        self._input = ''
        self._output = ''
        self._communicationUnit = CommunicationUnit(self)
        self._arithmeticUnit = ArithmeticUnit(self)
        self._controlUnit = ControlUnit(self)
        self.memory = {}        # Main memory dictionary
        for i in range(100):
            self.memory[i] = '+0000'

        # Loading in the commands from the file into the dictionary
        validCommands = ['10','11','20','21','30','31','32','33','40','41','42','43']
        halted = False
        for i in range(len(commands)):
            command = commands[i][1:3]
            # If there has already been a halt command, the user can input whatever values they like, as long as they fit the '+/- ####' format
            if halted:
                if (checkValidInput5chars(commands[i]) == False):
                    errors = []
                    for k in range(i,len(commands)):
                        if checkValidInput5chars(commands[k]) == False:
                            errors.append(commands[k])
                    errorString = "Invalid command(s) in the given file: "
                    errorStringList = ", ".join(errors)
                    errorString += errorStringList
                    raise ValueError(errorString)
                self.memory[i] = commands[i]
            else:
                # First make sure that each command is valid. If there are any invalid commands, raise an error
                if ((checkValidInput5chars(commands[i]) == False) or (command not in validCommands)):
                    errors = []
                    for k in range(i,len(commands)):
                        if checkValidInput5chars(commands[k]) == False:
                            errors.append(commands[k])
                    errorString = "Invalid command(s) in the given file: "
                    errorStringList = ", ".join(errors)
                    errorString += errorStringList
                    raise ValueError(errorString)
                # Command Valid, continue
                self.memory[i] = commands[i]
                if command == '43':
                    halted = True
            

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
            fullCommandString = self.memory[pointer]      # This goes through the commands one by one
            commandSign = fullCommandString[0]            # This refers to if the command is positive or negative
            command = fullCommandString[1:3]              # The first two numbers of the command in form '+####'. The 3rd index is non inclusive
            value = fullCommandString [3:5]               # The last two numbers of the command, or the value of the command
            print(pointer,fullCommandString, gui_input)
            
            match command:
                case '10':
                    got_input = self._communicationUnit.READ(value,gui_input)
                    if got_input == True:
                        need_input = False
                        pointer += 1
                        return (halted, pointer, need_input, print_val)
                    else:
                        print_val = "Please Enter a value in this format: +/-0000: "
                        need_input = True
                        return (halted, pointer, need_input, print_val)

                case '11':
                    self._communicationUnit.WRITE(value)
                    
                case '20':
                    self._controlUnit.LOAD(value)

                case '21':
                    self._controlUnit.STORE(value)

                case '30':
                    self._arithmeticUnit.ADD(value)

                case '31':
                    self._arithmeticUnit.SUBTRACT(value)

                case '32':
                    self._arithmeticUnit.DIVIDE(value)

                case '33':
                    self._arithmeticUnit.MULTIPLY(value)

                case '40':
                    pointer = self._controlUnit.BRANCH(value)

                case '41':
                    branch_val = self._controlUnit.BRANCHNEG(value)
                    if type(branch_val) == int:
                        pointer = branch_val

                case '42':

                    branch_val = self._controlUnit.BRANCHZERO(value)
                    if type(branch_val) == int:
                        pointer = branch_val

                case '43':
                    halted = self._controlUnit.HALT(command)

                case _:
                    raise ValueError("Command '" + fullCommandString + "' is not a valid command")

            pointer += 1
            return (halted, pointer, need_input, print_val)

###---------------------- SUBCLASSES ----------------------###

class CommunicationUnit:

    def __init__(self, cpu):
        self.cpu = cpu
        
    def READ(self, address, input_val='No Gui'):
            
        if input_val == 'No Gui':
            while True:
                user_input = input("Enter a value (format +/-0000): ")
                if checkValidInput5chars(user_input):
                    self.cpu.memory[int(address)] = user_input
                    break
                elif checkValidInput4chars(user_input):
                    self.cpu.memory[int(address)] = ('+' + user_input)
                    break
                print("Invalid input.")
        else:
            user_input = input_val
            if checkValidInput5chars(user_input):
                self.cpu.memory[int(address)] = user_input
                return True
            elif checkValidInput4chars(user_input):
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

        truncated_result = abs(result) % 10000

        if result >= 0:
            self.cpu._accumulator = '+' + str(truncated_result).zfill(4)
        else:
            self.cpu._accumulator = '-' + str(truncated_result).zfill(4)
    
    #subtracts value in memory from the accumulator & then stores it
        
    def SUBTRACT(self, address):
        mem_value = int(self.cpu.memory[int(address)])
        acc_value = int(self.cpu._accumulator)
        result = acc_value - mem_value

        truncated_result = abs(result) % 10000

        if result >= 0:
            self.cpu._accumulator = '+' + str(truncated_result).zfill(4)
        else:
            self.cpu._accumulator = '-' + str(truncated_result).zfill(4)

    #divides value in memory from the accumulator & then stores it

    def DIVIDE(self, address):
        mem_value = int(self.cpu.memory[int(address)])
        if mem_value == 0:
            raise ValueError("Division by zero")
        acc_value = int(self.cpu._accumulator)
        result = int(acc_value / mem_value)

        truncated_result = abs(result) % 10000

        if result >= 0:
            self.cpu._accumulator = '+' + str(truncated_result).zfill(4)
        else:
            self.cpu._accumulator = '-' + str(truncated_result).zfill(4)

    #multiplies value in memory from the accumulator & then stores it

    def MULTIPLY(self, address):
        mem_value = int(self.cpu.memory[int(address)])
        acc_value = int(self.cpu._accumulator)
        result = acc_value * mem_value
        
        truncated_result = abs(result) % 10000

        if result >= 0:
            self.cpu._accumulator = '+' + str(truncated_result).zfill(4)
        else:
            self.cpu._accumulator = '-' + str(truncated_result).zfill(4)

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
            if 1 <= value < 100:
                return int(value) - 1        #subtract one here, because one will be added at the end of the run loop by default
            else:
                self.cpu.output('Pick a value less than 100, but more than -1 to branch to')
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
        if '0000' in self.cpu._accumulator:
            return self.BRANCH(value)
        else:
            return False
        
    #branches to a specified point in memory, but only if the accumulator is positive

    def HALT(self, command='43'):
        '''halts the program if the command given to it is the string 43'''
        if command == '43':
            self.cpu.output('Halted')
            return True
        else:
            return False


if __name__ == '__main__':
    Gui(CPU)
    # myCPU = CPU('Testing_files/testfile.txt')
    # myCPU.run()
    

    # while True:    
    #     try:
    #         file = input('Please type the file path to the file you want to run (ex. Testing_files/testfile.txt)\n')
    #         if file.lower() == 'break':
    #             break
    #         myCPU = CPU(file)
    #         myCPU.run()  # added run call
    #         print('\n--------------------Functions complete--------------------\n')
    #         break
    #     except Exception as e:
    #         print(e)
