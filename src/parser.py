def read_data(file_path):
    libraries = {}
    scores = []
    diffbooks = None
    numLibs = None
    shipping_days = None

    with open(file_path, 'r') as file:
        lines = file.readlines()

        # Parsing the first line containing B, L, and D
        diffbooks, numLibs, shipping_days = map(int, lines[0].split())

        # Parsing the second line containing the scores of individual books
        scores = list(map(int, lines[1].split()))

        # Parsing library information
        i = 2  # Start from the third line
        libID = 0
        while i < len(lines):
            Nj, Tj, Mj = map(int, lines[i].split())
            book_ids = list(map(int, lines[i+1].split()))  # Get the book IDs for the current library
            books = {book_id: scores[book_id] for book_id in book_ids}  # Create a dictionary of book IDs and scores
            libraries[libID] = {
                'Nj': Nj,
                'Tj': Tj,
                'Mj': Mj,
                'books': books
            }
            libID += 1
            i += 2  # Move to the next library section

    return libraries, diffbooks, numLibs, shipping_days
