from utils.functions import is_sorted


def detect_duplicates_unsorted(input_list=None):
    # Time complexity of O(n^3), where n is the number of elements in the list
    duplicates = []
    for item in input_list:
        # .count() will internally scan the list, giving time complexity O(n) on its own
        # "in" operator has O(n) complexity for lists
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
        # print("The input list is sorted")
        # Measuring execution time with O(nlogn) time complexity
        # print("Executing  with O(n) time complexity...")
        # start_time = time.time()
        duplicates = detect_duplicates_sorted(input_list)
        # end_time = time.time()
        # print("Duplicates O(n)", duplicates)
        # print("Time taken O(n):", end_time - start_time, "seconds\n")
    # If not sorted
    else:
        # Measuring execution time with O(n^3) time complexity
        # print("Executing with O(n^3) time complexity...")
        # start_time = time.time()
        duplicates = detect_duplicates_unsorted(input_list)
        # end_time = time.time()
        # print("Duplicates O(n^3):", duplicates)
        # print("Time taken O(n^3):", end_time - start_time, "seconds")

        # print("List has ", len(duplicates), " duplicates.\n")

    return duplicates
