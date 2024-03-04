import library as l

def read_data(file_path):
    i = 0
    libraries = {}
    books = {}
    scores = []
    libID = 0
    islib = False
    diffbooks = None
    numLibs = None
    shipping_days = None

    with open(file_path, 'r') as file:
        for line in file:
            arguments = line.split()
            if i == 0 :
                diffbooks = int(arguments[0])
                numLibs = int(arguments[1])
                shipping_days = int(arguments[2])
            elif i == 1:
                for arg in arguments:
                    scores.append(arg)
            elif i > 0 and (len(arguments) > 3 or len(arguments) < 3):
                
                for arg in arguments:
                    books[arg] = scores[int(arg)]
                    
                libraries[libID].books = books
            elif i > 0 and len(arguments) == 3 : 
                if islib :
                    libID += 1
                    islib = False
                lib = l.Library(int(arguments[0]),int(arguments[1]),int(arguments[2]))
                libraries[libID] = lib
                islib = True
            i += 1
            books = {}


    return libraries, books, scores, diffbooks, numLibs, shipping_days


def write_data(file_path, shipped_books_libraries, shipped_libraries):
    i = 0
    list_shipped_libraries = list(shipped_libraries)
    list_shipped_books_libraries = list(shipped_books_libraries)
    with open(file_path, 'w') as file:
        while True :
            if(len(list_shipped_libraries) == 0): break
            else:
                if i == 0:
                    file.write(str(len(shipped_libraries)))
                    file.write('\n')
                elif i % 2 != 0:
                    file.write(str(list_shipped_libraries[0]))
                    file.write(' ')
                    num_books = 0
                    for book in list_shipped_books_libraries:
                        if book[1] == list_shipped_libraries[0]:
                            num_books += 1
                    file.write(str(num_books))
                    file.write('\n')
                else:
                    for book in list_shipped_books_libraries:
                        if book[1] == list_shipped_libraries[0]:
                            file.write(book[0])
                            file.write(' ')
                    list_shipped_libraries.pop(0)
                    file.write('\n')
            i += 1
    
    return 0