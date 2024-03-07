########################################
### Initial Solutions
# Random Solution
# Trivial Solution
# Greedy Constrution

### Algorithms to implement
# [Metaheuristic Methods] Genetic [Anotations on PP3]
# [Metaheuristic Methods] Simulated Annealing [Anotations on PP3]
# [Metaheuristic Methods] Tabu Search [Anotations on PP3]
# [Metaheuristic Methods] Guided Local Search [Anotations on PP3]
# [Metaheuristic Methods] Particle Swarm Optimization
# [Iterative Methods] Gradient Descent
# [Iterative Methods] Newton's Method
# [Iterative Methods] Conjugate Gradient Method
# [Analytical Methods] Calculus-based Optimization
# [Analytical Methods] Linear Programming
# [Derivative-Free Optimization] Pattern Search
# [Derivative-Free Optimization] Nelder-Mead Method
# [Derivative-Free Optimization] Evolutionary Strategies

########################################
# Imports 
from library import Library
from pparser import read_data
import evaluate_funcs as ef
import neighbor_funcs as nf
import mutation_funcs as mf
import operators as op
import numpy as np
import random as rand
import copy

########################################
# Global Variables
libraries_shipped = set()
libraries = {}
scores = []
i = 0
books = {}
libID = 0
islib = False
diffbooks = None
numLibs = None
shipping_days = None


########################################
# Function to get the id of the initial solution

# Random initial solution

def generate_random_solution(libraries, diffbooks, shipping_days, libraries_info, libraries_shipped):
    visited_libs = set()
    canShip_libs = set()
    shipped_books = set()
    shipped_books_libraries = set()
    shuffled_libraries = libraries_info.copy()
    rand.shuffle(shuffled_libraries)
    shuffled_libraries_aux = copy.copy(shuffled_libraries)
    randlibID = shuffled_libraries_aux[0]
    randlibSignUp = 0
   
    while shipping_days > 0:

        if len(shipped_books) == diffbooks: 
            libraries_shipped = visited_libs
            return shipped_books_libraries, libraries_shipped
        elif randlibSignUp == 0 and len(shuffled_libraries_aux) > 0:
            canShip_libs.add(randlibID)
            visited_libs.add(randlibID)
            shuffled_libraries_aux.pop(0)
            if(len(shuffled_libraries_aux) > 0):
                randlibID = shuffled_libraries_aux[0]
                randlibSignUp = libraries[randlibID].sign_up_time
        for libID in canShip_libs:
            all_books = set(libraries[libID].books.keys())
            available_books = list(all_books - shipped_books)
            if(len(available_books) == 0): continue
            daily_limit = libraries[libID].shipping_time
            selected_books = np.random.choice(available_books, min(len(available_books), daily_limit), replace=False)
            for book in selected_books:
                shipped_books.add(book)
                shipped_books_libraries.add((book, libID))
        randlibSignUp -= 1
        shipping_days -= 1
   

    libraries_shipped = visited_libs
    return shipped_books_libraries, libraries_shipped
        
        

# Trivial initial solution
def get_trivial_solution():
    print("##################################")
    print("You enter the get_trivial_solution Function")
    print("##################################")

    #TO DO 

    return 0

# Gready initial solution
def get_greedy_solution():
    print("##################################")
    print("You enter the get_greedy_solution Function")
    print("##################################")

    #TO DO 

    return 0

########################################
# Helper function to print algorithm information
def print_info(alg_name,file_path,init_solution_name,score):
    print("-------------------------------------------------------------")
    print(f"| Algorithm: {alg_name}")
    print(f"| File: {file_path}")
    print(f"| Initial Solution: {init_solution_name}")
    print(f"| The final score was: {score}")
    print("-------------------------------------------------------------")

########################################
    
# Auxiliar funcs
    
def generate_population(population_size, shipping_days, numLibs, diffbooks, libraries_shipped, init_solution):
    solutions = []
    for i in range(population_size):
        shipped_books_libraries, libs_shipped = init_solution(shipping_days, numLibs, diffbooks, libraries_shipped)
        solutions.append(shipped_books_libraries)
    return solutions



# Algorithms
    

