from concurrent.futures import ProcessPoolExecutor, as_completed
import copy
import random as rand
import numpy as np
import operators as op

def generate_population(population_size, libraries, diffbooks, shipping_days, libraries_info, libraries_shipped, init_solution):
    solutions = []
    for i in range(population_size):
        shipped_books_libraries, libraries_shipped = init_solution(libraries, diffbooks, shipping_days, libraries_info, libraries_shipped)
        solutions.append(list(shipped_books_libraries))
    return solutions

def worker(init_solution, libraries, diffbooks, shipping_days, libraries_info, libraries_shipped):
    return init_solution(libraries, diffbooks, shipping_days, libraries_info, libraries_shipped)

def exchange_library_worker(mutation_func_aux, libraries, shipping_days, individual_library, shipped_books_libraries, mutation_func):
     return mutation_func_aux(libraries, shipping_days, individual_library, shipped_books_libraries, mutation_func)

def generate_population_parallel(population_size, libraries, diffbooks, shipping_days, libraries_info, libraries_shipped, init_solution):
    solutions = []

    with ProcessPoolExecutor(max_workers=7) as executor:
        future_to_index = {executor.submit(worker, init_solution, libraries, diffbooks, shipping_days, libraries_info, libraries_shipped): i for i in range(population_size)}

        for future in as_completed(future_to_index):
            try:
                shipped_books_libraries, libs_shipped = future.result()
                solutions.append(list(shipped_books_libraries))
                libraries_shipped.append(libs_shipped)
            except Exception as exc:
                print(f'Generated an exception: {exc}')
    
    return solutions


def generate_offspring(pairs, cross_func):

    tournament_winner, roulette_winner = pairs
    
    new_individual1 , new_individual2 = cross_func(tournament_winner, roulette_winner)

    return new_individual1, new_individual2

def generate_offspring_wrapper(args):
    parents, crossover_func = args
    return generate_offspring(parents,  crossover_func)


def mutate_book(child, libraries_shipped, libraries, mutation_func):
                mutated_child, _ = mutation_func(child, libraries_shipped, libraries, 0)
                return mutated_child


def mutate_library(libraries, shipping_days, shipped_libraries, shipped_books_libraries, mutation_func):
                mutated_child, _ = mutation_func(libraries, shipping_days, shipped_libraries, list(shipped_books_libraries))
                return mutated_child

def generate_random_solution(libraries, diffbooks, shipping_days, libraries_info, libraries_shipped):
    visited_libs = []
    canShip_libs = set()
    shipped_books = set()
    shipped_books_libraries = []
    shuffled_libraries = libraries_info.copy()
    rand.shuffle(shuffled_libraries)
    shuffled_libraries_aux = copy.copy(shuffled_libraries)
    randlibID = shuffled_libraries_aux[0]
    randlibSignUp = libraries[randlibID].sign_up_time
   
    while shipping_days > 0:        
        if len(shipped_books) == diffbooks: 
            libraries_shipped = visited_libs
            return shipped_books_libraries, libraries_shipped
        elif randlibSignUp == 0 and len(shuffled_libraries_aux) > 0:
            canShip_libs.add(randlibID)
            visited_libs.append(randlibID)
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
                shipped_books_libraries.append((book, libID))

        randlibSignUp -= 1
        shipping_days -= 1

    libraries_shipped = visited_libs
    return shipped_books_libraries, libraries_shipped


def generate_trivial_solution(libraries, diffbooks, shipping_days, libraries_info, libraries_shipped):
    visited_libs = []
    canShip_libs = set()
    shipped_books = set()
    shipped_books_libraries = set()

    sorted_libraries = sorted(libraries_info, key=lambda libID: libraries[libID].sign_up_time)
    
    for libID in sorted_libraries:
        sign_up_time = libraries[libID].sign_up_time
        if sign_up_time > shipping_days:
            break  
        shipping_days -= sign_up_time  
        visited_libs.append(libID)
        all_books = set(libraries[libID].books.keys())
        available_books = list(all_books - shipped_books)
        
        daily_limit = libraries[libID].shipping_time
        selected_books = available_books[:daily_limit] 
        for book in selected_books:
            shipped_books.add(book)
            shipped_books_libraries.add((book, libID))

    libraries_shipped = visited_libs
    return shipped_books_libraries, libraries_shipped



def generate_determined_library_solution(shipped_books_libraries, lib_to_add, best_books):
    num_books = lib_to_add[1]
    sorted_available_books = sorted(best_books, key=lambda x: x[1], reverse=True)
    sorted_available_books = sorted_available_books[:num_books]
    new_books = []

    for book in sorted_available_books:
         new_books.append((book[0], lib_to_add[0]))
    shipped_books_libraries.extend(new_books)

    return shipped_books_libraries
          