import pytest
from main import CPU

def test_read_valid_input(monkeypatch):
    inputCase1 = '+1007'  # Native valid value from Testing_files/testfile.txt
    test_address = '00'
    
    cpu = CPU("Testing_files/testfile.txt")
    monkeypatch.setattr('builtins.input', lambda _: inputCase1)
    cpu._communicationUnit.READ(test_address)
    
    assert cpu.memory[int(test_address)] == inputCase1

def test_read_invalid_input(monkeypatch):
    inputCaseInvalid = 'abc'
    inputCaseValid = '+1008'  # Native valid value from Testing_files/testfile.txt
    test_address = '01'
    
    # The __READ loop will reject 'abc' and then accept '+1008'
    inputs = iter([inputCaseInvalid, inputCaseValid])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    cpu = CPU("Testing_files/testfile.txt")
    cpu._communicationUnit.READ(test_address)
    
    assert cpu.memory[int(test_address)] == inputCaseValid

def test_write_valid_address():
    test_address = '00'
    expected_value = '+1007'  # Pre-loaded in Testing_files/testfile.txt memory[0]
    
    cpu = CPU("Testing_files/testfile.txt")
    cpu._communicationUnit.WRITE(test_address)
    
    # Asserting memory remains intact without using capsys
    assert cpu.memory[int(test_address)] == expected_value

def test_write_invalid_address():
    invalid_address = '999'
    
    cpu = CPU("Testing_files/testfile.txt")
    with pytest.raises(KeyError):
        cpu._communicationUnit.WRITE(invalid_address)

def test_load_value_positive():
    test_address = '02'
    expected_value = '+2007'  # Pre-loaded in Testing_files/testfile.txt memory[2]
    
    cpu = CPU("Testing_files/testfile.txt")
    cpu._controlUnit.LOAD(test_address)
    
    assert cpu._accumulator == expected_value

def test_load_value_negative():
    test_address = '04'
    expected_value = '-2109'  # Pre-loaded in Testing_files/testfile.txt memory[4]
    
    cpu = CPU("Testing_files/testfile.txt")
    cpu._controlUnit.LOAD(test_address)
    
    assert cpu._accumulator == expected_value

def test_load_invalid_address():
    invalid_address = 'xyz'
    
    cpu = CPU("Testing_files/testfile.txt")
    with pytest.raises(ValueError):
        cpu._controlUnit.LOAD(invalid_address)

def test_store_value_positive():
    source_address = '00'
    expected_value = '+1007'  # Pre-loaded in Testing_files/testfile.txt memory[0]
    store_address = '20'
    
    cpu = CPU("Testing_files/testfile.txt")
    cpu._controlUnit.LOAD(source_address)
    cpu._controlUnit.STORE(store_address)
    
    assert cpu.memory[int(store_address)] == expected_value

def test_store_value_negative():
    source_address = '04'
    expected_value = '-2109'  # Pre-loaded in Testing_files/testfile.txt memory[4]
    store_address = '21'
    
    cpu = CPU("Testing_files/testfile.txt")
    cpu._controlUnit.LOAD(source_address)
    cpu._controlUnit.STORE(store_address)
    
    assert cpu.memory[int(store_address)] == expected_value

def test_store_invalid_address():
    invalid_address = 'invalid'
    
    cpu = CPU("Testing_files/testfile.txt")
    with pytest.raises(ValueError):
        cpu._controlUnit.STORE(invalid_address)
