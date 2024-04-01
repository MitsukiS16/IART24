# Imports 
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from multiprocessing import Manager
from pparser import read_data
import hashlib
import collections
import evaluate_funcs as ef
import neighbor_funcs as nf
import mutation_funcs as mf
import generators as gn
from generators import generate_random_solution
import operators as op
import numpy as np
import math as m
import random as rand


########################################
#Global Variables

DataContainer = collections.namedtuple('DataContainer', ['libraries', 'scores', 'diffbooks', 'shipping_days', 'libraries_info'])

########################################

# Genetic Algorithm
def genetic_algorithm(file_path,init_solution):
    libraries_shipped = []
    data = DataContainer(*read_data(file_path))
    population_size = 20
    population = gn.generate_population_parallel(population_size , data.libraries, data.diffbooks, data.shipping_days, data.libraries_info, libraries_shipped, init_solution)

    population_len = len(population)

    population_fitness = None
    crossover_func = op.midpoint_crossover
    mutation_func = mf.mutation_solution_exchange_libraries
    best_solution = None
    best_score = None
    best_solution_generation = 0 
    num_iterations = 20
    generation_no = 0
    eval_scores = []

    population_fitness, old_best_score, old_best_solution , old_individuals_scores = ef.evaluate_population(population, data.scores)
   
    best_score = old_best_score
    best_solution = old_best_solution 
    best_library = None

    while(num_iterations > 0):
        
        generation_no += 1
        new_population = []
        num_offspring = m.floor(population_len/2)
        
        tournament_size = 5
        with ProcessPoolExecutor() as executor:
            parent_pairs = [(ef.tournament_select(population, tournament_size, data.scores),
                            ef.roulette_select(population_fitness, old_individuals_scores))
                            for _ in range(num_offspring)]
            
            parent_crossover_pairs = [((tuple(parent1), tuple(parent2)), crossover_func) for parent1, parent2 in parent_pairs]
            offspring_results = executor.map(gn.generate_offspring_wrapper, parent_crossover_pairs)
      
            for offspring1, offspring2 in offspring_results:
                
                new_population.append(offspring1)
                new_population.append(offspring2)
    
        
        elite_percentage = 0.2
        new_population = ef.hybrid_elitism(population_len, new_population, old_individuals_scores,  elite_percentage)
        individual_library = {}
        individual_key = {}
        for individual in new_population:
            op.update_individual_library(individual, individual_library, individual_key)

     
        mutated_offspring = []
        mutation_probability = 0.1
        
       
        with ProcessPoolExecutor(max_workers=7) as executor:
            futures = [executor.submit(gn.exchange_library_worker, gn.mutate_library, data.libraries, data.shipping_days, individual_library[(tuple(child),individual_key[tuple(child)])], child, mutation_func) for child in new_population if rand.random() <= mutation_probability]
            for future in as_completed(futures):
                try:
                    mutated_child = future.result()
                    mutated_offspring.append(mutated_child)
                except Exception as exc:
                    print(f'Generated an exception: {exc}')
   
        num_mutated = len(mutated_offspring)
        num_new_population = len(new_population)
        
        new_population = mutated_offspring + new_population[:num_new_population - num_mutated]
        print(len(new_population))
        
        new_total_fitness, new_best_fitness, new_best_solution , new_individual_scores = ef.evaluate_population(new_population, data.scores)
       
        best_solution = new_best_solution
        best_score = new_best_fitness
        population = new_population
        population_fitness = new_total_fitness
        old_best_score = new_best_fitness
        old_best_solution = new_best_solution
        old_individuals_scores = new_individual_scores
        best_solution_generation = generation_no
        
        eval_scores.append(new_total_fitness)
       
        num_iterations -= 1
       

    best_library = ef.get_solution_library(best_solution)

    
    return  best_solution, best_library , eval_scores

# Tabu Search
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

# Simulated Annealing Algorithm
def get_sa_solution(file_path,init_solution):   

    libraries_shipped = set()

    data = DataContainer(*read_data(file_path))
    

    shipped_books_libraries, libraries_shipped = init_solution(data.libraries, data.diffbooks, data.shipping_days, data.libraries_info, libraries_shipped)

    

    num_iterations = 10
    iteration = 0
    temperature = 1000

    cooling_rate = 0.999

    best_score = ef.evaluate_solution(shipped_books_libraries, data.scores)


    eval_scores = []

    eval_scores.append(best_score)
    
    best_solution = list(shipped_books_libraries)

    if(best_score == sum(data.scores)): return best_solution, libraries_shipped, eval_scores

    while iteration < num_iterations :

        temperature *= cooling_rate
        iteration += 1
        
        neighbor_score = best_score

        neighbor , neighbor_score = nf.neighbor_solution_exchange_book(best_solution, libraries_shipped, data.libraries, neighbor_score)
        

        if(neighbor_score == sum(data.scores)): return best_solution, libraries_shipped, eval_scores
        elif(neighbor_score == best_score): return best_solution, libraries_shipped, eval_scores

        
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

# Hill Climbing Algorithm
def hill_climbing_algorithm(file_path, init_solution):

    libraries_shipped = set()

    data = DataContainer(*read_data(file_path))

    shipped_books_libraries, libraries_shipped = init_solution(data.libraries, data.diffbooks, data.shipping_days, data.libraries_info, libraries_shipped)

    best_score = ef.evaluate_solution(shipped_books_libraries, data.scores)
    best_sol = list(shipped_books_libraries)
    
    improved = True
    while improved:
        improved = False
        neighbor_sol, potential_new_score = nf.neighbor_solution_exchange_book(best_sol, libraries_shipped, data.libraries, best_score)

        neighbor_score = ef.evaluate_solution(neighbor_sol, data.scores)

        # If the neighbor solution is better, update the best solution
        if neighbor_score > best_score:
            best_sol = neighbor_sol
            best_score = neighbor_score
            improved = True

    return best_sol, libraries_shipped, best_score

