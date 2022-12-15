#Import the required modules
import mysql.connector
from mysql.connector import Error


#Connect to the MySQL Database (lms)
#Create a MySQL Connection object
connection = mysql.connector.connect(host='localhost', #Host name, running on 'localhost' or IP = 127.0.0.0
                                         database='lms', #Database name
                                         user='root', #Username
                                         password='nake') #Password

#Create a Cursor object to perform various SQL operations
cursor = connection.cursor()


#Function to check the credentials of the user
def checkCredential():
    print("\n")
    print("Hello! This is the Home Page")
    
    #Choose one of the below options to move forward
    print("1. Student sign in")
    print("2. Student sign up")
    print("3. Faculty sign in")
    print("4. Faculty sign up")
    print("5. Admin sign in")

    #Other options that can be accessed without logging in
    print("6. Display books")
    print("7. Number of books available")
    print("8. Number of distinct books available")
    print("9. Exit")
    choice = input('Choose an option: ')
    
    if(choice == '1'):
        stuSignIn()
    elif(choice == '2'):
        stuSignUp()
    elif(choice == '3'):
        facSignIn()
    elif(choice == '4'):
        facSignUp()
    elif(choice == '5'):
        adminSignIn()
    elif(choice == '6'):
        displayBooks()
    elif(choice == '7'):
        countBooks()
    elif(choice == '8'):
        countDistinctBooks()
    elif(choice == '9'):
        exit()


#Sign in method for the admin/owner
def adminSignIn():
    print("\n")
    print("Hello! This is where the admin can sign in")

    #Enter all the admin details to login
    adm_id = int(input("Enter your ID: "))
    adm_first_name = input("Enter your first name: ")
    adm_last_name = input("Enter your last name: ")
    adm_email = input("Enter your email: ")
    
    sql_get_id = """ select * from admin;""" #SQL SELECT to get all the attributes and tuples from 'admin' table
    cursor.execute(sql_get_id)
    record = cursor.fetchall()

    signed_in = False
    for row in record:
        if adm_id == row[0] and adm_first_name == row[1] and adm_last_name == row[2] and adm_email == row[3]: #Check if the retrieved data from 'admin' table matches the user entered data
            print("Singned in successfully")
            signed_in = True
            mainAdmin(adm_id)

    if signed_in == False: #If user entered data does not match the retrieved data from 'admin' table
        print("You are not the admin, you will be redirected to earlier page")
        checkCredential()


#Sign in method for Students        
def stuSignIn():
    print("\n")
    print("Hello! This is where students can sign in")

    #Enter the Student ID to login
    stu_id = int(input("Enter your Student ID: "))
    
    sql_get_id = """select * from students;""" #SQL SELECT to get all the attributes and tuples from 'students' table
    cursor.execute(sql_get_id)
    record = cursor.fetchall()

    signed_in = False
    for row in record: #Check if the user entered data(id) matches any of the retrieved data from 'students' table
        if stu_id == row[0]:
            print("Signed in successfully")
            signed_in = True
            mainStudent(stu_id)
            
    if signed_in == False: #If user entered data does not match the retrieved data from 'students' table
        print("You are not a member here, so you will be redirected to Students Sign Up page")
        stuSignUp()            
            
