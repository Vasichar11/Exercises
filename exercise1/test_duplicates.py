import pytest
from detect_duplicates import detect_duplicates
from utils.classes import Proton, Date


sputnik_space = Date(1957, 10, 4)
apollo11_moon = Date(1969, 7, 20)
titanic_sinks = Date(1912, 4, 15)
swiss_cheese_birth = Date(1912, 4, 15)

proton1 = Proton(10e-6, 600e3, 30, 10)
proton2 = Proton(8.1e-6, 453e3, 31, 10)
proton3 = Proton(10e-6, 600e3, 30, 10)
proton4 = Proton(15e-6, 1000e3, 90, 45)


@pytest.mark.parametrize("input_list, expected_duplicates", [
    (["b", "a", "c", "c", "e", "a", "c", "d", "c", "d"], ["a", "c", "d"]),
    ([1, 2, 3, 3, 4, 4, 5], [3, 4]),
    ([True, False, False, False, True, True], [True, False]),
    ([True, False, "banana", 0, True, "avocado", "8", "banana", 0, 0], [True, 0, "banana"]),
    ([True, False, "banana", 1, True, "avocado", "8", "banana", 1, 1], [True, "banana"]),
    ([[1, 2, 3], [4, 5, 6], [1, 2, 3], "8", 14, [8, 32], "8", [1, 2, 3], [8, 32]], [[1, 2, 3], "8", [8, 32]]),
    ([4.123, -1.02, "banana", 98.29, 10E6, 1.02, -892.3, "avocado", -1.02, -1.02, "banana", 4.123, 108.92, 10E6], [4.123, -1.02, "banana", 10E6]),
    ([apollo11_moon, sputnik_space, titanic_sinks, swiss_cheese_birth, proton1, proton2, proton3], [titanic_sinks, proton1])
])
# Test lists using detect_duplicates()
def test_detect_duplicates(input_list, expected_duplicates):
    duplicates = detect_duplicates(input_list)
    assert duplicates == expected_duplicates


# Expected fails
# TypeError is expected for string inputs
def test_invalid_list():
    with pytest.raises(TypeError):
        detect_duplicates("test")


"""SUCCESS!
@pytest.mark.xfail(reason="Test fails. Using lists as elements is not supported yet.")
def test_lists():
    failing_list = [[1, 2, 3], [4, 5, 6], [1, 2, 3], "8", 14, [8, 32], "8", [1, 2, 3], [8, 32]]
    expected_list = [[1, 2, 3], "8", [8, 32]]
    assert detect_duplicates(failing_list) == expected_list


@pytest.mark.xfail(reason="Test fails. Integer 0 is interpreted as False.")
def test_boolean0():
    failing_list = [True, False, "banana", 0, True, "avocado", "8", "banana", 0, 0]
    expected_list = [True, 0, "banana"]
    assert detect_duplicates(failing_list) == expected_list


@pytest.mark.xfail(reason="Test fails. Integer 1 interpreted as True.")
def test_boolean1():
    failing_list = [True, False, "banana", 1, True, "avocado", "8", "banana", 1, 1]
    expected_list = [True, "banana"]
    assert detect_duplicates(failing_list) == expected_list


@pytest.mark.xfail(reason="Test fails. Using instances of classes as elements is not supported yet")
def test_classes():
    failing_list = [apollo11_moon, sputnik_space, titanic_sinks, swiss_cheese_birth, proton1, proton2, proton3]
    expected_list = [titanic_sinks, proton1]
    assert detect_duplicates(failing_list) == expected_list
"""
