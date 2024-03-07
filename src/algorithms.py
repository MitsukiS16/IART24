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
from pparser import read_data
import hashlib
import collections
import evaluate_funcs as ef
import neighbor_funcs as nf
import mutation_funcs as mf
import operators as op
import numpy as np
import math as m
import random as rand
import copy

########################################
#Global Variables

DataContainer = collections.namedtuple('DataContainer', ['libraries', 'scores', 'diffbooks', 'shipping_days', 'libraries_info'])


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
    
def generate_population(population_size, libraries, diffbooks, shipping_days, libraries_info, libraries_shipped, init_solution):
    solutions = []
    for i in range(population_size):
        shipped_books_libraries, libraries_shipped = init_solution(libraries, diffbooks, shipping_days, libraries_info, libraries_shipped)
        solutions.append(list(shipped_books_libraries))
    return solutions



# Algorithms
    

# Algorithm 3
def genetic_algorithm(file_path,init_solution):
    
    libraries_shipped = set()

    data = DataContainer(*read_data(file_path))
    
    population_size = 10

    population = generate_population(population_size , data.libraries, data.diffbooks, data.shipping_days, data.libraries_info, libraries_shipped, init_solution)


    crossover_func = op.midpoint_crossover
    mutation_func = mf.mutation_solution_exchange_book
    fit_func = ef.get_greatest_fit

    best_solution = population[0] # Initial solution
    best_score = 0
    best_solution_generation = 0 # Generation on which the best solution was found
    num_iterations = 1000
    generation_no = 0

    eval_scores = []

    while(num_iterations > 0):
        population_fitness = sum(ef.evaluate_solution(individual, data.scores) for individual in population)
        generation_no += 1
        new_population = []
        visited_parents = set()
        
        print(len(population))
        for i in range(0, m.floor(len(population)/2)):
                if(len(new_population) == population): break
                #print("in")
                total_fitness = sum(ef.evaluate_solution(individual, data.scores) for individual in population)
                tournament_winner_sol = ef.tournament_select(population, 10, data.scores, visited_parents)
                roulette_winner_sol = ef.roulette_select(population, total_fitness, data.scores, visited_parents)
                #visited_parents.add(tuple(tournament_winner_sol))
                #visited_parents.add(tuple(roulette_winner_sol))
                offspring = crossover_func(tournament_winner_sol, roulette_winner_sol)           
                for child in offspring:
                    new_population.append(child)

        # Crossover

        if(rand.random() <= 0.2):
            # Mutation
            results = [(mutation_func(child, libraries_shipped, data.libraries, ef.evaluate_solution(child, data.scores))) for child in new_population]
            
            mutated_offspring, mutated_scores = zip(*results)

            mutated_offspring = list(mutated_offspring)
            mutated_scores = list(mutated_scores)

            # Evaluate and integrate offspring into the population
            # This step depends on your population management strategy
            new_population = ef.replace_worst_individuals(new_population, mutated_offspring, data.scores)
        
        # Checking the greatest fit among the current population
        new_total_fitness = sum(ef.evaluate_solution(individual, data.scores) for individual in new_population)
        
        if new_total_fitness > population_fitness:
            greatest_fit = fit_func(new_population, data.scores)
           
            best_solution = greatest_fit
            #best_solution = greatest_fit
            #best_score = greatest_fit_score
            #best_solution_generation = generation_no
            best_score = ef.evaluate_solution(greatest_fit, data.scores)
            population = new_population
            best_solution_generation = generation_no
        else:
            greatest_fit = fit_func(population, data.scores)
           
            best_solution = greatest_fit
            best_score = ef.evaluate_solution(greatest_fit, data.scores)

        #print(num_iterations)
        num_iterations -= 1
        eval_scores.append(best_score)

    #print(best_solution_generation)
   
    return  best_solution, libraries_shipped, eval_scores



# Algorithm 2
def tabu_search(file_path,init_solution):   

    libraries_shipped = set()

    data = DataContainer(*read_data(file_path))
    
    shipped_books_libraries, libraries_shipped = init_solution(data.libraries, data.diffbooks, data.shipping_days, data.libraries_info, libraries_shipped)

    num_iterations = 1000
    tabu_tenure = 10

    eval_scores = []

    tabu_deque = collections.deque()

    best_score = ef.evaluate_solution(shipped_books_libraries, data.scores)
    best_sol = list(shipped_books_libraries)
    for current_iter in range(num_iterations):
        neighbor_score = best_score
        neighbor_sol, neighbor_score = nf.neighbor_solution_exchange_book(best_sol, libraries_shipped, data.libraries, neighbor_score)
        str_neighbor = ','.join(map(str,neighbor_sol))
        hashed_neighbor = hashlib.md5(str_neighbor.encode()).hexdigest()
        if not any(hashed_neighbor == hash for hash, _ in tabu_deque):
            tabu_deque.append((hashed_neighbor,current_iter))
            if best_score < neighbor_score:
                best_sol = neighbor_sol
                best_score = neighbor_score
        while tabu_deque and current_iter - tabu_deque[0][1] > tabu_tenure:
            tabu_deque.popleft()
        eval_scores.append(best_score)
    
    return best_sol, libraries_shipped, eval_scores





# Algorithm 1
def get_sa_solution(file_path,init_solution):   

    libraries_shipped = set()

    data = DataContainer(*read_data(file_path))
    
    shipped_books_libraries, libraries_shipped = init_solution(data.libraries, data.diffbooks, data.shipping_days, data.libraries_info, libraries_shipped)


    num_iterations = 1000
    iteration = 0
    temperature = 1000

    cooling_rate = 0.9999

    best_score = ef.evaluate_solution(shipped_books_libraries, data.scores)

    eval_scores = []

    eval_scores.append(best_score)
    
    best_solution = list(shipped_books_libraries)


    if(best_score == sum(int(s) for s in data.scores)): return best_solution, libraries_shipped, eval_scores

    while iteration < num_iterations :

        temperature *= cooling_rate
        iteration += 1
        

        neighbor_score = best_score
        
        neighbor , neighbor_score = nf.neighbor_solution_exchange_book(best_solution, libraries_shipped, data.libraries, neighbor_score)
    
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




