def detect_duplicates(input_list=None):
    # Time complexity of O(n^3), where n is the number of elements in the list
    duplicates = []
    for item in input_list:
        # .count() will internally scan the list, giving time complexity O(n) on its own
        # "in" operator has O(n) complexity for lists
        if input_list.count(item) > 1 and item not in duplicates:
            duplicates.append(item)

    return duplicates
