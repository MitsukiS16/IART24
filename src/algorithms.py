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

def generate_random_solution(shipping_days, numLibs, diffbooks, libraries_shipped):
    visited_libs = set()
    canShip_libs = set()
    shipped_books = set()
    shipped_books_libraries = set()
    randlibID = op.random_sign_up(numLibs)
    visited_libs.add(randlibID)
    canShip_libs.add(randlibID)
    shipping_days -= libraries[randlibID].sign_up_time
    randlibSignUp = 0
    while shipping_days > 0:
        if randlibSignUp == 0:
            # print(f"visited libs LEN: {len(visited_libs)}")
            # print(f"visited libs : {visited_libs}")
            if len(visited_libs) < numLibs:
                while True:
                    randlibID = op.random_sign_up(numLibs)
                    if randlibID not in visited_libs:
                        visited_libs.add(randlibID)
                        randlibSignUp = libraries[randlibID].sign_up_time
                        break  
            if randlibID not in canShip_libs:
                canShip_libs.add(randlibID)
        for libid in canShip_libs:
            #print(f"shipped books: {shipped_books}")
            sameDayShipping = libraries[libid].shipping_time
            book_keys_list = list(libraries[libid].books.keys())
            if not book_keys_list : continue
            else: 
                while sameDayShipping > 0:
                    if(diffbooks == len(shipped_books)): 
                        libraries_shipped = copy.deepcopy(visited_libs)
                        return shipped_books_libraries, libraries_shipped
                    else :
                        random_key = np.random.choice(book_keys_list)
                        if random_key not in shipped_books:
                            shipped_books.add(random_key)
                            shipped_books_libraries.add((random_key,libid))
                            sameDayShipping -= 1
                
        
        #print(f"shipping_days: {shipping_days}")
        randlibSignUp -= 1
        shipping_days -= 1

    libraries_shipped = copy.deepcopy(visited_libs)
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

    
    shipped_books_libraries, libraries_shipped = init_solution(shipping_days, numLibs, diffbooks, libraries_shipped)

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

    libraries, books, scores, diffbooks, numLibs, shipping_days = read_data(file_path)

    
    shipped_books_libraries, libraries_shipped = init_solution(shipping_days, numLibs, diffbooks, libraries_shipped)

    num_iterations = 100
    iteration = 0
    temperature = 100
    cooling_rate = 0.999

    best_score = ef.evaluate_solution(shipped_books_libraries, scores)
    
    best_solution = copy.deepcopy(shipped_books_libraries)

    while iteration < num_iterations :
        # Test with different cooling schedules
        temperature *= cooling_rate
        iteration += 1
        
        neighbor = nf.neighbor_solution_exchange_book(list(best_solution), libraries_shipped, libraries)

        neighbor_score = ef.evaluate_solution(neighbor, scores)

        eval = neighbor_score - best_score

        if eval > 0:
            best_solution = neighbor
            best_score = neighbor_score
        elif(np.exp(eval/temperature) >= np.random.rand()):
            best_solution = neighbor
            best_score = neighbor_score

    return best_solution, best_score, scores