# Algorithm 3
def genetic_algorithm(file_path,init_solution):
    
    global libraries, books, scores, libraries_shipped

    libraries, books, scores, diffbooks, numLibs, shipping_days = read_data(file_path)


    num_iterations = 20 
    population_size = 10 
    crossover_func = op.midpoint_crossover
    mutation_func = mf.mutation_solution_exchange_book

    
    population = generate_population(population_size, shipping_days, numLibs, diffbooks, libraries_shipped, init_solution)

    best_solution = population[0] # Initial solution
    best_score = ef.evaluate_solution(population[0], scores)
    best_solution_generation = 0 # Generation on which the best solution was found
    
    generation_no = 0

    while(num_iterations > 0):
        
        generation_no += 1

        total_fitness = 0

        for individual in population:
            total_fitness += ef.evaluate_solution(individual, scores)
        
        tournament_winner_sol = ef.tournament_select(population, 10, scores)
        roulette_winner_sol = ef.roulette_select(population, total_fitness, scores)
        
        # Crossover
        offspring = crossover_func(tournament_winner_sol, roulette_winner_sol)

        # Mutation
        mutated_offspring = [mutation_func(child, libraries_shipped, libraries) for child in offspring]

        # Evaluate and integrate offspring into the population
        # This step depends on your population management strategy
        population = ef.replace_worst_individuals(population, mutated_offspring, scores)
        
        # Checking the greatest fit among the current population
        greatest_fit = ef.get_greatest_fit(population, scores)
        greatest_fit_score = ef.evaluate_solution(greatest_fit, scores)
        if greatest_fit_score > best_score:
            best_solution = greatest_fit
            best_score = greatest_fit_score
            best_solution_generation = generation_no
        else:
            num_iterations -= 1

    print(best_solution_generation)
   
    return best_solution, best_score, scores



# Algorithm 2
def tabu_search(file_path,init_solution):   

    global libraries, books, scores, libraries_shipped

    libraries, books, scores, diffbooks, numLibs, shipping_days = read_data(file_path)

    
    shipped_books_libraries, libraries_shipped = init_solution(libraries, diffbooks, shipping_days)

    num_iterations = 100

    best_sol = list(shipped_books_libraries)
    tabu_set = set()
    while num_iterations > 0:
        neighbor_sol = nf.neighbor_solution_exchange_book(best_sol, libraries_shipped, libraries)
        if tuple(neighbor_sol) not in tabu_set:
            tabu_set.add(tuple(neighbor_sol))
            if ef.evaluate_solution(shipped_books_libraries, scores) < ef.evaluate_solution(neighbor_sol, scores):
                best_sol = neighbor_sol
        num_iterations -= 1
    
    return best_sol, ef.evaluate_solution(best_sol, scores), scores





# Algorithm 1
def get_sa_solution(file_path,init_solution):   

    global libraries, books, scores, libraries_shipped

    libraries, scores, diffbooks, shipping_days , libraries_info= read_data(file_path)

    
    shipped_books_libraries, libraries_shipped = init_solution(libraries, diffbooks, shipping_days, libraries_info, libraries_shipped)


    num_iterations = 10
    iteration = 0
    temperature = 1000

    cooling_rate = 0.999

    best_score = ef.evaluate_solution(shipped_books_libraries, scores)

    eval_scores = []

    eval_scores.append(best_score)
    
    best_solution = list(shipped_books_libraries)


    if(best_score == sum(int(s) for s in scores)): return best_solution, libraries_shipped, eval_scores

    while iteration < num_iterations :

        temperature *= cooling_rate
        iteration += 1
        

        neighbor_score = best_score
        
        neighbor , neighbor_score = nf.neighbor_solution_exchange_book(best_solution, libraries_shipped, libraries, neighbor_score)
    
        eval = neighbor_score - best_score


        if eval >= 0:
            best_solution = neighbor
            best_score = neighbor_score
        elif(np.exp(eval/temperature) >= np.random.uniform(0, 1 + np.finfo(float).eps)):
            best_solution = neighbor
            best_score = neighbor_score
            
            
            iteration -= 1

        eval_scores.append(best_score)


    return best_solution, libraries_shipped, eval_scores




