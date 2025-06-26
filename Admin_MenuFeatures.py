''''
Library Management System (LSM) Admin Menu Features Module
This module provides the admin menu functions for user management in the Library Management System (LSM).

Developer:
Queñano, Ethan Cielo Luc V.
BS CpE 1-5
Group 3

Program Date:
June 20, 2025
'''

import datetime
import sqlalchemy as sa
from ORM_LSM import Admin, Member, Book, Transaction, BookTranscripts, engine
from sqlalchemy.orm import sessionmaker

class AdminMenu():
    def __init__(self, ID):
        self.__ID = ID  # User ID of the admin

    def get_showProfile(self):  # Display My Details
        # Retrieve and display admin's personal details
        Session = sessionmaker(bind=engine)

        # Create a new session
        session = Session()

        # Query the database for the admin with the given ID
        user = session.query(Admin).filter_by(ID=self.__ID).one_or_none()

        print(f"Admin ID: {user.ID}\nUsername: {user.username}\nName: {user.firstname} {user.surname}\nPUP Webmail: {user.puplibrary_webmail}")  # PLEASE REPLACE FOR GUI IMPLEMENTATION


    def showAllBooks(self):  # Display All Books
        # Retrieve and display a list of all books in the library
        # Create a new session to interact with the database
        Session  = sessionmaker(bind=engine)

        session = Session()

        books = session.query(Book).all()

        for book in books:
            print(f"{book.bookID} : {book.category} : {book.title} : {book.author} : {book.publishing_house} : {book.publishing_date} : {book.isAvail}") # PLEASE REPLACE FOR GUI IMPLEMENTATION

    def showAvailableBooks(self):  # Display Available Books
        # Retrieve and display a list of available books
        # Create a new session to interact with the database
        Session  = sessionmaker(bind=engine)

        session = Session()

        books = session.query(Book).filter_by(isAvail='TRUE').all()  # Assuming '1' indicates available books

        for book in books:
            print(f"{book.bookID} : {book.category} : {book.title} : {book.author} : {book.publishing_house} : {book.publishing_date} : {book.isAvail}") # PLEASE REPLACE FOR GUI IMPLEMENTATION

    def showBorrowedBooks(self):  # Display Borrowed Books
        # Retrieve and display a list of borrowed books
        Session = sessionmaker(bind=engine)

        session = Session()

        transactions = session.query(Transaction).filter_by(transactionType='BORROW').all()  # Get the book to borrow

        for transaction in transactions:
            books = session.query(BookTranscripts).filter_by(bookID=transaction.bookID).one_or_none()
            print(f"Book Borrowed: {books.title} by {books.author}, Borrowed on: {transaction.dateborrowed}, Due Date: {transaction.dueDate}")


    def markReturned(self):  # Mark Book as Returned
        # Logic to mark a book as returned in the library
        Session = sessionmaker(bind=engine)
        session = Session()

        while True:
            # Search Function
            # REPLACE WITH GUI IMPLEMENTATION
            bID = input("Enter Book ID: ")  # Get book ID from user input 
            title = input("Enter Book Title: ")  # Get book title from user input
            author = input("Enter Book Author: ")  # Get book author from user input
            house = input("Enter Book Publishing: ")  # Get book publishing house from user input

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
                    markReturn = input("Enter the Book ID of the Book that was returned: ")  # Get book ID from user input
                    books = session.query(Book).filter_by(bookID = int(markReturn)).one_or_none()
                    if books == None:
                        print("Book not found. Please try again.")
                        continue
                    print(f"You have selected: {books.title} by {books.author}")
                except ValueError:
                    print("Invalid input. Please enter a valid Book ID.")
                returneeID = input("Enter the ID of the Member that returned book: ")  # Get book ID from user input
                while True:
                    returnee = session.query(Member).filter_by(ID = returneeID).one_or_none()
                    if returnee == None:
                        print("Member not found. Please try again.")
                        continue
                    print(f"You have selected: {returnee.firstname} {returnee.surname}")
                    confirm = input("Please Confirm (yes/no): ").strip().lower()
                    if confirm == 'yes':
                        break
                    else:
                        continue
                break
            elif retry != 'yes':
                continue
            
        returned = session.query(Book).filter_by(bookID=int(markReturn)).one_or_none() # Get the book to borrow 
        returned.isAvail = 'TRUE'  # Mark all books as available

        transaction_rec = Transaction(ID=returneeID, bookID=markReturn, transactionType="RETURN")
        session.add(transaction_rec)
        session.commit()

    def AddBook(self):  # Add Book Function
        # Logic to add a new book to the library
        Session = sessionmaker(bind=engine)
        session = Session()

        # REPLACE WITH GUI IMPLEMENTATION
        ctg = input("Catgory: ")  # Get book category from user input
        ttl = input("Title: ") # Get book title from user input
        auth = input("Author: ") # Get book author from user input
        publihs = input("Publication House: ") # Get book publishing house from user input
        publidt = input("Publication Date: ") # Get book publication date from user input

        new = Book(category=ctg, title=ttl, author=auth, publishing_house=publihs, publishing_date=publidt)

        session.add(new)
        session.commit()

    def RemoveBook(self):  # Remove Book Function
        # Logic to remove a book from the library
        Session = sessionmaker(bind=engine)
        session = Session()

        while True:
            # Search Function
            # REPLACE WITH GUI IMPLEMENTATION
            bID = input("Enter Book ID: ")  # Get book ID from user input 
            title = input("Enter Book Title: ")  # Get book title from user input
            author = input("Enter Book Author: ")  # Get book author from user input
            house = input("Enter Book Publishing: ")  # Get book publishing house from user input

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
            
            retry = input("Do you want to select a book to remove? (yes/no): ").strip().lower()
            if retry == 'yes':
                try:
                    bookRemove = input("Enter the Book ID of the Book to be removed: ")  # Get book ID from user input
                    books = session.query(Book).filter_by(bookID = int(bookRemove)).one_or_none()
                    if books == None:
                        print("Book not found. Please try again.")
                        continue
                    print(f"You have selected: {books.title} by {books.author}")
                except ValueError:
                    print("Invalid input. Please enter a valid Book ID.")
                break
            elif retry != 'yes':
                continue
            
        remove = session.query(Book).filter_by(bookID=int(bookRemove)).one_or_none() # Get the book to borrow 
        session.delete(remove)
        session.commit()


    def showAllMemberDetails(self):  # Display User Details
        # Retrieve and display user's personal details
        Session = sessionmaker(bind=engine)

        # Create a new session
        session = Session()

        # Query the database for the user with the given studentID and password
        users = session.query(Member).all()

        for user in users:
            print(f"Student ID: {user.ID}\nUsername: {user.username}\nName: {user.firstname} {user.surname}\nPUP Webmail: {user.pup_webmail}") # PLEASE REPLACE FOR GUI IMPLEMENTATION

    def showMemberDetails(self):  # Display User Details by ID
        # Retrieve and display user's personal details by ID
        Session = sessionmaker(bind=engine)

        session = Session()

        while True:
            # Search Function
            # REPLACE WITH GUI IMPLEMENTATION
            mID = input("Enter student ID: ")  # Get book ID from user input 
            fname = input("Enter Firstname: ")  # Get book title from user input
            sname = input("Enter Surname: ")  # Get book author from user input
            uname = input("Enter Usrname: ")  # Get book publishing house from user input
            
            users = session.query(Member).filter(Member.ID.contains(mID), 
                                                Member.firstname.contains(fname), 
                                                Member.surname.contains(sname), 
                                                Member.username.contains(uname)).all()

            for user in users:
                print(f"Student ID: {user.ID}\nUsername: {user.username}\nName: {user.firstname} {user.surname}\nPUP Webmail: {user.pup_webmail}") # PLEASE REPLACE FOR GUI IMPLEMENTATION
            

    def showTransactionHistory(self):  # Display Transaction History
        # Retrieve and display transaction history of the library
        Session = sessionmaker(bind=engine)

        session = Session()

        transactions = session.query(Transaction).all()  # Get the book to borrow

        for transaction in transactions:
            books = session.query(BookTranscripts).filter_by(bookID=transaction.bookID).one_or_none()
            print(f"Book: {books.title} by {books.author}, Transaction: {transaction.transactionType} Date: {transaction.dateborrowed}, Book Return Due Date: {transaction.dueDate}")


