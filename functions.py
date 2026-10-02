#Useful functions used in multiple modules

#checks if an input from the user or from a given file is in the correct format for 5 characters

def checkValidInput5chars(input): #Returns true if the input is valid, returns false if invalid
    if len(input) == 5 and input[0] in ['+', '-'] and input[1:].isdigit():
        return True
    return False

#checks if an input from the user or from a given file is in the correct format for 4 characters (implicit '+' sign, should not be used with file checking)
def checkValidInput4chars(input): #Returns true if the input is valid, returns false if invalid
    if len(input) == 4 and input.isdigit():
        return True
    return False
