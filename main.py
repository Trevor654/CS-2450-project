class CPU:

    ###  ------ CPU Initialization ------ ###

    def __init__(self, filename: str):

        # If the filename doesn't exist, throw an error. If it does, edit the memory 
        try:
            file = open(filename, 'r')
            filecontent = file.read()
            commands = filecontent.split('\n')
        except:
            raise ValueError("File '" + filename + "' does not exist or filepath is invalid")

        # Other variables
        self.__accumulator = '+0000'
        self.__input = ''
        self.__output = ''
        self.memory = {}        # Main memory dictionary
        for i in range(100):
            self.memory[i] = '0000'

        # Loading in the commands from the file into the dictionary
        validCommands = ['10','11','20','21','30','31','32','33','40','41','42','43']
        for i in range(len(commands)):
            # First make sure that each command is valid. If there are any invalid commands, raise an error
            command = commands[i][1:3]
            if (len(commands[i]) != 5 or (command not in validCommands) or (commands[i][0] not in ['+','-'])):
                raise ValueError("Invalid command '" + commands[i] + "' in file " + filename)

            # Command Valid, continue
            self.memory[i] = commands[i]
            

    ###  ------ CPU Methods ------ ###

    ## Public Methods ##
    def run(self):
        # print("Running the machine...")
        halted = False
        pointer = 0
        while not halted:
            fullCommandString = self.memory[pointer]      # This goes through the commands one by one
            commandSign = fullCommandString[0]            # This refers to if the command is positive or negative
            command = fullCommandString[1:3]              # The first two numbers of the command in form '+####'. The 3rd index is non inclusive
            value = fullCommandString [3:5]               # The last two numbers of the command, or the value of the command

            # print(f'fullCommandString {fullCommandString}, command {command}, value {value}, pointer {pointer}, accumulator, {self.__accumulator}')
            # print("fullCommandString:", fullCommandString)
            # print("commandSign:", commandSign)
            # print("command:", command)
            # print("value:", value)

            if command == '10':
                self.__READ(value)
                # print("reading")

            elif command == '11':
                self.__WRITE(value)
                # print("writing")

            elif command == '20':
                self.__LOAD(value)
                # print("loading")

            elif command == '21':
                self.__STORE(value)
                # print("storing")

            elif command == '30':
                self.__ADD(value)
                # print("adding")

            elif command == '31':
                self.__SUBTRACT(value)
                # print("subtracting")

            elif command == '32':
                self.__DIVIDE(value)
                # print("dividing")

            elif command == '33':
                self.__MULTIPLY(value)
                # print("multiplying")

            elif command == '40':
                pointer = self.__BRANCH(value) - 1

                # Debug prints
                # print(f'Value to branch to {value}')
                # print(f'Branched to {pointer}')

            elif command == '41':
                # print(f'Value to branch to {value}, accumulator is {self.__accumulator}')

                branch_val = self.__BRANCHNEG(value)
                if type(branch_val) == int:
                    pointer = branch_val - 1
                    # print(f'Branched to {branch_val}')

            elif command == '42':
                # print(f'Value to branch to {value}, accumulator is {self.__accumulator}')

                branch_val = self.__BRANCHZERO(value)
                if type(branch_val) == int:
                    pointer = branch_val - 1
                    # print(f'Branched to {branch_val}')

            elif command == '43':
                halted = True
                self.__HALT()
                # print("halting")

            else:
                raise ValueError("Command '" + fullCommandString + "' is not a valid command")

            pointer += 1



    ## Private Methods (denoted by leading double underscores) ##

    def __READ(self, address):
        while True:
            user_input = input("Enter a value (format +/-0000): ")
            if len(user_input) == 5 and user_input[0] in ['+', '-'] and user_input[1:].isdigit():
                self.memory[int(address)] = user_input
                break
            print("Invalid input.")

    def __WRITE(self, address):
        print(self.memory[int(address)])

    def __LOAD(self, address):
        self.__accumulator = self.memory[int(address)]

    def __STORE(self, address):
        self.memory[int(address)] = self.__accumulator

#adds value in memory to the accumulator & then stores it
#oh and mem_value is memory value and acc_value is the accumulator value :) 

    def __ADD(self, address):
        mem_value = int(self.memory[int(address)])
        acc_value = int(self.__accumulator)
        result = acc_value + mem_value

        if result >= 0:
            self.__accumulator = '+' + str(result).zfill(4)
        else:
            self.__accumulator = '-' + str(abs(result)).zfill(4)

#subtracts value in memory from the accumulator & then stores it
    
    def __SUBTRACT(self, address):
        mem_value = int(self.memory[int(address)])
        acc_value = int(self.__accumulator)
        result = acc_value - mem_value

        if result >= 0:
            self.__accumulator = '+' + str(result).zfill(4)
        else:
            self.__accumulator = '-' + str(abs(result)).zfill(4)

#divides value in memory from the accumulator & then stores it

    def __DIVIDE(self, address):
        mem_value = int(self.memory[int(address)])
        if mem_value == 0:
            raise ValueError("Division by zero")
        acc_value = int(self.__accumulator)
        result = int(acc_value / mem_value)

        if result >= 0:
            self.__accumulator = '+' + str(result).zfill(4)
        else:
            self.__accumulator = '-' + str(abs(result)).zfill(4)

#multiplies value in memory from the accumulator & then stores it

    def __MULTIPLY(self, address):
        mem_value = int(self.memory[int(address)])
        acc_value = int(self.__accumulator)
        result = acc_value * mem_value
        
        if result >= 0:
            self.__accumulator = '+' + str(result).zfill(4)
        else:
            self.__accumulator = '-' + str(abs(result)).zfill(4)

    def __BRANCH(self, value):
        return int(value)

    def __BRANCHNEG(self, value):
        if self.__accumulator[0] == '-':
            return int(value)
        else:
            return False
    
    def __BRANCHZERO(self, value):
        if '0000' in self.__accumulator:
            return int(value)
        else:
            return False

    def __HALT(self):
        '''Nothing needed here right now, covered before calling this function'''
        ...

        

    



if __name__ == '__main__':
    # myCPU = CPU('Testing_files/testfile.txt')
    # myCPU.run()
    while True:
        try:
            file = input('Please type the file path to the file you want to run (ex. Testing_files/testfile.txt)\n')
            if file.lower() == 'break':
                break
            myCPU = CPU(file)
            myCPU.run()  # added run call
            break
        except:
            print('Please type a valid file path or type "break" to stop\n')
