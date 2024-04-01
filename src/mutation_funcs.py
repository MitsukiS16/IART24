import neighbor_funcs as nf

def mutation_solution_exchange_book(solution, libraries_shipped, libraries, neighbor_score):
    return nf.neighbor_solution_exchange_book(solution, libraries_shipped, libraries, neighbor_score)

def mutation_solution_exchange_libraries(libraries, shipping_days, shipped_libraries, shipped_books_libraries):
    return nf.neighbor_exchange_libraries(libraries, shipping_days, shipped_libraries, shipped_books_libraries)