#Sign up method for Students
def stuSignUp():
    print("\n")
    print("Hello! This is where students can sign up")

    #Enter the Students' details
    stu_id = int(input("Enter your Student ID: "))
    stu_first_name = input("Enter your First Name: ")
    stu_last_name = input("Enter your Last Name: ")
    stu_email = input("Enter your Email ID: ")
    
    sql_select_cred = """select * from students;""" #SQL SELECT to get all the attributes and tuples from 'students' table
    cursor.execute(sql_select_cred)
    record = cursor.fetchall()
    
    ok_for_sign_up = True
    for row in record:
        if stu_id == row[0]: #Student ID matches the data retrieved from 'students' table
            print("There is already an account registered with this Student ID, so you will be redirected to the Students Sign In page")
            ok_for_sign_up = False
            stuSignIn()
        elif stu_email == row[3]: #Student Email matches the data retrieved from 'students' table
            print("There is already an account registered with this Email ID, so you will be redirected to the Students Sign In page")
            ok_for_sign_up = False
            stuSignIn()
            
    if ok_for_sign_up == True: #No data retrieved from 'students' table matches with the user entered detatils    
        try:
            sql_insert_cred = """insert into students (stu_id, stu_first_name, stu_last_name, stu_email) values (%s, %s, %s, %s);""" #SQL INSERT to insert Student details in 'students' table
            row_insert = (stu_id, stu_first_name, stu_last_name, stu_email)
            cursor.execute(sql_insert_cred, row_insert)
            connection.commit()
            print("Sing Up successfull")
            mainStudent(stu_id)
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL row {}".format(error))


#Sign in method for faculty
def facSignIn():
    print("\n")
    print("Hello! This is where faculty can sign in")

    #Enter Faculty ID
    fac_id = int(input("Enter your Faculy ID: "))
    
    sql_get_id = """select * from faculty;""" #SQL SELECT to get all attributes and tuples from 'faculty' table
    cursor.execute(sql_get_id)
    record = cursor.fetchall()

    signed_in = False
    for row in record:
        if fac_id == row[0]: #If the entered ID matches the data retrieved from 'faculty' table
            print("Signed in successfully")
            signed_in = True
            mainFaculty(fac_id)
            
    if signed_in == False: #If user entered data does not match with the data retrieved from 'faculty' table
        print("You are not a member here, so you will be redirected to Faculty Sign Up page")
        facSignUp()


#Sign up method for Faculty        
def facSignUp():
    print("\n")
    print("Hello! This is where faculty can sign up")

    #Enter Faculty details
    fac_id = int(input("Enter your Faculy ID: "))
    fac_first_name = input("Enter your First Name: ")
    fac_last_name = input("Enter your Last Name: ")
    fac_email = input("Enter your Email ID: ")
    
    sql_select_cred = """select * from faculty;""" #SQL SELECT to get all attributes and tuples from 'faculty' table
    cursor.execute(sql_select_cred)
    record = cursor.fetchall()
    
    ok_for_sign_up = True
    for row in record:
        if fac_id == row[0]: #Check if user entered ID matches with the data retrieved from 'faculty' table
            print("There is already an account registered with this Faculty ID, so you will be redirected to the Faculty Sign In page")
            ok_for_sign_up = False
            facSignIn()
        elif fac_email == row[3]: #Check if user entered Email matches with the data retrieved from 'faculty' table
            print("There is already an account registered with this Email ID, so you will be redirected to the Faculty Sign In page")
            ok_for_sign_up = False
            facSignIn()
            
    if ok_for_sign_up == True:        
        try:
            sql_insert_cred = """insert into faculty (fac_id, fac_first_name, fac_last_name, fac_email) values (%s, %s, %s, %s);""" #SQL INSERT to insert Faculty details in the 'faculty' table
            row_insert = (fac_id, fac_first_name, fac_last_name, fac_email)
            cursor.execute(sql_insert_cred, row_insert)
            connection.commit()
            print("Sign Up successfull")
            mainFaculty(fac_id)
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL row {}".format(error))


