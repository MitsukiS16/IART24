import numpy as np
import random as rand
import evaluate_funcs as ef
#exchange book 

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


            

        
    
    #exchange 2 books

def neighbor_solution_exchange_two_books(solution, libraries_shipped):
    solution_list = list(solution)

    book1 = None
    book2 = None

    size = 0
    for sol in solution_list:
        if(size == len(solution_list) - 1):
            book1 = solution_list[size - 1]
            book2 = sol
        else:
            even_odd = np.random.randint(1,3)
            if(even_odd % 2 == 0):
                book1 = sol
                book2 = solution_list[size + 1]
        size += 1

    sol_len = len(solution)

    aux_libs = list()
    aux_books = list()

    aux_libs.append(book1[1])
    aux_libs.append(book2[1])

    aux_books.append(book1[0])
    aux_books.append(book2[0])

    solution.remove(book1)  
    solution.remove(book2)

    for book, library_id in aux_books, aux_libs:
        if library_id in libraries_shipped:
            keys = list(libraries[library_id].books.keys())
            if int(book) in keys:
                available_books = [b for b in keys if b != int(book) and str(b) not in solution]
                if available_books:
                    new_book = np.random.choice(available_books) 
                    #print(f"new book: {new_book}")
                    solution.add(str(new_book)) 
    
    # if sol_len > len(solution):
    #     solution.add(book1)
    #     solution.add(book2)
    return solution



def neighbor_solution_exchange_library_check(shipped_books, libraries_shipped):
    randlibID_shipped = random_sign_up(len(libraries_shipped))

    libraries_not_shipped = set()
    for library_key in libraries.keys():
        if library_key not in libraries_shipped:
            libraries_not_shipped.add(library_key)

    randlibID_not_shipped = random_sign_up(libraries_not_shipped)

    i = 0 
    for libID in libraries_shipped:
        if(libID == randlibID_shipped):
            libraries_shipped[i] = randlibID_not_shipped
            break
        i += 1

    for book in shipped_books:
        if(book[1]) == randlibID_shipped:
            remove_book(shipped_books, book)
            add_book(shipped_books, randlibID_not_shipped)
            
     
    return shipped_books, libraries_shipped


def neighbor_solution_exchange_library_no_check(shipped_books, libraries_shipped):
    randlibID_shipped = random_sign_up(len(libraries_shipped))

    libraries_not_shipped = set()
    for library_key in libraries.keys():
        if library_key not in libraries_shipped:
            libraries_not_shipped.add(library_key)

    randlibID_not_shipped = random_sign_up(libraries_not_shipped)

    i = 0 
    for libID in libraries_shipped:
        if(libID == randlibID_shipped):
            libraries_shipped[i] = randlibID_not_shipped
            break
        i += 1

    for book in shipped_books:
        if(book[1]) == randlibID_shipped:
            remove_book(shipped_books, book)

    for i in range(0,len(libraries[randlibID_shipped].books)):
            add_book(shipped_books, randlibID_not_shipped)
            
     
    return shipped_books, libraries_shipped
