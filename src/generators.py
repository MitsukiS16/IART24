from concurrent.futures import ProcessPoolExecutor, as_completed
import copy
import random as rand
import numpy as np

def generate_population(population_size, libraries, diffbooks, shipping_days, libraries_info, libraries_shipped, init_solution):
    solutions = []
    for i in range(population_size):
        shipped_books_libraries, libraries_shipped = init_solution(libraries, diffbooks, shipping_days, libraries_info, libraries_shipped)
        solutions.append(list(shipped_books_libraries))
    return solutions

def worker(init_solution, libraries, diffbooks, shipping_days, libraries_info, libraries_shipped):
        return init_solution(libraries, diffbooks, shipping_days, libraries_info, libraries_shipped)

def generate_population_parallel(population_size, libraries, diffbooks, shipping_days, libraries_info, libraries_shipped, init_solution):
    solutions = []

    with ProcessPoolExecutor(max_workers=7) as executor:
        future_to_index = {executor.submit(worker, init_solution, libraries, diffbooks, shipping_days, libraries_info, libraries_shipped): i for i in range(population_size)}

        for future in as_completed(future_to_index):
            try:
                shipped_books_libraries, _ = future.result()
                solutions.append(list(shipped_books_libraries))
            except Exception as exc:
                print(f'Generated an exception: {exc}')
    
    return solutions


def generate_offspring(pairs, cross_func):
    tournament_winner, roulette_winner = pairs
    return cross_func(tournament_winner, roulette_winner)

def generate_offspring_wrapper(args):
    parents, crossover_func = args
    return generate_offspring(parents, crossover_func)

def mutate(child, libraries_shipped, libraries, mutation_func):
                mutated_child, _ = mutation_func(child, libraries_shipped, libraries, 0)
                return mutated_child

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

def generate_determined_library_solution(libraries, shipped_books_libraries, lib_to_add):
    
    num_books = lib_to_add[1]

    shipped_books = {tup[0] for tup in shipped_books_libraries}

    available_books = [(int(key), int(value)) for key, value in libraries[lib_to_add[0]].books.items() if int(key) not in shipped_books]

    sorted_available_books = sorted(available_books, key=lambda x: x[1], reverse=True)

    sorted_available_books = sorted_available_books[:num_books]

    new_books = []

    for book in sorted_available_books:
         new_books.append((book[0], lib_to_add[0]))

    shipped_books_libraries.extend(new_books)


    return shipped_books_libraries
          