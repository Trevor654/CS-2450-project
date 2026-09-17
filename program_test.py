import pytest
from main import CPU


testing_CPU = CPU('Testing_files/branchtestfile.txt')
# testing_CPU.run()
# print(testing_CPU._CPU__accumulator)

def test_init_bad_argument():
    # Testing if the argument given is an invalid testfile
    with pytest.raises(ValueError, match=r"File 'Testing_files/randomstring.txt' does not exist or filepath is invalid"): 
        CPU1 = CPU('Testing_files/randomstring.txt')
    with pytest.raises(ValueError, match=r"File 'Testing_files/samantha.txt' does not exist or filepath is invalid"): 
        CPU2 = CPU('Testing_files/samantha.txt')
    with pytest.raises(ValueError, match=r"File 'Testing_files/idk' does not exist or filepath is invalid"): 
        CPU3 = CPU('Testing_files/idk')

def test_init_invalid_string_in_file():
    with pytest.raises(ValueError, match=r"Invalid command '\+11aa' in file Testing_files/test_bad_string_1.txt"): 
        CPU1 = CPU('Testing_files/test_bad_string_1.txt')
    with pytest.raises(ValueError, match=r"Invalid command '\+30082' in file Testing_files/test_bad_string_2.txt"): 
        CPU1 = CPU('Testing_files/test_bad_string_2.txt')


def test_init_success():
    # Testing to see that no errors are raised by inputing valid testFileNames
    CPU1 = CPU('Testing_files/Test1.txt')
    CPU2 = CPU('Testing_files/Test2.txt')
    #testing to see that all of the memory allocations are correct
    assert CPU1.memory[0] == '+1007'
    assert CPU1.memory[1] == '+1008'
    assert CPU1.memory[2] == '+2007'
    assert CPU1.memory[3] == '+3008'
    assert CPU1.memory[4] == '+2109'
    assert CPU1.memory.get(5) == '+1109'
    assert CPU1.memory.get(6) == '+4300'
    assert CPU1.memory.get(7) == '+0000'
    assert CPU1.memory.get(8) == '+0000'
    assert CPU1.memory.get(9) == '+0000'

def test_branch():
    pass

def test_branchneg():
    pass

def test_branchzero():
    pass

def test_halt():
    assert testing_CPU._CPU__HALT('43') == True
    assert testing_CPU._CPU__HALT('44') == False

