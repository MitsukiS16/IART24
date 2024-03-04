import numpy as np
#exchange book 

def neighbor_solution_exchange_book(solution, libraries_shipped, libraries):
    
    solution_list = list(solution)

    book = None

    size = 0
    for sol in solution_list:
        if(size == len(solution_list) - 1):
            book = sol
        else:
            even_odd = np.random.randint(1,3)
            if(even_odd % 2 == 0):
                book = sol
        size += 1

    sol_len = len(solution)
    #print(f"book to remove: {book}")
    library_id = book[1]
    solution.remove(book)  

    if library_id in libraries_shipped:
        keys = list(libraries[library_id].books.keys())
        if int(book[0]) in keys:
            available_books = [b for b in keys if b != int(book[0]) and str(b) not in solution]
            if available_books:
                new_book = np.random.choice(available_books) 
                #print(f"new book: {new_book}")
                solution.append(str(new_book)) 
    
    if sol_len > len(solution):
        solution.append(book)
        


    return solution


            

        
    
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