#Method to search Book by its Title, for Students
def stuSearchByBookName(stu_id):
    print("\n")
    print("Hello! This is where students can rent book, based on Book Name")

    #Enter Book details
    book_name = input("Enter the book name: ")
    book_edition = int(input("Enter the edition: "))
    
    sql_select_books = """select * from books;""" #SQL SELECT to fetch all data from 'books' table
    cursor.execute(sql_select_books)
    record = cursor.fetchall()

    book_found = False
    for row in record:
        if book_name == row[1] and book_edition == row[2]: #Check if the user entered book details matches with the data fetched from 'books' table
            if row[4] == 0: #Check if the number of books available is zero
                print("Your request is currently not available here, please check for a different book")
                stuSearchByBookName(stu_id)
            try:
                sql_update_book = """update books set book_available_count = book_available_count - 1 where (book_name = %s and book_edition = %s);""" #SQL UPDATE on 'books' table to decrement the count on number of books available
                row_update = (book_name, book_edition)
                cursor.execute(sql_update_book, row_update)
                connection.commit()

                sql_select_stu = """select stu_id from track_stu_rent;""" #SQL SELECT to get 'stu_id' column from 'track_stu_rent' table
                cursor.execute(sql_select_stu)
                stu_rows = cursor.fetchall()
                
                stu_row_found = False
                for r in stu_rows:
                    if stu_id == r[0]: #If the user's ID is already present in 'track_stu_rent' table, that is, the user already has 1 or more books rented
                        sql_update_stu = """update track_stu_rent set books_rented = books_rented + 1 where stu_id = %s;""" #SQL UPDATE to increment number of books rented for this user in 'track_stu_rent' table
                        cursor.execute(sql_update_stu, (stu_id,))
                        connection.commit()
                        stu_row_found = True
                if stu_row_found == False: #If the user's ID is not present in 'track_stu_rent' table, that is, the user has not rented any book yet
                    sql_insert_stu = """insert into track_stu_rent values (%s, %s);""" #SQL INSERT to insert 'stu_id' and 'books_rented' = 1 into the 'track_stu_rent' table
                    stu_row = (stu_id, 1)
                    cursor.execute(sql_insert_stu, stu_row)
                    connection.commit()
                        
                print("Book has been rented by you")
                book_found = True
                mainStudent(stu_id)
            except mysql.connector.Error as error:
                print("Failed to update MySQL row {}".format(error))
    if book_found == False: #If book is not found in the 'books' table
        print("Your request is currently not available here, please check for a different book")
        stuSearchByBookName(stu_id)


#Method to seach Book by Title, for Faculty
def facSearchByBookName(fac_id):
    print("\n")
    print("Hello! This is where faculty can rent book, based on Book Name")

    #Enter Book details
    book_name = input("Enter the book name: ")
    book_edition = int(input("Enter the edition: "))
    
    sql_select_books = """select * from books;""" #SQL SELECT to fetch all data from 'books' table
    cursor.execute(sql_select_books)
    record = cursor.fetchall()

    book_found = False
    for row in record:
        if book_name == row[1] and book_edition == row[2]: #Check if the user entered details matches with the data fetched from 'books' table
            if row[4] == 0: #Check if the number of books available is zero
                print("Your request is currently not available here, please check for a different book")
                facSearchByBookName(fac_id)
            try:
                sql_update_book = """update books set book_available_count = book_available_count - 1 where (book_name = %s and book_edition = %s);""" #SQL UPDATE to decrement the number of books available in the 'books' table
                row_update = (book_name, book_edition)
                cursor.execute(sql_update_book, row_update)
                connection.commit()

                sql_select_fac = """select fac_id from track_fac_rent;""" #SQL SELECT to get 'fac_id' column from the 'track_fac_rent' table
                cursor.execute(sql_select_fac)
                fac_rows = cursor.fetchall()
                
                fac_row_found = False
                for r in fac_rows:
                    if fac_id == r[0]: #If the user entered ID is present in the 'track_fac_rent' table, that is, the user has rented 1 or more books
                        sql_update_fac = """update track_fac_rent set books_rented = books_rented + 1 where fac_id = %s;""" #SQL UPDATE to increment 'books_rented' column in the 'track_fac_rent' table
                        cursor.execute(sql_update_fac, (fac_id,))
                        connection.commit()
                        fac_row_found = True
                if fac_row_found == False: #If the user entered ID is absent in the 'track_fac_rent' table, that is, the user has not rented any book yet
                    sql_insert_fac = """insert into track_fac_rent values (%s, %s);""" #SQL INSERT to insert 'fac_id' and 'books_rented' = 1 in the 'track_fac_rent' table
                    fac_row = (fac_id, 1)
                    cursor.execute(sql_insert_fac, fac_row)
                    connection.commit()
                        
                print("Book has been rented by you")
                book_found = True
                mainFaculty(fac_id)
            except mysql.connector.Error as error:
                print("Failed to update MySQL row {}".format(error))

    if book_found == True: #If the book is present in the 'books' table
        print("Your request is currently not available here, please check for a different book")
        facSearchByBookName(fac_id)
            