test = AdminMenu("2024-00697-MN-0")  # Example instantiation of AdminMenu with ID 2024-00697-MN-0
test.get_showProfile()  # Example call to display admin profile details
#test.showAllMemberDetails()  # Example call to display all member details
#test.showMemberDetails()  # Example call to display member details by ID
#test.markReturned()  # Example call to mark a book as returned
#test.AddBook()
#test.RemoveBook()



if __name__ == "__main__":
    # This block can be used for testing the functions or running the module directly
    while True:
        print("Library Management System Admin Menu:")
        myID = input("Please enter your ID: ")  # Get admin ID from user input; enter ID to
        print("1. Display Admin Profile")
        print("2. Display Member Details")
        print("3. Display Books")
        print("4. Manage Books")
        print("5. Manage Transaction History")
        choice = input("Please choose an option: ") # Get user choice from input
        if choice == "1":
            user = AdminMenu(myID)


# Developer function to set book availability status to True
def markAllReturned():  # Mark All Books as Returned
    # Logic to mark all books as returned in the library
    Session = sessionmaker(bind=engine)
    session = Session()
    borrow = session.query(Book).all()  # Get the book to borrow    
    for book in borrow:
        book.isAvail = 'TRUE'  # Mark all books as available
    session.commit()
    print("All books have been marked as available.")  # Confirmation message

#markAllReturned()  # Call the function to reset all books to available status

# Developer function to set book availability status to False
def markAllBorrowed():  # Mark All Books as Returned
    # Logic to mark all books as returned in the library
    Session = sessionmaker(bind=engine)
    session = Session()
    borrow = session.query(Book).all()  # Get the book to borrow    
    for book in borrow:
        book.isAvail = 'FALSE'  # Mark all books as available
    session.commit()
    print("All books have been marked as unavailable.")  # Confirmation message

#markAllBorrowed()  # Call the function to reset all books to available status
