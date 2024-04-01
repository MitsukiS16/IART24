import numpy as np
import random as rand
import evaluate_funcs as ef
import generators as gn

def neighbor_solution_exchange_book(solution, libraries_shipped, libraries, neighbor_score):
    neighbor_sol = solution.copy()
    book = rand.choice(neighbor_sol)
    library_id = book[1]
    neighbor_sol.remove(book)
 
    neighbor_score = ef.update_solution_score(neighbor_score, libraries[int(book[1])].books[int(book[0])], "dec")  

    if library_id in libraries_shipped:
        keys = list(libraries[library_id].books.keys())
        if book[0] in keys:
            available_books = [b for b in keys if b != book[0] and b not in neighbor_sol]
            if available_books:
                new_book = np.random.choice(available_books) 
                neighbor_sol.append((new_book, library_id))
                neighbor_score = ef.update_solution_score(neighbor_score, libraries[library_id].books[new_book], "inc")  
                
    return neighbor_sol, neighbor_score


def neighbor_exchange_libraries(libraries, shipping_days, shipped_libraries, shipped_books_libraries):
    shipped_library_efficiency = []
    library_efficiency = []
    remaining_shipping_days = shipping_days


    for libID in shipped_libraries:
        sign_up_time = libraries[libID].sign_up_time
        shipping_time = libraries[libID].shipping_time
        efficiency, days_left = ef.evaluate_library_efficiency(sign_up_time, remaining_shipping_days, shipping_time)
        remaining_shipping_days -= sign_up_time
        shipped_library_efficiency.append((libID, efficiency, days_left))

    sorted_shipped_library_efficiency = sorted(shipped_library_efficiency, key=lambda x: x[1])

        
    sorted_shipped_library_efficiency = sorted(shipped_library_efficiency, key=lambda x: x[1])
    lib_to_remove = sorted_shipped_library_efficiency[0][0]

    lib_to_remove_days_left = sorted_shipped_library_efficiency[0][2]
    library_keys = libraries.keys()

    available_libraries = [libID for libID in library_keys if int(libID) not in shipped_libraries]

    for libID in available_libraries:
        sign_up_time = libraries[libID].sign_up_time
        shipping_time = libraries[libID].shipping_time
        efficiency, days_left = ef.evaluate_library_efficiency(sign_up_time, lib_to_remove_days_left, shipping_time)
        library_efficiency.append((libID, efficiency))
    
    sorted_library_efficiency = sorted(library_efficiency, key=lambda x: x[1])

    
    
    if(sorted_library_efficiency[-1][1] <= 0): return shipped_books_libraries, shipped_libraries
    elif(sorted_library_efficiency[-1][1] < sorted_shipped_library_efficiency[0][1]): return shipped_books_libraries, shipped_libraries


   
    best_library , best_books = ef.evaluate_library_book_efficiency(libraries, sorted_library_efficiency, shipped_books_libraries)

    
    lib_to_remove_index = shipped_libraries.index(lib_to_remove)
    
    shipped_libraries.remove(lib_to_remove)

    shipped_libraries.insert(lib_to_remove_index, best_library[0])

    lib_to_add = best_library
    
    for book_lib in shipped_books_libraries:
        if book_lib[1] == lib_to_remove:
            shipped_books_libraries.remove(book_lib)

    shipped_books_libraries = gn.generate_determined_library_solution(shipped_books_libraries, lib_to_add, best_books)

    return shipped_books_libraries, shipped_libraries
        
    