#Method to search Book by Author, for Student
def stuSearchByBookAuthor(stu_id):
    print("\n")
    print("Hello! This is where Students can rent book, based on book author")

    #Enter Book details
    book_name = input("Enter book name: ")
    book_edition = int(input("Enter book edition: "))
    count = int(input("Enter number of authors (not more than 3): ")) #Check the number of authors and take input accordingly
    if count == 1:
        book_author_1 = input("Enter book author 1: ")
        book_author_2 = "NULL"
        book_author_3 = "NULL"
    elif count == 2:
        book_author_1 = input("Enter book author 1: ")
        book_author_2 = input("Enter book author 2: ")
        book_author_3 = "NULL"
    else:
        book_author_1 = input("Enter book author 1: ")
        book_author_2 = input("Enter book author 2: ")
        book_author_3 = input("Enter book author 3: ")

    #SQL SELECT to get specified attributes after joining (Natural Join) 'books' and 'author' tables    
    sql_select_books_author = """select book_name, book_edition, author_1, author_2, author_3, book_available_count from books natural join author;"""
    cursor.execute(sql_select_books_author)
    record = cursor.fetchall()

    book_found = False
    for row in record:
        if book_name == row[0] and book_edition == row[1] and book_author_1 == row[2] and book_author_2 == row[3] and book_author_3 == row[4]: #Check if the required book is present in the 'books' table
            if row[5] == 0: #If the number of books available is zero
                print("Your request is currently not available here, please check for a different book")
                stuSearchByBookAuthor(stu_id)
            
            try:
                sql_update_book = """update books set book_available_count = book_available_count - 1 where (book_name = %s and book_edition = %s);""" #SQL UPDATE to decrement the 'book_available_count' value for the corresponding tuple
                row_update = (book_name, book_edition)
                cursor.execute(sql_update_book, row_update)
                connection.commit()

                sql_select_stu = """select stu_id from track_stu_rent;""" #SQL SELECT to get the ID of signed in user from 'track_stu_rent' table
                cursor.execute(sql_select_stu)
                stu_rows = cursor.fetchall()
                
                stu_row_found = False
                for r in stu_rows:
                    if stu_id == r[0]: #Check if the ID of the signed in user is present in the 'track_stu_rent' table
                        sql_update_stu = """update track_stu_rent set books_rented = books_rented + 1 where stu_id = %s;""" #SQL UPDATE to increment the value in 'books_rented' column in the 'track_stu_rent' table
                        cursor.execute(sql_update_stu, (stu_id,))
                        connection.commit()
                        stu_row_found = True
                        
                if stu_row_found == False: #If the signed in user has not rented any Book(s) yet
                    sql_insert_stu = """insert into track_stu_rent values (%s, %s);""" #SQL INSERT to add the ID in 'stu_id' column and 'books_rented' = 1, in the 'track_stu_rent' table
                    stu_row = (stu_id, 1)
                    cursor.execute(sql_insert_stu, stu_row)
                    connection.commit()
                        
                print("Book has been rented by you")
                book_found = True
                mainStudent(stu_id)
                
            except mysql.connector.Error as error:
                print("Failed to update MySQL row {}".format(error))

    if book_found == False: #If the desired Book is not available in the 'books' table
        print("Your request is currently not available here, please check for a different book")
        stuSearchByBookAuthor(stu_id)
        

