########################################
# Imports 
import sys
import os

from algorithms import algorithm1
from algorithms import algorithm2
from algorithms import algorithm3


# Exit Menu Function
def exit_application():
    print("Exiting the application. Goodbye!")
    sys.exit()


# Book Scanning Menu Function
def book_scanning_menu():
    os.system('clear')

    print("-------------------------------------------------------------")
    print("| Book Scanning Menu                                        |")
    print("-------------------------------------------------------------")
    print("| Please select an input file :                             |")
    print("| 1. a_example                                              |")
    print("| 2. b_read_on                                              |")
    print("| 3. c_incunabula                                           |")
    print("| 4. d_tough_choices                                        |")
    print("| 5. e_so_many_books                                        |")
    print("| 6. f_libraries_of_the_world                               |")
    print("| 0. Main Menu                                              |")
    print("-------------------------------------------------------------")
    inputfile = input("Please enter your choice: ")

    file_paths = {
        '1': "../libraries/a_example.txt",
        '2': "../libraries/b_read_on.txt",
        '3': "../libraries/c_incunabula.txt",
        '4': "../libraries/d_tough_choices.txt",
        '5': "../libraries/e_so_many_books.txt",
        '6': "../libraries/f_libraries_of_the_world.txt",
        '0': "0"
    }

    if inputfile in file_paths:
        print("-------------------------------------------------------------")
        print("| Please select the initial solution:                       |")
        print("| 1. Random Solution                                        |")
        print("| 2. Trivial Solution                                       |")
        print("| 3. Greedy Constrution                                     |")
        print("| 0. Main Menu                                              |")
        print("-------------------------------------------------------------")
        init_solution = input("Please enter your choice: ")

        sol_name = {
        '1': "Random Solution",
        '2': "Trivial Solution",
        '3': "Greedy Constrution",
        '0': "0"
    }

        print("-------------------------------------------------------------")
        print("| Please select the algorithm:                              |")
        print("| 1. Algorithm 1                                            |")
        print("| 2. Algorithm 2                                            |")
        print("| 3. Algorithm 3                                            |")
        print("| 0. Main Menu                                              |")
        print("-------------------------------------------------------------")
        inputalgorithm = input("Please enter your choice: ")

        options = {
            '1': algorithm1,
            '2': algorithm2,
            '3': algorithm3,
            '0': menu
        }

        selected_algorithm = options.get(inputalgorithm)

        if selected_algorithm:
            selected_algorithm(file_paths[inputfile],init_solution,sol_name[init_solution])  # Pass the file path directly
            choice = input("Press 0 to go back to main menu.\n")
            if choice == '0':
                menu()
            else:
                print("Invalid choice. Please enter a valid option.")
                best_score_menu()
        else:
            print("Invalid choice. Please enter a valid option.")
            book_scanning_menu()
    elif inputfile == '0':
        menu()
    else:
        print("Invalid choice. Please enter a valid option.")
        book_scanning_menu()



# Best Score Menu Function
def best_score_menu():
    os.system('clear')

    print("--------------------------------------------------------------------------------")
    print("| Best Score Menu                                                              |")
    print("--------------------------------------------------------------------------------")
    print("| File                      | Score       | Initial Solution | Algorithm       |")
    print("| a_example                 | 000 000 000 | -                | -               |")
    print("| b_read_on                 | 000 000 000 | -                | -               |")
    print("| c_incunabula              | 000 000 000 | -                | -               |")
    print("| d_tough_choices           | 000 000 000 | -                | -               |")
    print("| e_so_many_books           | 000 000 000 | -                | -               |")
    print("| f_libraries_of_the_world  | 000 000 000 | -                | -               |")
    print("--------------------------------------------------------------------------------")

    choice = input("Press 0 to go back to main menu.\n")
    if choice == '0':
        menu()
    else:
        print("Invalid choice. Please enter a valid option.")
        best_score_menu()


# Main menu Function
def menu():
    os.system('clear')

    print("-------------------------------------------------------------")
    print("| Welcome to our application                                |")
    print("-------------------------------------------------------------")
    print("| What do you want to do:                                   |")
    print("| 1. Book Scanning                                          |")
    print("| 2. See the best score for each library                    |")
    print("| 0. Exit                                                   |")
    print("-------------------------------------------------------------")
    
    choice = input("Please enter your choice: ")

    options = {
        '1': book_scanning_menu,
        '2': best_score_menu,
        '0': exit_application
    }

    selected_option = options.get(choice)

    if selected_option:
        selected_option()
    else:
        print("Invalid choice. Please enter a valid option.")
        menu()
