import pytest
from main import CPU

def testREADValidInput(monkeypatch):
    inputCase1 = '+1007'  # Native valid value from Testing_files/testfile.txt
    test_address = '00'
    
    cpu = CPU("Testing_files/testfile.txt")
    monkeypatch.setattr('builtins.input', lambda _: inputCase1)
    cpu._CPU__READ(test_address)
    
    assert cpu.memory[int(test_address)] == inputCase1

def testREADInvalidInput(monkeypatch):
    inputCaseInvalid = 'abc'
    inputCaseValid = '+1008'  # Native valid value from Testing_files/testfile.txt
    test_address = '01'
    
    # The __READ loop will reject 'abc' and then accept '+1008'
    inputs = iter([inputCaseInvalid, inputCaseValid])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    cpu = CPU("Testing_files/testfile.txt")
    cpu._CPU__READ(test_address)
    
    assert cpu.memory[int(test_address)] == inputCaseValid

def testWRITEValidMemory():
    test_address = '00'
    expected_value = '+1007'  # Pre-loaded in Testing_files/testfile.txt memory[0]
    
    cpu = CPU("Testing_files/testfile.txt")
    cpu._CPU__WRITE(test_address)
    
    # Asserting memory remains intact without using capsys
    assert cpu.memory[int(test_address)] == expected_value

def testWRITEInvalidAddress():
    invalid_address = '999'
    
    cpu = CPU("Testing_files/testfile.txt")
    with pytest.raises(KeyError):
        cpu._CPU__WRITE(invalid_address)

def testLOADValidPositive():
    test_address = '02'
    expected_value = '+2007'  # Pre-loaded in Testing_files/testfile.txt memory[2]
    
    cpu = CPU("Testing_files/testfile.txt")
    cpu._CPU__LOAD(test_address)
    
    assert cpu._CPU__accumulator == expected_value

def testLOADValidNegative():
    test_address = '04'
    expected_value = '-2109'  # Pre-loaded in Testing_files/testfile.txt memory[4]
    
    cpu = CPU("Testing_files/testfile.txt")
    cpu._CPU__LOAD(test_address)
    
    assert cpu._CPU__accumulator == expected_value

def testLOADInvalidAddress():
    invalid_address = 'xyz'
    
    cpu = CPU("Testing_files/testfile.txt")
    with pytest.raises(ValueError):
        cpu._CPU__LOAD(invalid_address)

def testSTOREValidPositive():
    source_address = '00'
    expected_value = '+1007'  # Pre-loaded in Testing_files/testfile.txt memory[0]
    store_address = '20'
    
    cpu = CPU("Testing_files/testfile.txt")
    cpu._CPU__LOAD(source_address)
    cpu._CPU__STORE(store_address)
    
    assert cpu.memory[int(store_address)] == expected_value

def testSTOREValidNegative():
    source_address = '04'
    expected_value = '-2109'  # Pre-loaded in Testing_files/testfile.txt memory[4]
    store_address = '21'
    
    cpu = CPU("Testing_files/testfile.txt")
    cpu._CPU__LOAD(source_address)
    cpu._CPU__STORE(store_address)
    
    assert cpu.memory[int(store_address)] == expected_value

def testSTOREInvalidAddress():
    invalid_address = 'invalid'
    
    cpu = CPU("Testing_files/testfile.txt")
    with pytest.raises(ValueError):
        cpu._CPU__STORE(invalid_address)
