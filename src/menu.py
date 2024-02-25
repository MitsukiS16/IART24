import sys
import os

# Exit Menu Function
def exit_application():
    print("Exiting the application. Goodbye!")
    sys.exit()

# Function Test Yet to be done 
def idkyet():
    print("Not yet implemented")

# Choose Library Menu Function
def choose_library_menu():
    os.system('clear')

    print("----------------------------------------------------")
    print("| Library File Menu                                |")
    print("----------------------------------------------------")
    print("| 1. a_example                                     |")
    print("| 2. b_read_on                                     |")
    print("| 3. c_incunabula                                  |")
    print("| 4. d_tough_choices                               |")
    print("| 5. e_so_many_books                               |")
    print("| 6. f_libraries_of_the_world                      |")
    print("| 0. Main Menu                                     |")
    print("----------------------------------------------------")
    
    choice = input("Please enter your choice: ")

    options = {
        '1': choose_library_menu,
        '2': choose_library_menu,  # Change to correct function name or idkyet
        '0': menu  # Change to correct function name
    }

    selected_option = options.get(choice)

    if selected_option:
        selected_option()  # Call the selected function
    else:
        print("Invalid choice. Please enter a valid option.")
        choose_library_menu()

# Choose Algorithm Menu Function
def choose_algorithm_menu():
    os.system('clear')

    print("----------------------------------------------------")
    print("| Library File Menu                                |")
    print("----------------------------------------------------")
    print("| 1. Algorithm 1                                   |")
    print("| 2. Algorithm 2                                   |")
    print("| 3. Algorithm 3                                   |")
    print("| 0. Main Menu                                     |")
    print("----------------------------------------------------")

    choice = input("Please enter your choice: ")

    options = {
        '1': idkyet,
        '2': idkyet,
        '3': idkyet,
        '0': menu
    }

    selected_option = options.get(choice)

    if selected_option:
        selected_option()
    else:
        print("Invalid choice. Please enter a valid option.")
        choose_algorithm_menu()

# Best Score Menu Function
def best_score_menu():
    os.system('clear')

    print("----------------------------------------------------")
    print("| Best Score Menu                                  |")
    print("----------------------------------------------------")
    print("| 1. ...                                           |")
    print("| 2. ...                                           |")
    print("| 3. ...                                           |")
    print("| 0. Main Menu                                     |")
    print("----------------------------------------------------")
    choice = input("Please enter your choice: ")

    options = {
        '1': idkyet,
        '2': idkyet,
        '3': idkyet,
        '0': menu
    }

    selected_option = options.get(choice)

    if selected_option:
        selected_option()
    else:
        print("Invalid choice. Please enter a valid option.")
        best_score_menu()



# Main menu Function
def menu():
    os.system('clear')

    print("----------------------------------------------------")
    print("| Welcome to our application                       |")
    print("----------------------------------------------------")
    print("| What do you want to do:                          |")
    print("| 1. Choose a library file                         |")
    print("| 2. See the best score for each library           |")
    print("| 0. Exit                                          |")
    print("----------------------------------------------------")
    
    choice = input("Please enter your choice: ")

    options = {
        '1': choose_library_menu,
        '2': best_score_menu,
        '0': exit_application
    }

    selected_option = options.get(choice)

    if selected_option:
        selected_option()
    else:
        print("Invalid choice. Please enter a valid option.")
        menu()