#Method to search Book by Author, for Faculty
def facSearchByBookAuthor(fac_id):
    print("\n")
    print("Hello! This is where Faculty can rent book, based on book author")

    #Enter Book details
    book_name = input("Enter book name: ")
    book_edition = int(input("Enter book edition: "))
    count = int(input("Enter number of authors (not more than 3): ")) #Check the number of authors and take input accordingly
    if count == 1:
        book_author_1 = input("Enter book author 1: ")
        book_author_2 = "NULL"
        book_author_3 = "NULL"
    elif count == 2:
        book_author_1 = input("Enter book author 1: ")
        book_author_2 = input("Enter book author 2: ")
        book_author_3 = "NULL"
    else:
        book_author_1 = input("Enter book author 1: ")
        book_author_2 = input("Enter book author 2: ")
        book_author_3 = input("Enter book author 3: ")

    #SQL SELECT to get specified attributes after joining (Natural Join) 'books' and 'author' tables        
    sql_select_books_author = """select book_name, book_edition, author_1, author_2, author_3, book_available_count from books natural join author;"""
    cursor.execute(sql_select_books_author)
    record = cursor.fetchall()

    book_found = False
    for row in record:
        if book_name == row[0] and book_edition == row[1] and book_author_1 == row[2] and book_author_2 == row[3] and book_author_3 == row[4]: #Check if the required book is present in the 'books' table
            if row[5] == 0: #If the number of books available is zero
                print("Your request is currently not available here, please check for a different book")
                facSearchByBookAuthor(fac_id)
            
            try:
                sql_update_book = """update books set book_available_count = book_available_count - 1 where (book_name = %s and book_edition = %s);""" #SQL UPDATE to decrement the 'book_available_count' value for the corresponding tuple
                row_update = (book_name, book_edition)
                cursor.execute(sql_update_book, row_update)
                connection.commit()

                sql_select_fac = """select fac_id from track_fac_rent;""" #SQL SELECT to get the ID of signed in user from 'track_fac_rent' table
                cursor.execute(sql_select_fac)
                fac_rows = cursor.fetchall()
                
                fac_row_found = False
                for r in fac_rows:
                    if fac_id == r[0]: #Check if the ID of the signed in user is present in the 'track_fac_rent' table
                        sql_update_fac = """update track_fac_rent set book_rented = book_rented + 1 where fac_id = %s;""" #SQL UPDATE to increment the value in 'books_rented' column in the 'track_fac_rent' table
                        cursor.execute(sql_update_fac, (fac_id,))
                        connection.commit()
                        fac_row_found = True
                        
                if fac_row_found == False: #If the signed in user has not rented any Book(s) yet
                    sql_insert_fac = """insert into track_fac_rent values (%s, %s);""" #SQL INSERT to add the ID in 'fac_id' column and 'books_rented' = 1, in the 'track_fac_rent' table
                    fac_row = (fac_id, 1)
                    cursor.execute(sql_insert_fac, fac_row)
                    connection.commit()
                        
                print("Book has been rented by you")
                book_found = True
                mainFaculty(fac_id)
                
            except mysql.connector.Error as error:
                print("Failed to update MySQL row {}".format(error))

    if book_found == False: #If the desired Book is not available in the 'books' table
        print("Your request is currently not available here, please check for a different book")
        facSearchByBookAuthor(fac_id)    


#Method to Rent Books for a Student
def rentStuBooks(stu_id):
    print("\n")
    print("Hello! This is the Students' Book Rent Page")

    #Choose an option
    print("Search by - ")
    print("1. Book name")
    print("2. Book author")
    print("3. Go back to Students' Home Page")
    choice = input('Choose an option: ')

    if(choice == '1'):
        stuSearchByBookName(stu_id)
    elif(choice == '2'):
        stuSearchByBookAuthor(stu_id)
    elif(choice == '3'):
        mainStudent(stu_id)


