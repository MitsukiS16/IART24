########################################
# Imports 
import sys
import os
import time
import matplotlib.pyplot as plt
from pparser import write_data
from tabulate import tabulate

from generators import generate_random_solution, generate_trivial_solution
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

rs = "Random Solution"
ts = "Trivial Solution"

INITIAL_SOLUTIONS = {
    '1': (generate_random_solution, rs),
    '2': (generate_trivial_solution, ts)
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
def error_handling_input():
    print("Invalid option.")
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
        print(f"{key}. {value[1]}")
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
    if input_file not in INPUT_FILES:
        error_handling_input()

    init_solution = select_initial_population()
    if init_solution not in INITIAL_SOLUTIONS:
        error_handling_input()
        
    selected_algorithm_key = select_algorithm()
    if selected_algorithm_key not in ALGORITHMS:
        error_handling_input()


    selected_algorithm = ALGORITHMS.get(selected_algorithm_key)

    start_time = time.time() # Start time 

    best_solution, libraries_shipped, eval_scores = selected_algorithm[0](INPUT_FILES[input_file], INITIAL_SOLUTIONS[init_solution][0])  
    
    end_time = time.time() # End time
    elapsed_time = end_time - start_time 

    update_data(selected_algorithm_key, input_file, init_solution, eval_scores, best_solution, libraries_shipped,elapsed_time)
    
    print_info(selected_algorithm, input_file, init_solution, eval_scores, elapsed_time)

    choice = input("Press 1 for showing the graph of the algorithm; Press 0 for main menu.\n")
    if choice == '1':
        draw_graph(eval_scores)
    menu()


def update_data(selected_algorithm_key, input_file, init_solution, eval_scores, best_solution, libraries_shipped, elapsed_time):
    if isinstance(eval_scores, list):
        max_score = max(eval_scores)
    else:
        max_score = eval_scores

    # Arredonda o tempo para 5 casas decimais se for menor que 1, caso contrário, exibe como inteiro
    if elapsed_time < 1:
        elapsed_time_rounded = round(elapsed_time, 5)
    else:
        elapsed_time_rounded = int(elapsed_time)

    with open('best_score.txt', 'r') as f:
        lines = f.readlines()

    file_name = INPUT_FILES[input_file].split('/')[-1]
    init_solution_name = INITIAL_SOLUTIONS[init_solution][1]
    algorithm_name = ALGORITHMS[selected_algorithm_key][1]

    for i, line in enumerate(lines[1:], start=1):  
        data = line.strip().split(',')
        if int(i) == int(input_file):  
            old_score = int(data[3])
            old_time = float(data[4])
            if max_score > old_score or (max_score == old_score and elapsed_time < old_time): 
                lines[i] = f"{file_name}, {init_solution_name}, {algorithm_name}, {max_score}, {elapsed_time_rounded}\n"
                break
    
    with open('best_score.txt', 'w') as f:
        f.writelines(lines)

    INITIAL_SOLUTIONS[input_file] = (INITIAL_SOLUTIONS[init_solution][0], init_solution)
    ALGORITHMS[input_file] = ALGORITHMS[selected_algorithm_key]

    write_data(f'{OUTPUT_FILES[input_file]}', best_solution, libraries_shipped)


# Helper function to print algorithm information
def print_info(alg_name, file_path, type_initial_population, eval_scores, time_taken):
    clear_screen()
    print("--------------------------------------------------------------------------------")
    print(f"Algorithm: {alg_name[1]}")
    print(f"File: {file_path}")
    print(f"Initial Solution: {type_initial_population}")
    
    if isinstance(eval_scores, list):
        max_score = max(eval_scores)
    else:
        max_score = eval_scores
        
    print(f"The final score was: {max_score}")  
    print(f"Time taken: {time_taken:.6f} seconds")
    print("--------------------------------------------------------------------------------")


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
    print("--------------------------------------------------------------------------------")
    print("Welcome to our application")
    print("--------------------------------------------------------------------------------")
    print("What do you want to do:")
    print("1. Book Scanning")
    print("2. See the best score for each library")
    print("0. Exit")
    print("--------------------------------------------------------------------------------")
    
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
