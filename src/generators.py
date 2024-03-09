from concurrent.futures import ProcessPoolExecutor, as_completed

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