#Method to Rent Books for a Faculty
def rentFacBooks(fac_id):
    print("\n")
    print("Hello! This is the Faculty's Book Rent Page")

    #Choose an option
    print("Search by - ")
    print("1. Book name")
    print("2. Book author")
    print("3. Go back to Faculty Home Page")
    choice = input('Choose an option: ')

    if(choice == '1'):
        facSearchByBookName(fac_id)
    elif(choice == '2'):
        facSearchByBookAuthor(fac_id)
    elif(choice == '3'):
        mainFaculty(fac_id)


#Method to check the Rented Books by a Student
def checkStuRentedBooks(stu_id):
    print("\n")
    print("Hello! This is where Students can check their rented books")
    
    try:
        sql_select_stu_row = """select * from track_stu_rent where stu_id = %s;""" #SQL SELECT to get data from 'track_stu_rent' table for the signed in user
        cursor.execute(sql_select_stu_row,(stu_id,))
        record = cursor.fetchall()
        
        stu_row_found = False
        for row in record:
            if stu_id == row[0]: #Check if the signed in user has already rented any Books
                print("Student ID = ", row[0], )
                print("Number of books rented = ", row[1])
                print("Going back to Home Page")
                stu_row_found = True
                mainStudent(stu_id)
        if stu_row_found == False: #If the signed in user has not yet rented any Books
            print("You do not have any books rented!")
            print("Going back to Students' Home Page")
            mainStudent(stu_id)
            
    except mysql.connector.Error as error:
        print("Failed to get MySQL row {}".format(error))     


#Method to check the Rented Books by a Faculty
def checkFacRentedBooks(fac_id):
    print("\n")
    print("Hello! This is where Faculty can check their rented books")
    
    try:
        sql_select_fac_row = """select * from track_fac_rent where fac_id = %s;""" #SQL SELECT to get data from 'track_fac_rent' table for the signed in user
        cursor.execute(sql_select_fac_row,(fac_id,))
        record = cursor.fetchall()
        
        fac_row_found = False
        for row in record:
            if fac_id == row[0]: #Check if the signed in user has already rented any Books
                print("Faculty ID = ", row[0], )
                print("Number of books rented = ", row[1])
                print("Going back to Home Page")
                fac_row_found = True
                mainFaculty(fac_id)
        if fac_row_found == False: #If the signed in user has not yet rented any Books
            print("You do not have any books rented!")
            print("Going back to Faculty's Home Page")
            mainFaculty(fac_id)
    except mysql.connector.Error as error:
        print("Failed to get MySQL row {}".format(error))


#Method to check dues for a Student
def stuCheckMyDues(stu_id):
    print("\n")
    print("Hello! This is where Students can check their dues")
    print("Cost of any book for any student is constant = $2")
    cost = 2 #Cost of any book rented by a Student
    
    try:
        sql_select_stu_row = """select * from track_stu_rent where stu_id = %s;""" #SQL SELECT to get all data from 'track_stu_rent' table of the signed in user
        cursor.execute(sql_select_stu_row,(stu_id,))
        record = cursor.fetchall()
        
        stu_row_found = False
        for row in record:
            if stu_id == row[0]: #Check if the signed in user has any rented book
                print("Student ID = ", row[0], )
                cost = row[1] * 2 #Cost = number of books rented * 2
                print("You have to pay $", cost, "by the end of this semester");
                stu_row_found = True

        if stu_row_found == False: #If the signed user has not rented any book yet
            print("You do not have any books rented!")
            print("Going back to Students' Home Page")
            mainStudent(stu_id)
        if stu_row_found == True:
            print("Redirecting back to Students' Home Page")
            mainStudent(stu_id)
            
    except mysql.connector.Error as error:
        print("Failed to get MySQL row {}".format(error))


