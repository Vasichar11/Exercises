def homogeneous(input_list=None):
    # Function that returns True if the elements of the input list are all of the same type
    for element in input_list:
        if not isinstance(element, type(input_list[0])):
            return False
    return True


def is_sorted(input_list=None):
    # Function that returns True if the input list is sorted (ascending or descending order)
    # O(n) time complexity.
    ascending = descending = False
    if homogeneous(input_list):
        n = len(input_list)
        ascending = all(input_list[i] <= input_list[i + 1] for i in range(n - 1))
        descending = all(input_list[i] >= input_list[i + 1] for i in range(n - 1))

    return ascending or descending
