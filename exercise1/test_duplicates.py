import pytest
from detect_duplicates import detect_duplicates


@pytest.mark.parametrize("input_list, expected_duplicates", [
    (["b", "a", "c", "c", "e", "a", "c", "d", "c", "d"], ["a", "c", "d"]),
    ([1, 2, 3, 3, 4, 4, 5], [3, 4]),
    ([True, False, False, False, True, True], [True, False]),
    ([True, False, "banana", 0, True, "avocado", "8", "banana", 0, 0], [True, 0, "banana"]),
    ([True, False, "banana", 1, True, "avocado", "8", "banana", 1, 1], [True, "banana"]),
    ([[1, 2, 3], [4, 5, 6], [1, 2, 3], "8", 14, [8, 32], "8", [1, 2, 3], [8, 32]], [[1, 2, 3], "8", [8, 32]]),
    ([4.123, -1.02, "banana", 98.29, 10E6, 1.02, -892.3, "avocado", -1.02, -1.02, "banana", 4.123, 108.92, 10E6],
     [4.123, -1.02, "banana", 10E6])
])
# Test lists using detect_duplicates()
def test_detect_duplicates_unsorted(input_list, expected_duplicates):
    duplicates = detect_duplicates(input_list)
    assert duplicates == expected_duplicates
