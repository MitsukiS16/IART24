import math as m
import numpy as np


def random_sign_up(number_of_libs):
    return np.random.randint(0,number_of_libs)


# crossover operators

def midpoint_crossover(solution1, solution2):
    genetic_linfo_sol1 = solution1[:m.ceil(len(solution1)/2)]
    genetic_linfo_sol2 = solution2[:m.ceil(len(solution2)/2)]
    
    genetic_rinfo_sol1 = solution1[m.ceil(len(solution1)/2):]
    genetic_rinfo_sol2 = solution2[m.ceil(len(solution2)/2):]
    
    chromosome1 = genetic_linfo_sol1 + genetic_rinfo_sol2
    chromosome2 = genetic_rinfo_sol1 + genetic_linfo_sol2
    
    return chromosome1, chromosome2


def randompoint_crossover(solution1, solution2):
    genetic_linfo_sol1 = solution1[:m.ceil(random_sign_up(len(solution1))/2)]
    genetic_linfo_sol2 = solution2[:m.ceil(random_sign_up(len(solution2))/2)]

    genetic_rinfo_sol1 = solution1[m.ceil(random_sign_up(len(solution1))/2):]
    genetic_rinfo_sol2 = solution2[m.ceil(random_sign_up(len(solution2))/2):]

    chromosome1 = genetic_linfo_sol1 + genetic_rinfo_sol2
    chromosome2 = genetic_rinfo_sol1 + genetic_linfo_sol2

    return chromosome1, chromosome2


def remove_book(shipped_books, book):
    if book in shipped_books:
        shipped_books.remove(book)
    return shipped_books