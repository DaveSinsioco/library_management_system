''''
Library Management System (LSM) User Login Module
This module provides the login function for user management in the Library Management System (LSM).

Developer:
Queñano, Ethan Cielo Luc V.
BS CpE 1-5
Group 3

Program Date:
June 20, 2025
'''

# Import necessary libraries
# Import abstract base class for defining abstract classes
import os
import sqlite3
import datetime
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, DateTime, VARCHAR, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


import os

directory = (os.path.dirname(os.path.abspath(__file__))).replace("\\", "/")

print('Absolute directoryname: ', directory)

# SQLite database url format:
# sqllite_db_url = sqllite://<path>
# sqllite_db_url = "sqlite:///path/to/your/database.db" => 3 forward slash is relative path, 4 forward slash is absolute path


sqllite_db_url = f"sqlite:///{directory[0].upper()}{directory[1:]}/Database/lsmDatabase.db"

engine = create_engine(sqllite_db_url)

Base = declarative_base()


class Admin(Base):
    # Class for ORM allowing database management through object oriented programming techniques
    # ORM for book_database table
    __tablename__ = "admin_database"

    username = Column(String)
    ID = Column(String, primary_key=True)  # Assuming ID (Student, Instructor/Professor, Librarian) is unique
    firstname = Column(String)
    surname = Column(String)
    puplibrary_webmail = Column(String) #provvided and manually uploaded by the admin (IT and Lead Librarian) into the database
    password = Column(String)


class Member(Base):
    # Class for ORM allowing database management through object oriented programming techniques
    # ORM for user_database table
    __tablename__ = "user_database"

    username = Column(String)
    ID = Column(String, primary_key=True)  # Assuming studentID is unique
    firstname = Column(String)
    surname = Column(String)
    pup_webmail = Column(String)
    password = Column(String)

class Book(Base):
    # Class for ORM allowing database management through object oriented programming techniques
    # ORM for book_database table
    __tablename__ = "real_library_books"

    bookID = Column(Integer, autoincrement=True, primary_key=True)  # Assuming bookID is unique
    category = Column(VARCHAR(45))  # e.g., 'fiction', 'non-fiction', 'science', etc.
    title = Column(VARCHAR(45))
    author = Column(VARCHAR(45))
    publishing_house = Column(VARCHAR(45))  # e.g., 'Publisher Name'
    publishing_date = Column(VARCHAR(45))  # Date when the book was published
    isAvail = Column(VARCHAR(45), default="TRUE")  # 1 if available, 0 if not available

class BookTranscripts(Base):
    # Class for ORM allowing database management through object oriented programming techniques
    # ORM for book_database table
    __tablename__ = "book_transcripts"

    bookID = Column(Integer, autoincrement=True, primary_key=True)  # Assuming bookID is unique
    category = Column(VARCHAR(45))  # e.g., 'fiction', 'non-fiction', 'science', etc.
    title = Column(VARCHAR(45))
    author = Column(VARCHAR(45))
    publishing_house = Column(VARCHAR(45))  # e.g., 'Publisher Name'
    publishing_date = Column(VARCHAR(45))  # Date when the book was published


class Transaction(Base):
    __tablename__ = "transaction_history"

    transactionID = Column(Integer, autoincrement=True, primary_key=True)  # Assuming transactionID is unique
    ID = Column(VARCHAR(45))  # Foreign key to Member table
    bookID = Column(VARCHAR(45))  # Foreign key to Book table
    transactionType = Column(VARCHAR(45))
    dateborrowed = Column(DateTime, default=datetime.datetime.now())  # Date when the book was borrowed
    dueDate = Column(DateTime, default=datetime.datetime.now() + datetime.timedelta(days=7))  # Date when the book is due to be returned

Base.metadata.create_all(engine)

# Developer Fuctions for Test cases:
def test_Transaction():
    Session = sessionmaker(bind=engine)
    session = Session()

    test = Transaction(ID="2024-00697-MN-0", bookID="1")

    session.add(test)
    session.commit()

#test_Transaction()

