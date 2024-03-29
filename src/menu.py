########################################
# Imports 
import sys
import os
import time
import matplotlib.pyplot as plt
from pparser import write_data
from tabulate import tabulate

from algorithms import generate_random_solution
from algorithms import genetic_algorithm, tabu_search, get_sa_solution, hill_climbing_algorithm

########################################
# Global Libraries

INPUT_FILES = {
    '1': '../input/a_example.txt',
    '2': '../input/b_read_on.txt',
    '3': '../input/c_incunabula.txt',
    '4': '../input/d_tough_choices.txt',
    '5': '../input/e_so_many_books.txt',
    '6': '../input/f_libraries_of_the_world.txt'
}

OUTPUT_FILES = {
    '1': '../output/a_example.txt',
    '2': '../output/b_read_on.txt',
    '3': '../output/c_incunabula.txt',
    '4': '../output/d_tough_choices.txt',
    '5': '../output/e_so_many_books.txt',
    '6': '../output/f_libraries_of_the_world.txt'
}

INITIAL_SOLUTIONS = {
    '1': generate_random_solution,
    '2': "trivial_population",
    # add more
}

sa = "Simulated Annealing"
ts = "Tabu Search"
ga = "Genetic Algorithm"
hc = "Hill Climbing Algorithm"

ALGORITHMS =  {
    '1': (get_sa_solution, sa),
    '2': (tabu_search, ts),
    '3': (genetic_algorithm, ga),
    '4': (hill_climbing_algorithm, hc)
    # add more
}



########################################
# Auxiliar Functions

# Clear screen
def clear_screen():
    os.system('clear')

# Exit Menu Function
def exit_application():
    print("Exiting the application. Goodbye!")
    sys.exit()

# Input Handling Function
def error_handling_input(input):
    if input not in INPUT_FILES and input not in INITIAL_SOLUTIONS and input not in ALGORITHMS: 
        print("Invalid choice. Please enter a valid option.")
        input("Press Enter to continue...")
        return book_scanning_menu()


########################################
def select_input_files():
    clear_screen()
    print("Please select an input file:")
    for key, value in INPUT_FILES.items():
        print(f"{key}. {value.split('/')[-1]}")
    print("-------------------------------------------------------------")
    choice = input("Please enter your choice: ")
    return choice
        

def select_initial_population():
    clear_screen()
    print("Please select initial population:")
    for key, value in INITIAL_SOLUTIONS.items():
        print(f"{key}. {value}")
    print("-------------------------------------------------------------")
    choice = input("Please enter your choice: ")
    return choice


def select_algorithm():
    clear_screen()
    print("Please select an algorithm:")
    for key, value in ALGORITHMS.items():
        print(f"{key}. {value[1]}")  
    print("-------------------------------------------------------------")
    choice = input("Please enter your choice: ")
    return choice



def draw_graph(eval_scores):
    x_positions = range(len(eval_scores))

    # Plotting
    plt.bar(x_positions, eval_scores, edgecolor='black')

    # Set the title and labels
    plt.title('Score Variation per Instance')
    plt.xlabel('Instance')
    plt.ylabel('Score Value')

    # Set x-ticks to be the position of each score
    plt.xticks(rotation=90)

    # Optionally, adjust the y-axis to better show variations in scores
    plt.ylim(min(eval_scores) - 10, max(eval_scores) + 10)  # Adjust as needed for visibility

    plt.show()


def book_scanning_menu():
    os.system('clear')

    input_file = select_input_files()
    error_handling_input(input_file)

    init_solution = select_initial_population()
    error_handling_input(init_solution)

    selected_algorithm_key = select_algorithm()
    error_handling_input(selected_algorithm_key)

    selected_algorithm = ALGORITHMS.get(selected_algorithm_key)

    start_time = time.time() # Start time 

    best_solution, libraries_shipped, eval_scores = selected_algorithm[0](INPUT_FILES[input_file], INITIAL_SOLUTIONS[init_solution])  
    write_data(f'{OUTPUT_FILES[input_file]}', best_solution, libraries_shipped)
        
    end_time = time.time() # End time
    elapsed_time = end_time - start_time 

    print_info(selected_algorithm, input_file, init_solution, eval_scores, elapsed_time)

    choice = input("Press 1 for showing the graph of the algorithm; Press 0 for main menu.\n")
    if choice == '1':
        draw_graph(eval_scores)
    menu()



# Helper function to print algorithm information
def print_info(alg_name, file_path, type_initial_population, eval_scores, time_taken):
    clear_screen()
    print("-------------------------------------------------------------")
    print(f"Algorithm: {alg_name}")
    print(f"File: {file_path}")
    print(f"Initial Solution: {type_initial_population}")
    print(f"The final score was: {eval_scores}")
    print(f"Time taken: {time_taken:.6f} seconds")
    print("-------------------------------------------------------------")


# Get and Print Content of Best Score Menu Function
def get_content_best_score():
    with open('best_score.txt', 'r') as f:
        lines = f.readlines()

    # Initialize table headers and rows
    headers = ['File', 'Initial Solution', 'Algorithm', 'Score', 'Time (sec)']
    rows = []

    # Skip the first line (header)
    lines = lines[1:]

    # Parse each line and extract relevant information
    for line in lines:
        file_name, initial_solution, algorithm, score, time = line.strip().split(',')
        rows.append([file_name.strip(), initial_solution.strip(), algorithm.strip(), int(score), float(time)])

    return tabulate(rows, headers=headers)


# Best Score Menu Function
def best_score_menu():
    clear_screen()

   # Print Init UI
    print("--------------------------------------------------------------------------------")
    print("Best Score Menu                                                              ")
    print("--------------------------------------------------------------------------------")
    print(get_content_best_score())
    print("--------------------------------------------------------------------------------")
    input("Press Enter to continue...")
    menu()


# Main menu Function
def menu():
    clear_screen()

   # Print Init UI
    print("-------------------------------------------------------------")
    print("Welcome to our application")
    print("-------------------------------------------------------------")
    print("What do you want to do:")
    print("1. Book Scanning")
    print("2. See the best score for each library")
    print("0. Exit")
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
        input("Press Enter to continue...")
        menu()
