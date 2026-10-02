from gui import Gui

class CPU:

    ###  ------ CPU Initialization ------ ###

    def __init__(self, filename: str):

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
            #See if the current line is a number. If not, raise a ValueError
            try:
                float(commands[i])
            except:
                raise ValueError("Invalid command '" + commands[i] + "' in file " + filename)
            
            command = commands[i][1:3]
            # If there has already been a halt command, the user can input whatever values they like, as long as they fit the '+/- ####' format
            if halted:
                if (len(commands[i]) != 5 or (commands[i][0] not in ['+','-'])):
                    raise ValueError("Invalid command '" + commands[i] + "' in file " + filename)
                self.memory[i] = commands[i]
            else:
                # First make sure that each command is valid. If there are any invalid commands, raise an error
                if (len(commands[i]) != 5 or (command not in validCommands) or (commands[i][0] not in ['+','-'])):
                    raise ValueError("Invalid command '" + commands[i] + "' in file " + filename)
                # Command Valid, continue
                self.memory[i] = commands[i]
                if command == '43':
                    halted = True
            

    ###  ------ CPU Methods ------ ###

    ## Public Methods ##
    def run(self, pointer=0, gui_input=''):
        # print("Running the machine...")
        # print(pointer,input)

        halted = False
        need_input = False
        print_val = None

        while not halted:
            fullCommandString = self.memory[pointer]      # This goes through the commands one by one
            commandSign = fullCommandString[0]            # This refers to if the command is positive or negative
            command = fullCommandString[1:3]              # The first two numbers of the command in form '+####'. The 3rd index is non inclusive
            value = fullCommandString [3:5]               # The last two numbers of the command, or the value of the command

            # print(f'fullCommandString {fullCommandString}, command {command}, value {value}, pointer {pointer}, accumulator, {self._accumulator}')
            # print("fullCommandString:", fullCommandString)
            # print("commandSign:", commandSign)
            # print("command:", command)
            # print("value:", value)
            
            match command:
                case '10':
                    # print(gui_input)
                    got_input = self._communicationUnit.READ(value,gui_input)
                    if got_input == True:
                        need_input = False
                        pointer += 1
                        return (halted, pointer, need_input, print_val)
                    else:
                        print_val = "Please Enter a value in this format: +/-0000: "
                        need_input = True
                        return (halted, pointer, need_input, print_val)

                    # print("reading")

                case '11':
                    self._communicationUnit.WRITE(value)
                    # print("writing")
                    
                case '20':
                    self._controlUnit.LOAD(value)
                    # print("loading")

                case '21':
                    self._controlUnit.STORE(value)
                    # print("storing")

                case '30':
                    self._arithmeticUnit.ADD(value)
                    # print("adding")

                case '31':
                    self._arithmeticUnit.SUBTRACT(value)
                    # print("subtracting")

                case '32':
                    self._arithmeticUnit.DIVIDE(value)
                    # print("dividing")

                case '33':
                    self._arithmeticUnit.MULTIPLY(value)
                    # print("multiplying")

                case '40':
                    pointer = self._controlUnit.BRANCH(value) - 1  #subtract one here, because one will be added at the end of loop by default
                    # print(f'Branched to {pointer}')

                case '41':
                    # print(f'Value to branch to {value}, accumulator is {self._accumulator}')

                    branch_val = self._controlUnit.BRANCHNEG(value)
                    if type(branch_val) == int:
                        pointer = branch_val - 1        #subtract one here, because one will be added at the end of loop by default
                        # print(f'Branched to {branch_val}')

                case '42':
                    # print(f'Value to branch to {value}, accumulator is {self._accumulator}')

                    branch_val = self._controlUnit.BRANCHZERO(value)
                    if type(branch_val) == int:
                        pointer = branch_val - 1        #subtract one here, because one will be added at the end of loop by default
                        # print(f'Branched to {branch_val}')

                case '43':
                    halted = self._controlUnit.HALT(command)
                    # print("halting")

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
                if len(user_input) == 5 and user_input[0] in ['+', '-'] and user_input[1:].isdigit():
                    self.cpu.memory[int(address)] = user_input
                    break
                print("Invalid input.")
        else:
            user_input = input_val
            if len(user_input) == 5 and user_input[0] in ['+', '-'] and user_input[1:].isdigit():
                return True
            return False
    
    def WRITE(self, address):
        print(self.cpu.memory[int(address)])

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
            if 0 <= value < 100:
                return int(value)
            else:
                print('Pick a value less than 100, but more than -1')
                return False
        except:
            print('Only can branch to an integer')
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
            print('Halted')
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
