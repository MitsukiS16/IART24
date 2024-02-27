class Library:
    books = {}

    def __init__(self, number_books, sign_up_time, shipping_time):
        self.number_books = number_books
        self.sign_up_time = sign_up_time
        self.shipping_time = shipping_time
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    