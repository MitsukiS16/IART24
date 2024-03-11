from library import Library
from tabulate import tabulate

def read_data(file_path):
    libraries = {}
    num_libs = None
    diffbooks = set()
    shipping_days = 0
    libraries_info = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
        num_books, num_libs, shipping_days = map(int, lines[0].split())
        scores = list(map(int, lines[1].split()))

        current_line = 2
        for i in range(num_libs):
            num_books_in_lib, signup_days, shipping_rate = map(int, lines[current_line].split())
            current_line += 1
            book_ids = list(map(int, lines[current_line].split()))
            current_line += 1
            library_books = {book_id: scores[book_id] for book_id in book_ids}  # Use dictionary instead of list of tuples
            libraries[i] = Library(num_books_in_lib, signup_days, shipping_rate)
            libraries[i].books = library_books
            diffbooks.update(book_ids)
            libraries_info.append(i) 
            
    libraries_info = list(libraries.keys())
    return libraries, scores, diffbooks, shipping_days, libraries_info


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
                            file.write(str(book[0]))
                            file.write(' ')
                    list_shipped_libraries.pop(0)
                    file.write('\n')
            i += 1
    return 0



def test_read_func(libraries, scores, diffbooks, shipping_days, libraries_info):
    print("Number of libraries:", len(libraries))
    print("Number of different books:", len(diffbooks))
    total_score = sum(scores)
    print("Total score (sum of all scores):", total_score)

    print("\nLibrary details:")
    rows = []
    for lib_id, lib in libraries.items():
        total_lib_score = sum(scores[book[0]] for book in lib.books)
        rows.append([lib_id, len(lib.books), total_lib_score])
    headers = ["Library ID", "Number of Books", "Total Score"]
    print(tabulate(rows, headers=headers))


# file_path = "../input/a_example.txt"
# file_path = "../input/b_read_on.txt"
# file_path = "../input/a_example.txt"
# file_path = "../input/a_example.txt"
# file_path = "../input/a_example.txt"
# file_path = "../input/a_example.txt"

# libraries, scores, diffbooks, shipping_days, libraries_info = read_data(file_path)
# test_read_func(libraries, scores, diffbooks, shipping_days, libraries_info)
