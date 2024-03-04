########################################
# Imports 
import sys
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np

import algorithms as algo


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
        '1': algo.generate_random_solution,
        '2': "Trivial Solution",
        '3': "Greedy Constrution",
        '0': "0"
    }
        sa = "Simulated Annealing"
        ts = "Tabu Search"
        ga = "Genetic Algorithm"

        print("-------------------------------------------------------------")
        print("| Please select the algorithm:                              |")
        print("| 1. Simulated Annealing                                    |")
        print("| 2. Tabu Search                                            |")
        print("| 3. Genetic Algorithm                                      |")
        print("| 0. Main Menu                                              |")
        print("-------------------------------------------------------------")
        inputalgorithm = input("Please enter your choice: ")

        options = {
            '1': (algo.get_sa_solution, sa),
            '2': (algo.tabu_search, ts),
            '3': (algo.genetic_algorithm, ga),
            '0': menu
        }

        selected_algorithm = options.get(inputalgorithm)

        if selected_algorithm:
            best_solution , best_score, scores = selected_algorithm[0](file_paths[inputfile],sol_name[init_solution])  # Pass the file path directly
            total = 0
            for s in scores:
                total += int(s)

            print(total)
            print(best_score)
            choice = input("Select 0 for main menu or 1 to draw graph of 10 solutions.\n")
            if choice == '0':
                menu()
            elif choice == '1':
                best_solution1 , best_score1, scores1 = selected_algorithm[0](file_paths[inputfile],sol_name[init_solution]) 
                best_solution2 , best_score2, scores2 = selected_algorithm[0](file_paths[inputfile],sol_name[init_solution]) 
                best_solution3 , best_score3, scores3 = selected_algorithm[0](file_paths[inputfile],sol_name[init_solution]) 
                best_solution4 , best_score4, scores4 = selected_algorithm[0](file_paths[inputfile],sol_name[init_solution]) 
                best_solution5 , best_score5, scores5 = selected_algorithm[0](file_paths[inputfile],sol_name[init_solution]) 
                best_solution6 , best_score6, scores6 = selected_algorithm[0](file_paths[inputfile],sol_name[init_solution]) 
                best_solution7 , best_score7, scores7 = selected_algorithm[0](file_paths[inputfile],sol_name[init_solution]) 
                best_solution8, best_score8, scores8 = selected_algorithm[0](file_paths[inputfile],sol_name[init_solution]) 
                best_solution9 , best_score9, scores9 = selected_algorithm[0](file_paths[inputfile],sol_name[init_solution]) 
                best_solution10 , best_score10, scores10 = selected_algorithm[0](file_paths[inputfile],sol_name[init_solution]) 

                scores = np.array([best_score1, best_score2, best_score3, best_score4, best_score5, best_score6, best_score7, best_score8, best_score9, best_score10])

                min_score = scores.min()
                max_score = scores.max() + 1
                bin_size = 10000
                bins = np.arange(min_score, max_score, bin_size)
                plt.hist(scores, bins=bins, edgecolor= 'black')

                plt.title(selected_algorithm[1])
                plt.xlabel('Score Intervals')
                plt.ylabel('Number of Algorithm Calls')

                plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

                plt.show()

                choice = input("Select 0 for main menu.\n")
                if choice == '0':
                    menu()

            else:
                print("Invalid choice. Please enter a valid option.")
                best_score_menu()
        else:
            print("Invalid choice. Please enter a valid option.")
            best_scanning_menu()
    elif inputfile == '0':
        menu()
    else:
        print("Invalid choice. Please enter a valid option.")
        best_scanning_menu()



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
