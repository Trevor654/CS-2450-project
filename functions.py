#Useful functions used in multiple modules


## FOUR-DIGIT COMMAND CODES
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

## SIX-DIGIT COMMAND CODES
#checks if an input from the user or from a given file is in the correct format for 7 characters
def checkValidInput7chars(input): #Returns true if the input is valid, returns false if invalid
    if len(input) == 7 and input[0] in ['+', '-'] and input[1:].isdigit():
        return True
    return False

#checks if an input from the user or from a given file is in the correct format for 6 characters (implicit '+' sign, should not be used with file checking)
def checkValidInput6chars(input): #Returns true if the input is valid, returns false if invalid
    if len(input) == 6 and input.isdigit():
        return True
    return False

def convertNumToCommand(number, fileFormat):
    try:
        number = int(number)
    except:
        raise ValueError(f"Input number must be convertable to type \"int.\" Instead recieved: {number}")

    numString = ""
    if fileFormat == "six-digit":
        if -999999 <= number and number <= 999999:
            if number >= 0:
                numString = str(number).zfill(6)
                return "+" + numString
            else:
                number = abs(number)
                numString = str(number).zfill(6)
                return "-" + numString
        else:
            raise ValueError(f"{number} is outside of the maximum range for a {fileFormat} formated cpu")

    elif fileFormat == "four-digit" :
        if -9999 <= number and number <= 9999:
            if number >= 0:
                numString = str(number).zfill(4)
                return "+" + numString
            else:
                number = abs(number)
                numString = str(number).zfill(4)
                return "-" + numString
        else:
            raise ValueError(f"{number} is outside of the maximum range for a {fileFormat} formated cpu")
    else:
        raise ValueError(f"\"{fileFormat}\" is not a valid code-file-format. Must be either \"six-digit\" or \"four-digit\"")
