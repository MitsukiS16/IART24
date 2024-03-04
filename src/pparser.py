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
