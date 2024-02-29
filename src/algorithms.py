# Algorithm Functions

# Sugestoes de algoritmos para implementar: (5 primeiros +importantes, os outros fazemos dependendo do tempo que temos :P)

# Gready 
# Random Neighbour
# [Metaheuristic Methods] Genetic
# [Metaheuristic Methods] Simulated Annealing
# [Metaheuristic Methods] Particle Swarm Optimization
# [Iterative Methods] Gradient Descent
# [Iterative Methods] Newton's Method
# [Iterative Methods] Conjugate Gradient Method
# [Analytical Methods] Calculus-based Optimization
# [Analytical Methods] Linear Programming
# [Derivative-Free Optimization] Pattern Search
# [Derivative-Free Optimization] Nelder-Mead Method
# [Derivative-Free Optimization] Evolutionary Strategies

# Escolher um algoritmos, criar o codigo e ver score :) simples :P

########################################
# Imports 
from library import Library
from pparser import read_data_file
import numpy as np
import copy

########################################
# Global Variables
# libraries_shipped = set()
libraries = {}
scores = []
numLibs = None

# libraries = {}
# books = {}
# libraries_shipped = set()
# scores = []
# libID = 0
# islib = False
# diffbooks = None
# numLibs = None
# shipping_days = None

########################################
# Main and Auxiliar Functions for Optimization Algorithms

# Algorithm 1
def algorithm1(file):


    libraries_shipped = set()

    libs, diffbooks, nlibs, shipping_days, scs = read_data_file(file)

    global libraries 
    libraries = libs

    global numLibs 
    numLibs = nlibs

    global scores
    scores = scs

    #print(scores)

    #print(random_sign_up())
    
    alg_name = "*name alg 1*"
    print("hello")
    solution , libs_shipped = generate_random_solution(shipping_days, numLibs, diffbooks, libraries_shipped)
    final_score = evaluate_solution(solution)
    print(final_score)
    #print_info(alg_name, file, final_score)


# Helper function to print algorithm information
def print_info(alg_name, input_file):
    print("-------------------------------------------------------------")
    print(f"| Algorithm {alg_name} selected for file {input_file}:")
    print("| The total score was: {score}")
    print("-------------------------------------------------------------")


# Random sign up function
def random_sign_up():
    print(numLibs)
    return np.random.randint(0, 2)


# Function to get book scores
def get_book_scores(shipped_books):
    book_scores = []
    for book in shipped_books:
        book_scores.append(scores[int(book)])
    return book_scores


# Neighbor solution function
def neighbor_solution(solution, libraries_shipped):
    book = np.random.choice(list(solution))
    sol_len = len(solution)
    solution.remove(book)
    for library in libraries_shipped:
        keys = list(libraries[library].books.keys())
        if int(book) in keys:
            available_books = [b for b in keys if b != int(book) and str(b) not in solution]
            if available_books:
                new_book = np.random.choice(available_books)
                solution.add(str(new_book))
                break
    if sol_len > len(solution):
        solution.add(book)
    return solution


# Generate random solution function
def generate_random_solution(shipping_days, numLibs, diffbooks, libraries_shipped):
    visited_libs = set()
    canShip_libs = set()
    shipped_books = set()
    randlibID = random_sign_up()
    visited_libs.add(randlibID)
    canShip_libs.add(randlibID)
    shipping_days -= libraries[randlibID].sign_up_time
    randlibSignUp = 0
    while shipping_days > 0:
        if randlibSignUp == 0:
            if len(visited_libs) < numLibs:
                while True:
                    randlibID = random_sign_up()
                    if randlibID not in visited_libs:
                        visited_libs.add(randlibID)
                        randlibSignUp = libraries[randlibID].sign_up_time
                        break
            if randlibID not in canShip_libs:
                canShip_libs.add(randlibID)
        for libid in canShip_libs:
            sameDayShipping = libraries[libid].shipping_time
            book_keys_list = list(libraries[libid].books.keys())
            if not book_keys_list:
                continue
            else:
                while sameDayShipping > 0:
                    if diffbooks == len(shipped_books):
                        libraries_shipped = copy.deepcopy(visited_libs)
                        return shipped_books, libraries_shipped
                    else:
                        random_key = np.random.choice(book_keys_list)
                        if random_key not in shipped_books:
                            shipped_books.add(random_key)
                            sameDayShipping -= 1
        randlibSignUp -= 1
        shipping_days -= 1
    libraries_shipped = copy.deepcopy(visited_libs)
    return shipped_books, libraries_shipped

    
# Simulated Annealing solution function
def get_sa_solution(num_iterations, shipping_days, numLibs, diffbooks, libraries_shipped):
    iteration = 0
    temperature = 1000
    cooling_rate = 0.999
    solution, libraries_shipped = generate_random_solution(shipping_days, numLibs, diffbooks, libraries_shipped)
    score = evaluate_solution(solution)
    best_solution = copy.deepcopy(solution)
    best_score = score
    while iteration < num_iterations:
        temperature *= cooling_rate
        iteration += 1
        neighbor = neighbor_solution(best_solution, libraries_shipped)
        neighbor_score = evaluate_solution(neighbor)
        eval = neighbor_score - best_score
        if eval > 0:
            best_solution = neighbor
            best_score = neighbor_score
        elif np.exp(eval/temperature) >= np.random.rand():
            best_solution = neighbor
            best_score = neighbor_score
    return best_solution


# Function to evaluate solution
def evaluate_solution(solution):
    score = 0
    for arg in solution:
        score += int(arg)
    return score

