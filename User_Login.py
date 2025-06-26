''''
Library Management System (LSM) User Login Module
This module provides the login function for user management in the Library Management System (LSM).

Developer:
Queñano, Ethan Cielo Luc V.
BS CpE 1-5
Group 3

Program Date:
June 19, 2025
'''

# Import necessary libraries
# Import abstract base class for defining abstract classes
from abc import ABC, abstractmethod
from ORM_LSM import Member, Admin, engine
# Import necessary libraries for database management and ORM
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker


class Login(ABC):

    # Abstract Class for User Login Management
    # This class defines the structure for user login management in the Library Management System (LSM).

    # Abstract Class Properties

    @property
    @abstractmethod
    def ID(self):
        pass

    @property
    @abstractmethod
    def password(self):
        pass


class MemberLogin(Login):
    # Class for Member User Login Management
    # This class implements the abstract methods defined in the Login class for member users.
    # Class Attributes
    def __init__(self, ID, password, uname=None, firstname=None, surname=None, pup_webmail=None):
        self.__ID = ID
        self.__password = password
        self.__uname = uname
        self.__firstname = firstname
        self.__surname = surname
        self.__pup_webmail = pup_webmail

    # Abstract Class Properties
    @property
    def ID(self):
        return None

    @property
    def password(self):
        return None


    # Class Methods    
    def get_signup(self):
        # Function to create a new user account in the database
        Session = sessionmaker(bind=engine)

        # Create a new session
        session = Session()

        # Create a new user instance 
        user = Member(username=self.__uname, ID=self.__ID, firstname=self.__firstname, surname=self.__surname, pup_webmail=self.__pup_webmail, password=self.__password)

        # Add the user to the session
        session.add(user)

        # Commit the session to save the user to the database
        session.commit()

    def get_signin(self):
        # Function to login to user account
        Session = sessionmaker(bind=engine)

        # Create a new session
        session = Session()

        # Query the database for the user with the given studentID and password
        user = session.query(Member).filter_by(ID=self.__ID).one_or_none()

        # Check if user exists and password matches
        # If user is None, it means no user was found with the given studentID
        # If user is not None, we check if the password matches
        if user is None:
            print("Invalid student ID or password.") # PLEASE REPLACE FOR GUI IMPLEMENTATION
            return
        if user.password == self.__password:
            print("Login successful!") # PLEASE REPLACE FOR GUI IMPLEMENTATION
            print(f"Student ID: {user.ID}\nUsername: {user.username}\nName: {user.firstname} {user.surname}\nPUP Webmail: {user.pup_webmail}") # PLEASE REMOVE FOR GUI IMPLEMENTATION (USED FOR TESTING PURPOSES)
        else:
            print("Invalid student ID or password.") # PLEASE REPLACE FOR GUI IMPLEMENTATION


class AdminLogin(Login):
    # Class for Member User Login Management
    # This class implements the abstract methods defined in the Login class for member users.
    # Class Attributes
    def __init__(self, ID, password):
        self.__ID = ID
        self.__password = password

    # Abstract Class Properties
    @property
    def ID(self):
        return None

    @property
    def password(self):
        return None

    # Class Methods    
    # Only Signin fuction is implemented for AdminLogin as Admins are manually added to the database by the IT and Lead Librarian for security purposes
    def get_signin(self):
        # Function to login to user account
        Session = sessionmaker(bind=engine)

        # Create a new session
        session = Session()

        # Query the database for the user with the given studentID and password
        user = session.query(Admin).filter_by(ID=self.__ID).one_or_none()

        # Check if user exists and password matches
        # If user is None, it means no user was found with the given studentID
        # If user is not None, we check if the password matches
        if user is None:
            print("Invalid student ID or password.") # PLEASE REPLACE FOR GUI IMPLEMENTATION
            return
        if user.password == self.__password:
            print("Login successful!")
            print(f"Student ID: {user.ID}\nUsername: {user.username}\nName: {user.firstname} {user.surname}\nPUP Webmail: {user.puplibrary_webmail}") # PLEASE REMOVE FOR GUI IMPLEMENTATION (USED FOR TESTING PURPOSES)
        else:
            print("Invalid student ID or password.") # PLEASE REPLACE FOR GUI IMPLEMENTATION



# Main Program Functions:
# Test the functionality of the User Login Module

def memberLogin():
    # Function to handle member login
    while True:  
        print("1. Sign Up")
        print("2. Sign In")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            uname = input("Enter username: ")
            student_id = input("Enter student ID: ")
            fname = input("Enter first name: ")
            sname = input("Enter surname: ")
            pupWebmail = input("Enter PUP Webmail: ")
            pword = input("Enter password: ")

            while True:
                # Validate password requirements
                if len(pword) < 8:
                    print("Password must be at least 8 characters long.")
                    pword = input("Enter password: ")
                    continue
                elif not any(char.isdigit() for char in pword):
                    print("Password must contain at least one digit.")
                    pword = input("Enter password: ")
                    continue
                elif not any(char.isupper() for char in pword):
                    print("Password must contain at least one uppercase letter.")
                    pword = input("Enter password: ")
                    continue
                elif not any(char.islower() for char in pword):
                    print("Password must contain at least one lowercase letter.")
                    pword = input("Enter password: ")
                    continue
                else:
                    break

            while True:
                # Confirm password
                confirm_pword = input("Confirm password: ")
                if pword != confirm_pword:
                    print("Passwords do not match. Please try again.")
                    continue
                else:
                    print("Passwords match. You may proceed.")
                    break

            # Call the signup function with the provided details
            login = MemberLogin(student_id, pword, uname, fname, sname, pupWebmail)
            login.get_signup()
            # Print success message
            print("Sign up successful! You can now sign in.")

        elif choice == '2':
            student_id = input("Enter student ID: ")
            pword = input("Enter password: ")
            uname = None
            fname = None
            sname = None
            pupWebmail = None
            # Call the signin function with the provided credentials
            login = MemberLogin(student_id, pword)
            login.get_signin()

        elif choice == '3':
            print("Exiting the User Management System. Goodbye!")
            break

        else:
            print("Invalid choice, please try again.") # Error handling for invalid input
            continue

def adminLogin():
    # Function to handle member login
    while True:  
        print("1. Sign In")
        print("2. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            id = input("Enter Faculty ID: ")
            pword = input("Enter password: ")
            # Call the signin function with the provided credentials
            login = AdminLogin(id, pword)
            login.get_signin()

        elif choice == '2':
            print("Exiting the User Management System. Goodbye!")
            break

        else:
            print("Invalid choice, please try again.") # Error handling for invalid input
            continue


# Function to handle user login and management
def userlogin():
    # Main Function to login to user account
    # Program loop for user management system
    while True:
        print("\nWelcome to the LSM User Management System \nPlease choose an option:")
        # Display options for user management
        print("1. Member Login")
        print("2. Admin Login")
        print("3. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            # Call the member login function
            memberLogin()
        elif choice == '2':
            adminLogin()
        elif choice == '3':
            print("Exiting the User Management System. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.") # Error handling for invalid input
            continue




# Run main function if this script is executed directly
if __name__ == "__main__":
    userlogin()