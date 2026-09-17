import pytest
from main import CPU


testing_CPU = CPU('Testing_files/branchtestfile.txt')
# testing_CPU.run()
# print(testing_CPU._CPU__accumulator)

def test_branch():
    pass

def test_branchneg():
    pass

def test_branchzero():
    pass

def test_halt():
    assert testing_CPU._CPU__HALT('43') == True
    assert testing_CPU._CPU__HALT('44') == False

