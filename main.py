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
        self.__accumulator = '0000'
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
            if (len(commands[i]) != 5 or (command not in validCommands)):
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

            # print("fullCommandString:", fullCommandString)
            # print("commandSign:", commandSign)
            # print("command:", command)
            # print("value:", value)

            if command == '10':
                self.__READ()
                # print("reading")

            elif command == '11':
                self.__WRITE()
                # print("writing")

            elif command == '20':
                self.__LOAD()
                # print("loading")

            elif command == '21':
                self.__STORE()
                # print("storing")

            elif command == '30':
                self.__ADD()
                # print("adding")

            elif command == '31':
                self.__SUBTRACT()
                # print("subtracting")

            elif command == '32':
                self.__DIVIDE()
                # print("dividing")

            elif command == '33':
                self.__MULTIPLY()
                # print("multiplying")

            elif command == '40':
                self.__BRANCH()
                # print("branching")

            elif command == '41':
                self.__BRANCHNEG()
                # print("brang-neg-ing")

            elif command == '42':
                self.__BRANCHZERO()
                # print("branch-zero-ing")

            elif command == '43':
                halted = True
                self.__HALT()
                # print("halting")

            else:
                raise ValueError("Command '" + fullCommandString + "' is not a valid command")

            pointer += 1



    ## Private Methods (denoted by leading double underscores) ##

    def __READ(self):
        ...

    def __WRITE(self):
        ...

    def __LOAD(self):
        ...
    
    def __STORE(self):
        ...

    def __ADD(self):
        ...
    
    def __SUBTRACT(self):
        ...

    def __DIVIDE(self):
        ...

    def __MULTIPLY(self):
        ...

    def __BRANCH(self):
        ...

    def __BRANCHNEG(self):
        ...
    
    def __BRANCHZERO(self):
        ...

    def __HALT(self):
        ...

        

    
myCPU = CPU('testfile.txt')
myCPU.run()

