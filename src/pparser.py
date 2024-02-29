from library import Library


# l = {}
# scores = []
# db = None
# numLibs = None
# sdays = None

# Function to read data from input file
def read_data_file(file_path):
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

    return libraries, diffbooks, numLibs, shipping_days, scores


# libraries, diffbooks, numlibs, shipping_days = read_data('/Users/valter/Documents/FEUP/2023_2024/2_semestre/3_ano/IA/proj/IART24/libraries/b_read_on.txt')

# def prnt_libs_books():
#     for key,value in libraries.items():
#         print(f"Library : {key}, {value.number_books}")
#         for bk, bv in value.books.items():
#             print(f"{bk}, {bv}")

# prnt_libs_books()