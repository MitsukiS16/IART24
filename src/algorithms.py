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
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from pparser import read_data
import hashlib
import collections
import evaluate_funcs as ef
import neighbor_funcs as nf
import mutation_funcs as mf
import generators as gn
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

# Algorithm 3
def genetic_algorithm(file_path,init_solution):
    
    libraries_shipped = set()

    data = DataContainer(*read_data(file_path))
    
    population_size = 100

    population = gn.generate_population_parallel(population_size , data.libraries, data.diffbooks, data.shipping_days, data.libraries_info, libraries_shipped, init_solution)
    population_len = len(population)
    population_fitness = None
    
    crossover_func = op.midpoint_crossover
    mutation_func = mf.mutation_solution_exchange_book

    best_solution = None
    best_score = None
    best_solution_generation = 0 
    num_iterations = 10
    generation_no = 0

    eval_scores = []
    population_fitness, old_best_score, old_best_solution , old_individuals_scores = ef.evaluate_population(population, data.scores)
    best_score = old_best_score
    best_solution = old_best_solution 

    while(num_iterations > 0):

        
        generation_no += 1
        new_population = []

        num_offspring = m.floor((population_len - len(new_population))/2)

        with ProcessPoolExecutor() as executor:
            parent_pairs = [(ef.tournament_select(population, 5, data.scores),
                            ef.roulette_select(population_fitness, old_individuals_scores))
                            for _ in range(num_offspring)]
            
            parent_crossover_pairs = [((parent1, parent2), crossover_func) for parent1, parent2 in parent_pairs]

            offspring_results = executor.map(gn.generate_offspring_wrapper, parent_crossover_pairs)
            
            for offspring in offspring_results:
                new_population.extend(offspring)
        
        new_population = ef.hybrid_elitism(population_len, new_population, old_individuals_scores,  0.2)

        mutated_offspring = []
        mutation_probability = 0.2

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(gn.mutate, list(child), libraries_shipped, data.libraries, mutation_func) for child in new_population if rand.random() <= mutation_probability]
            
            for future in as_completed(futures):
                mutated_child = future.result()
                mutated_offspring.append(mutated_child)
                
        for child in new_population:
            if child not in mutated_offspring:
                mutated_offspring.append(child)
                
        
       
        new_total_fitness, new_best_fitness, new_best_solution , new_individual_scores = ef.evaluate_population(mutated_offspring, data.scores)
        
        if new_total_fitness > population_fitness:
            best_solution = new_best_solution
            best_score = new_best_fitness
            population = new_population
            population_fitness = new_total_fitness
            old_best_score = new_best_fitness
            old_best_solution = new_best_solution
            old_individuals_scores = new_individual_scores
            best_solution_generation = generation_no
            eval_scores.append(new_total_fitness)
        else:
            eval_scores.append(population_fitness)

        num_iterations -= 1

   
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




