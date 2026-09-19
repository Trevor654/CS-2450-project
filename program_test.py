import pytest
from main import CPU

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


testing_CPU = CPU('Testing_files/branchtestfile.txt')

def test_branch():
    assert testing_CPU._CPU__BRANCH('hi') == False
    assert testing_CPU._CPU__BRANCH('50') == 50
    assert testing_CPU._CPU__BRANCH(150) == False
    assert testing_CPU._CPU__BRANCH(-150) == False

def test_branchneg():
    testing_CPU._CPU__accumulator = '-0001'
    assert testing_CPU._CPU__BRANCHNEG('60') == 60
    assert testing_CPU._CPU__BRANCHNEG(-50) == False
    testing_CPU._CPU__accumulator = '+0001'
    assert testing_CPU._CPU__BRANCHNEG(50) == False

def test_branchzero():
    testing_CPU._CPU__accumulator = '+0000'
    assert testing_CPU._CPU__BRANCHZERO('75') == 75
    assert testing_CPU._CPU__BRANCHZERO(-70) == False
    testing_CPU._CPU__accumulator = '+0001'
    assert testing_CPU._CPU__BRANCHZERO(50) == False

def test_halt():
    assert testing_CPU._CPU__HALT('43') == True
    assert testing_CPU._CPU__HALT('44') == False
    assert testing_CPU._CPU__HALT() == True

def test_add():
    testing_CPU._CPU__accumulator = '+0056'
    testing_CPU.memory[20] = '-0028'
    testing_CPU._CPU__ADD(20)
    assert testing_CPU._CPU__accumulator == '+0028'

def test_subtract():
    testing_CPU._CPU__accumulator = '+0056'
    testing_CPU.memory[21] = '-0030'
    testing_CPU._CPU__SUBTRACT(21)
    assert testing_CPU._CPU__accumulator == '+0086'

def test_multiply():
    testing_CPU._CPU__accumulator = '+0056'
    testing_CPU.memory[56] = '+0003'
    testing_CPU._CPU__MULTIPLY(56)
    assert testing_CPU._CPU__accumulator == '+0168'

def test_divide():
    testing_CPU._CPU__accumulator = '+0028'
    testing_CPU.memory[87] = '+0007'
    testing_CPU._CPU__DIVIDE(87)
    assert testing_CPU._CPU__accumulator == '+0004'
