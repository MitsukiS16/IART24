# Function to read data from input file
def read_data(file_path):
    libraries = {}
    scores = []
    diffbooks = None
    numLibs = None
    shipping_days = None

    with open(file_path, 'r') as file:
        i = 0
        libID = 0
        islib = False
        books = {}
        for line in file:
            arguments = line.split()
            if i == 0:
                diffbooks, numLibs, shipping_days = map(int, arguments)
            elif i == 1:
                scores = list(map(int, arguments))
            elif i > 0 and (len(arguments) > 3 or len(arguments) < 3):
                for arg in arguments:
                    books[arg] = scores[int(arg)]
                libraries[libID].books = books
            elif i > 0 and len(arguments) == 3:
                if islib:
                    libID += 1
                    islib = False
                libraries[libID] = Library(int(arguments[0]), int(arguments[1]), int(arguments[2]))
                islib = True
            i += 1
            books = {}

    return libraries, diffbooks, numLibs, shipping_days