#Method to check the dues of a Faculty
def facCheckMyDues(fac_id):
    print("\n")
    print("Hello! This is where Faculty can check their dues")
    print("Cost of any book for any faculty is constant = $4")
    cost = 4 #Cost of any book rented by a Faculty
    
    try:
        sql_select_fac_row = """select * from track_fac_rent where fac_id = %s;""" #SQL SELECT to fetch all data from 'track_fac_rent' table of the signed in user
        cursor.execute(sql_select_fac_row,(fac_id,))
        record = cursor.fetchall()
        
        fac_row_found = False
        for row in record:
            if fac_id == row[0]: #Check if the ID of signed is present in the 'track_fac_rent' table.
                print("Faculty ID = ", row[0], )
                cost = row[1] * 4 #Cost = number of books rented * 4
                print("You have to pay $", cost, "by the end of this semester");
                fac_row_found = True

        if fac_row_found == False: #If the signed in user has not rented any book yet
            print("You do not have any books rented!")
            print("Going back to Faculty's Home Page")
            mainFaculty(fac_id)
        if fac_row_found == True:
            print("Redirecting back to Faculty Home Page")
            mainFaculty(fac_id)
            
    except mysql.connector.Error as error:
        print("Failed to get MySQL row {}".format(error))


#Method to add a book in the Library, done by Admin
def insertBook(adm_id):
    print("\n")
    print("Hello! This is where you can add a new book for the library")
    
    book_id = 0
    #Enter Book details
    book_name = input("Enter book name: ")
    book_edition = int(input("Enter book edition: "))
    book_publisher = input("Enter book publisher: ")
    book_available_count = int(input("Enter number of books available: "))
    count = int(input("Enter number of authors (valid options are 1,2 or 3): ")) #Check the number of authors and take input accordingly
    if count == 1:
        author_1 = input("Enter book author 1: ")
        author_2 = "NULL"
        author_3 = "NULL"
    elif count == 2:
        author_1 = input("Enter book author 1: ")
        author_2 = input("Enter book author 2: ")
        author_3 = "NULL"
    else:
        author_1 = input("Enter book author 1: ")
        author_2 = input("Enter book author 2: ")
        author_3 = input("Enter book author 3: ")

    book_inserted = False
    author_inserted = False
    try:
        sql_insert_row = """insert into books (book_name, book_edition, book_publisher, book_available_count) values (%s, %s, %s, %s);""" #SQL INSERT to add a new tuple in the 'books' table
        row_insert = (book_name, book_edition, book_publisher, book_available_count)
        cursor.execute(sql_insert_row, row_insert)
        connection.commit()
        book_inserted = True
    except mysql.connector.Error as error:
        print("Failed to insert MySQL book row, book {}".format(error))

    try:
        sql_get_id = """select book_id from books where book_name = %s and book_edition = %s and book_publisher = %s and book_available_count = %s""" #SQL SELECT to get 'book_id' of the Book that was just inserted in the 'books' table
        row_find = (book_name, book_edition, book_publisher, book_available_count)
        cursor.execute(sql_get_id, row_find)
        record = cursor.fetchall()
        for row in record:
            book_id = row[0]
    except mysql.connector.Error as error:
        print("Failed to get MySQL row {}".format(error))
 
    try:
        sql_insert_row = """insert into author (book_id, author_1, author_2, author_3) values (%s, %s, %s, %s);""" #SQL INSERT to add the Authors in the 'author' table, for the corresponding Book that was inserted
        row_insert = (book_id, author_1, author_2, author_3)
        cursor.execute(sql_insert_row, row_insert)
        connection.commit()
        author_inserted = True
    except mysql.connector.Error as error:
        print("Failed to insert MySQL author row {}".format(error))

    if book_inserted == True and author_inserted == True: #Check if both, book and authors, are inserted in the 'books' and 'author' tables respectively
        print("Book inserted! redirecting to Admin Home Page")
        mainAdmin(adm_id)


