import os
import ast
from detect_duplicates import detect_duplicates


def get_list():
    # Function to get the list from the user
    default_list = ["b", "a", "c", "c", "e", "a", "c", "d", "c", "d"]  # Default example list

    # Repeat until a valid list is given
    while True:
        user_input = input(
            "Do you want to use the default list: ['b', 'a', 'c', 'c', 'e', 'a', 'c', 'd', 'c', 'd'] ? (y/n): "
        ).lower()

        if user_input == "y":  # User wants to use the default list
            return default_list

        elif user_input == "n":  # User wants to create a custom list

            while True:
                user_list_str = input("Enter a list of elements: ")
                try:
                    user_list = ast.literal_eval(user_list_str)  # evaluates a specific subset of Python literals - safer
                    if not isinstance(user_list, list):
                        print("Invalid input! Please provide a list with any type of elements.")
                    else:
                        return user_list
                except (ValueError, SyntaxError):
                    print("Invalid input! Please provide a valid Python list.")
        else:
            print("Invalid input! Please enter 'y' or 'n.'")


def save_list(input_list, filepath):
    # Function to save the input_list in a .txt file
    with open(filepath, 'w') as file:
        for item in input_list:
            file.write(str(item) + '\n')


def main():

    print('Running exercise 1 for the duplicate element detection...\n')
    print("Please provide a comma-separated list of objects.\n")
    valid_list = get_list()

    duplicates = detect_duplicates(valid_list)
    print("List has ", len(duplicates), " duplicates:", duplicates)

    # Save duplicates list to a text file
    output_directory = "../output"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    output_filepath = os.path.join(output_directory, "duplicates.txt")
    save_list(duplicates, output_filepath)
    print("Duplicates saved to:", output_filepath)


if __name__ == "__main__":
    main()
