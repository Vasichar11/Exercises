from utils.functions import is_sorted


def detect_duplicates_unsorted(input_list=None):
    # Time complexity of O(n^3), where n is the number of elements in the list
    duplicates = []
    for item in input_list:

        if input_list.count(item) > 1 and item not in duplicates:
            duplicates.append(item)

    return duplicates


def detect_duplicates_sorted(input_list=None):
    # Time complexity O(n), where n is the number of elements in the list
    duplicates = []
    previous_item = None

    for item in input_list:
        if item == previous_item:
            if not duplicates or duplicates[-1] != item:  # Ensure list is not empty and check if this duplicate has been examined
                duplicates.append(item)
        previous_item = item

    return duplicates


# ----------------------------------- #
# ----------------------------------- #
# The function for exercise 1 follows #
# ----------------------------------- #
# ----------------------------------- #

# 1)
def detect_duplicates(input_list=None):
    duplicates = []
    # Function accepts only list types on its input
    if not isinstance(input_list, list):
        raise TypeError("Input must be a list.")

    # If sorted, use a more efficient algorithm
    if is_sorted(input_list):
        duplicates = detect_duplicates_sorted(input_list)

    else:
        duplicates = detect_duplicates_unsorted(input_list)

    return duplicates
