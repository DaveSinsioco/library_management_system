''''
Library Management System (LSM) Member Menu Features Module
This module provides the member menu features for user management in the Library Management System (LSM).

Developer:
Queñano, Ethan Cielo Luc V.
BS CpE 1-5
Group 3

Program Date:
June 20, 2025
'''

import datetime
import sqlalchemy as sa
from ORM_LSM import Member, Book, Transaction, BookTranscripts, engine
from sqlalchemy.orm import sessionmaker



class MemberMenu():
    def __init__(self, ID):
        self.__ID = ID  # User ID of the member
        

    def get_showProfile(self):  # Display My Details
        # Retrieve and display user's personal details
        # Function to login to user account
        Session = sessionmaker(bind=engine)

        # Create a new session
        session = Session()

        # Query the database for the user with the given studentID and password
        user = session.query(Member).filter_by(ID=self.__ID).one_or_none()

        print(f"Student ID: {user.ID}\nUsername: {user.username}\nName: {user.firstname} {user.surname}\nPUP Webmail: {user.pup_webmail}") # PLEASE REPLACE FOR GUI IMPLEMENTATION


    def showAvailableBooks(self):  # Display Available Books
        # Retrieve and display a list of available books
        # Create a new session to interact with the database
        Session  = sessionmaker(bind=engine)

        session = Session()

        books = session.query(Book).filter_by(isAvail='TRUE').all()  # Assuming '1' indicates available books

        for book in books:
            print(f"{book.bookID} : {book.category} : {book.title} : {book.author} : {book.publishing_house} : {book.publishing_date} : {book.isAvail}") # PLEASE REPLACE FOR GUI IMPLEMENTATION


    def showAllBooks(self):  # Display All Books
        # Retrieve and display a list of all books in the library
        # Create a new session to interact with the database
        Session  = sessionmaker(bind=engine)

        session = Session()

        books = session.query(Book).all()

        for book in books:
            print(f"{book.bookID} : {book.category} : {book.title} : {book.author} : {book.publishing_house} : {book.publishing_date} : {book.isAvail}") # PLEASE REPLACE FOR GUI IMPLEMENTATION

    def get_BorrowBook(self):  # Borrow Book Function
        # Logic to borrow a book
        # No Return Book Function as it is handled by an Administrator after the book is returned
        
        # Create a new session to interact with the database
        Session  = sessionmaker(bind=engine)

        session = Session()

        # Select the book to borrow
        while True:
            # Search Function
            # REPLACE WITH GUI IMPLEMENTATION
            bID = input("Enter Book ID to borrow: ")  # Get book ID from user input 
            title = input("Enter Book Title to borrow: ")  # Get book title from user input
            author = input("Enter Book Author to borrow: ")  # Get book author from user input
            house = input("Enter Book Publishing House to borrow: ")  # Get book publishing house from user input

            if bID != "":
                try:
                    books = session.query(Book).filter(Book.bookID.contains(int(bID)),
                                                        Book.title.contains(title), 
                                                        Book.author.contains(author), 
                                                        Book.publishing_house.contains(house)).all()
                except ValueError:
                    print("Invalid Book ID. Please enter a valid integer.") # PLEASE REPLACE FOR GUI IMPLEMENTATION
                    continue
            else:
                books = session.query(Book).filter(Book.title.contains(title), 
                                                    Book.author.contains(author), 
                                                    Book.publishing_house.contains(house)).all()
            
            for book in books:
                print(f"Book ID: {book.bookID}, Title: {book.title}, Author: {book.author}, Publishing House: {book.publishing_house}, Available: {book.isAvail}") # PLEASE REPLACE FOR GUI IMPLEMENTATION
            
            retry = input("Do you want to select a book? (yes/no): ").strip().lower()
            if retry == 'yes':
                try:
                    bookToBorrow = input("Enter the Book ID of the Book you want to borrow: ")  # Get book ID from user input
                    books = session.query(Book).filter_by(bookID = int(bookToBorrow)).one_or_none()
                    if books == None:
                        print("Book not found. Please try again.")
                        continue
                    print(f"You have selected: {books.title} by {books.author}")
                except ValueError:
                    print("Invalid input. Please enter a valid Book ID.")
                break
            elif retry != 'yes':
                continue
            

        unavail = session.query(Book).filter_by(bookID=int(bookToBorrow)).one_or_none()  # Get the book to borrow    
        unavail.isAvail = 'FALSE'

        transaction_rec = Transaction(ID=self.__ID, bookID=bookToBorrow, transactionType="BORROW")
        session.add(transaction_rec)

        session.commit()

    def get_showBorrowedBooks(self):  # Transaction History Database will hold borrowed books while Program will filter for user details and hide the rest
        # Retrieve and display user's list of borrowed books
        Session = sessionmaker(bind=engine)

        session = Session()

        borrows = session.query(Transaction).filter_by(ID=self.__ID).all()  # Get the book to borrow

        for borrow in borrows:
            books = session.query(Book).filter_by(bookID=borrow.bookID).one_or_none()
            print(f"Book Borrowed: {books.title} by {books.author}, Borrowed on: {borrow.dateborrowed}, Due Date: {borrow.dueDate}")  # PLEASE REPLACE FOR GUI IMPLEMENTATION

    def get_showMyTransactionHistory(self):  # Display My Transactions
        # Retrieve and display user's transaction history
        Session = sessionmaker(bind=engine)

        session = Session()

        transactions = session.query(Transaction).filter_by(ID=self.__ID).all()  # Get the book to borrow

        for transaction in transactions:
            books = session.query(BookTranscripts).filter_by(bookID=transaction.bookID).one_or_none()
            print(f"Book Borrowed: {books.title} by {books.author}, Borrowed on: {transaction.dateborrowed}, Due Date: {transaction.dueDate}")
            

test = MemberMenu("2021-10001-MN-0")
test2 = MemberMenu("2021-10007-MN-0")
test.get_showProfile()  # Example usage to display profile details
test2.get_showProfile()  # Example usage to display profile details
#test.showAvailableBooks()  # Example usage to display available books
# test.showAllBooks()  # Example usage to display all books
#test.get_BorrowBook()  # Example usage to borrow a book
test.get_showBorrowedBooks()

if __name__ == "__main__":
    pass