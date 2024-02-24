# test_my_module.py
from functions import add, subtract, multiply, divide, calculate_factorial
from type_hinting import add_2_numbers, add_strings, empty_function
import pytest

def test_add():
    assert add(3, 5) == 8
    assert add(-1, 1) == 0
    # Add more test cases for add function

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(-1, 1) == -2
    # Add more test cases for subtract function

def test_multiply():
    assert multiply(3, 5) == 15
    assert multiply(-2, 4) == -8
    # Add more test cases for multiply function

def test_divide():
    assert divide(10, 2) == 5
    assert divide(-8, 4) == -2
    # Add more test cases for divide function

    # Test division by zero
    with pytest.raises(ValueError):
        divide(5, 0)



def test_calculate_factorial():
    # Test factorial of 0 and 1
    assert calculate_factorial(0) == 1
    assert calculate_factorial(1) == 1

    # Test factorial of a positive number
    assert calculate_factorial(5) == 120
    assert calculate_factorial(10) == 3628800

    # Test factorial of a large number
    assert calculate_factorial(20) == 2432902008176640000

    # Test factorial of a negative number
    with pytest.raises(ValueError):
        calculate_factorial(-3)


def test_add_2_numbers(): 
    assert add_2_numbers(1,2) == 3
    assert add_2_numbers(-4,0) == -4
    assert add_2_numbers(0,0) == 0
    assert add_2_numbers("2", "1") == "21"
    with pytest.raises(TypeError):
        assert add_2_numbers({"key": "value"}, {"key_2": "value_2"})


def test_add_strings(): 
    assert add_strings(1,2) == 3
    assert add_strings(-4,0) == -4
    assert add_strings(0,0) == 0
    assert add_strings("2", "1") == "21"

def test_empty_function():
    assert empty_function() ==None
