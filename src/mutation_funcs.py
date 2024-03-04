import neighbor_funcs as nf

def mutation_solution_exchange_book(solution, libraries_shipped, libraries):
    return nf.neighbor_solution_exchange_book(solution, libraries_shipped, libraries)


def mutation_solution_exchange_two_books(solution, libraries_shipped):
    return nf.neighbor_solution_exchange_two_books(solution, libraries_shipped)


def mutation_solution_exchange_library_check(shipped_books, libraries_shipped):
    return nf.neighbor_solution_exchange_library_check(shipped_books, libraries_shipped)


def mutation_solution_exchange_library_no_check(shipped_books, libraries_shipped):
    return nf.neighbor_solution_exchange_library_no_check(shipped_books, libraries_shipped)