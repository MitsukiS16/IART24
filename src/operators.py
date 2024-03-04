import math as m
import numpy as np


def random_sign_up(number_of_libs):
    return np.random.randint(0,number_of_libs)


# crossover operators

def midpoint_crossover(solution1, solution2):

    solution1 = list(solution1) if isinstance(solution1, set) else solution1
    solution2 = list(solution2) if isinstance(solution2, set) else solution2

    genetic_linfo_sol1 = solution1[:m.ceil(len(solution1)/2)]
    genetic_linfo_sol2 = solution2[:m.ceil(len(solution2)/2)]

    genetic_rinfo_sol1 = solution1[m.ceil(len(solution1)/2):]
    genetic_rinfo_sol2 = solution2[m.ceil(len(solution2)/2):]

    chromosome1 = genetic_linfo_sol1 + genetic_rinfo_sol2
    chromosome2 = genetic_rinfo_sol1 + genetic_linfo_sol2

    while len(chromosome1) > len(solution1):
        chromosome1 = chromosome1[:-1]

    while len(chromosome2) > len(solution2):
        chromosome2 = chromosome2[:-1]

    return chromosome1, chromosome2


def randompoint_crossover(solution1, solution2):

    solution1 = list(solution1) if isinstance(solution1, set) else solution1
    solution2 = list(solution2) if isinstance(solution2, set) else solution2

    genetic_linfo_sol1 = solution1[:m.ceil(random_sign_up(len(solution1))/2)]
    genetic_linfo_sol2 = solution2[:m.ceil(random_sign_up(len(solution2))/2)]

    genetic_rinfo_sol1 = solution1[m.ceil(random_sign_up(len(solution1))/2):]
    genetic_rinfo_sol2 = solution2[m.ceil(random_sign_up(len(solution2))/2):]

    chromosome1 = genetic_linfo_sol1 + genetic_rinfo_sol2
    chromosome2 = genetic_rinfo_sol1 + genetic_linfo_sol2

    while len(chromosome1) > len(solution1):
        chromosome1 = chromosome1[:-1]

    while len(chromosome2) > len(solution2):
        chromosome2 = chromosome2[:-1]

    return chromosome1, chromosome2


def add_book(shipped_books, libID):
    size = len(libraries[libID].books)

    visited_books = set()
    while True:
        random_book_id = np.random.randint(0,size)
        random_book = libraries[libID].books[random_book_id]
        if(random_book in shipped_books):
            if(len(visited_books) == size): break 
            visited_books.add(random_book_id)
            continue
        else:
            shipped_books.add((random_book,libID)) 
            break

    return shipped_books


def remove_book(shipped_books, book):
    if book in shipped_books:
        shipped_books.remove(book)
    return shipped_books