#Method to delete a book(s) from the Library, done by Admin    
def removeBook(adm_id):
    print("\n")
    print("Hello! This is where you can remove an existing book(s) from the Library")

    #Enter the Book details
    book_name = input("Enter book name: ")
    book_edition = int(input("Enter book edition: "))
    book_publisher = input("Enter book publisher: ")

    book_deleted = False
    try:
        sql_delete_row = """delete from books where book_name = %s and book_edition = %s and book_publisher = %s;""" #SQL DELETE to to delete the specified tuple from the 'books' table
        row_delete = (book_name, book_edition, book_publisher)
        cursor.execute(sql_delete_row, row_delete)
        connection.commit()
        book_deleted = True
    except mysql.connector.Error as error:
        print("Failed to delete MySQL row, book {}".format(error))
            
    if book_deleted == True:
        print("Book deleted! redirecting to Admin Home Page")
        mainAdmin(adm_id)


#Method to display all the distinct books available in the Library.
def displayBooks():
    print("\n")
    print("Here is a list of various Computer Science books that are available in my Library")

    try:
        sql_select = """select * from v1;""" #SQL SELECT to fetch data from View 'v1'
        cursor.execute(sql_select,) 
        record = cursor.fetchall()
        
        for row in record:
            print(row)
            print("\n")
        print("Redirecting back to Home Page")
        checkCredential()
        
    except mysql.connector.Error as error:
        print("Failed to get MySQL row {}".format(error))
        

#Method to count the number of books available in the Library
def countBooks():
    print("\n")
    print("The total number of books available in this library are - ")

    try:
        sql_select_count = """select sum(book_available_count) as count from books;""" #SQL SELECT to get the sum of tuples under 'book_available_count' table in the 'books' table
        cursor.execute(sql_select_count,)
        record = cursor.fetchall()
        
        for row in record:
            print(row[0])
        print("Redirecting back to Home Page")
        checkCredential()
        
    except mysql.connector.Error as error:
        print("Failed to get MySQL row {}".format(error))


#Method to count the number of distinct books available in the Library
def countDistinctBooks():
    print("\n")
    print("The total number of distinct books available in this library are - ")

    try:
        sql_select_distinct_count = """select count(book_id) as count from books;""" #SQL SELECT to get the count of 'book_id' column in the 'books' table
        cursor.execute(sql_select_distinct_count,)
        record = cursor.fetchall()
        
        for row in record:
            print(row[0])
        print("Redirecting back to Home Page")
        checkCredential()

    except mysql.connector.Error as error:
        print("Failed to get MySQL row {}".format(error))



#Main method for Stuents        
def mainStudent(stu_id):
    print("\n")
    print("Hello! This is the Home Page for Students")

    #Choose an option
    print("1. Rent books")
    print("2. Check my dues")
    print("3. Check my rented books")
    print("4. Go to Home Page")
    choice = input('Choose an option: ')
    
    if(choice == '1'):
        rentStuBooks(stu_id)
    elif(choice == '2'):
        stuCheckMyDues(stu_id)
    elif(choice == '3'):
        checkStuRentedBooks(stu_id)
    elif(choice == '4'):
        checkCredential()


#Main method for Admin/Owner
def mainAdmin(adm_id):
    print("\n")
    print("Hello! This is the Home Page for Admin")

    #Choose an option
    print("1. Add a new book in the database")
    print("2. Delete an existing book")
    print("3. Go to Home Page")
    choice = input('Choose an option')

    if(choice == '1'):
        insertBook(adm_id)
    elif(choice == '2'):
        removeBook()
    elif(choice == '3'):
        checkCredential()


#Main method for Faculty
def mainFaculty(fac_id):
    print("\n")
    print("Hello! This is the Home Page for Faculty")

    #Choose an option
    print("1. Rent books")
    print("2. Check my dues")
    print("3. Check my rented books")
    print("4. Go to Home Page")
    choice = input('Choose an option: ')
    
    if(choice == '1'):
        rentFacBooks(fac_id)
    elif(choice == '2'):
        facCheckMyDues(fac_id)
    elif(choice == '3'):
        checkFacRentedBooks(fac_id)
    elif(choice == '4'):
        checkCredential()

#Program starts here
print("Welcome to the Library Management System, by Nake S. Aparanji")
print("\n")
checkCredential() #call the function to sign in/sign up
    
        
