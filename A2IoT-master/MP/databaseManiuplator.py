import MySQLdb
from prettytable import PrettyTable 
from prettytable import from_db_cursor


class cloudDatabase:
    HOST = "35.201.3.196"
    USER = "root"
    PASSWORD = "password"
    DATABASE = "iotA2"

    def __init__(self, connection = None):
        if(connection == None):
            connection = MySQLdb.connect(cloudDatabase.HOST, cloudDatabase.USER, cloudDatabase.PASSWORD, cloudDatabase.DATABASE)
        self.connection = connection

    def close(self):
        self.connection.close()
    
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()
    
    def createUser(self):
        with self.connection.cursor() as cursor:
            cursor.execute(""" CREATE TABLE IF NOT EXISTS LmsUser (
                LmsUserID int(25) not null auto_increment,
                UserName nvarchar(256) not null,
                Email nvarchar(256) not null,
                constraint PK_LmsUser primary key (LmsUserID),
                constraint UN_UserName unique (UserName)
            )""")
        self.connection.commit()
    
    def createBook(self):
        with self.connection.cursor() as cursor:
            cursor.execute(""" CREATE TABLE IF NOT EXISTS Book (
                BookID int(25) not null auto_increment,
                Title text not null,
                Author text not null,
                PublishedDate date not null,
                constraint PK_Book primary key (BookID)
            )""")
        self.connection.commit()
    
    def createBorrowed(self):
        with self.connection.cursor() as cursor:
            cursor.execute(""" CREATE TABLE IF NOT EXISTS BookBorrowed (
                BookBorrowedID int(25) not null auto_increment,
                LmsUserID int not null,
                BookID int not null,
                Status enum ('borrowed', 'returned'),
                BorrowedDate date not null,
                ReturnedDate date null,
                eventID nvarchar(5) not null,
                constraint PK_BookBorrowed primary key (BookBorrowedID),
                constraint FK_BookBorrowed_LmsUser foreign key (LmsUserID) references LmsUser (LmsUserID),
                constraint FK_BookBorrowed_Book foreign key (BookID) references Book (BookID)
            )""")
        self.connection.close()
    
    def insertBook(self, title, author, pubDate):
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT INTO Book (Title,Author,PublishedDate) VALUES (%s, %s, %s)", (title, author, pubDate,))
        self.connection.commit()
        self.connection.close()
        return cursor.rowcount == 1
    
    def userExist(self,username):
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT * FROM LmsUser WHERE UserName = %s', (username,))
            rows = cursor.fetchone()
        self.connection.close()
        return rows

    def insertUser(self, username, email):
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT INTO LmsUser (UserName, Email) VALUES (%s,%s)", (username, email,))
        self.connection.commit()
        self.connection.close()


    #SEARCH FUNCTIONS
    def searchByID(self, id):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * from Book WHERE BookID = %s", (id,))
            rows = cursor.fetchone()
        return rows

    def searchByTitle(self, title):
        with self.connection.cursor() as cursor:
            sql='SELECT * FROM Book WHERE Title LIKE %s'
            args=['%'+title+'%']
            cursor.execute(sql,args)
            rows = cursor.fetchall()
        return rows

    def searchByAuthor(self, author):
        with self.connection.cursor() as cursor:
            sql='SELECT * FROM Book WHERE Author LIKE %s'
            args=['%'+author+'%']
            cursor.execute(sql,args)
            rows = cursor.fetchall()
        return rows

     #BORROWING FUNCTIONS       

    def getBookID(self, bookid):
        with self.connection.cursor() as cursor:
            sqlq1='SELECT BookID FROM Book WHERE BookID = %s'
            args=[bookid]
            cursor.execute(sqlq1, args)
            rows = cursor.fetchone()
        self.connection.close()
        return rows

    def getUserID(self, userID):
        with self.connection.cursor() as cursor:
            sqlq1='SELECT LmsUserID FROM LmsUser WHERE UserName = %s'
            args=[userID]
            cursor.execute(sqlq1, args)
            rows = cursor.fetchone()
        self.connection.close()
        return rows

    def getTitle(self, bookid):
        with self.connection.cursor() as cursor:
            sqlq1='SELECT Title FROM Book WHERE BookID = %s'
            args=[bookid]
            cursor.execute(sqlq1, args)
            rows = cursor.fetchone()
        self.connection.close()
        return rows
    
    def insertToBorrow(self, userID, bookID, status, date, eventID):
        with self.connection.cursor() as cursor:
            cursor.execute("""INSERT INTO BookBorrowed (LmsUserID, BookID, Status, BorrowedDate, eventID) VALUES (%s, %s, %s, %s,%s)""", (userID,bookID,status,date,eventID,))
        self.connection.commit()
        self.connection.close()

        return cursor.rowcount == 1

    def checkIfBorrowed(self, bookID):
        with self.connection.cursor() as cursor:
            sql='SELECT Status from BookBorrowed WHERE BookID = %s'
            args=[bookID]
            cursor.execute(sql,args)
            rows = cursor.fetchone()
        self.connection.close()
        return rows
    
    def getEmail(self, userID):
        with self.connection.cursor() as cursor:
            sql='SELECT Email from LmsUser WHERE LmsUserID = %s'
            args=[userID]
            cursor.execute(sql,args)
            rows = cursor.fetchone()
        self.connection.close()
        return rows
    
    #RETURNING FUNCTIONS

    def listBorrowedBooksForUser(self, userID):
        with self.connection.cursor() as cursor:
            status = 'borrowed'
            sql='SELECT bb.BookBorrowedID, b.Title FROM BookBorrowed bb, Book b WHERE bb.LmsUserID = %s AND bb.BookID = b.BookID AND bb.Status = %s'
            args=[userID,status]
            cursor.execute(sql,args)
            rows = cursor.fetchall()
        self.connection.close()
        return rows
    
    def setToReturned(self, bookID, status, date):
        with self.connection.cursor() as cursor:
            sql='UPDATE BookBorrowed SET Status = %s, ReturnedDate = %s WHERE BookBorrowedID = %s'
            args=[status, date,bookID]
            cursor.execute(sql,args)
        self.connection.commit()
        self.connection.close()

    def getEventID(self, bbID):
        with self.connection.cursor() as cursor:
            sql='SELECT eventID FROM BookBorrowed WHERE BookBorrowedID = %s'
            args=[bbID]
            cursor.execute(sql,args)
            rows = cursor.fetchone()
            return rows
    def getBorrowID(self, userID, bookID):
        with self.connection.cursor() as cursor:
            status= 'borrowed'
            sql='SELECT bb.BookBorrowedID FROM BookBorrowed bb WHERE LmsUserID = %s AND bb.BookID = %s AND bb.Status = %s'
            args=[userID, bookID, status]
            cursor.execute(sql,args)
            return cursor.fetchone()








    #TESTING FUNCTIONS
    def populateBooks(self):
        books_to_insert = [ 
        ('In Search of Lost Time', 'Marcel Proust', '1913-05-11'),
        ('Don Quixote', 'Miguel de Cervantes', '1620-03-23'),
        ('Ulysses', 'James Joyce', '1904-06-16'),
        ('The Great Gatsby', 'F.Scott Fitzgerald', '1925-04-10'),
        ('Moby Dick', 'Herman Melville', '1851-11-12'),
        ('Hamlet', 'William Shakespeare', '1601-02-20'),
        ('War & Peace', 'Leo Tolstoy', '1869-03-21'),
        ('The Odyssey', 'Homer', '0080-01-01'),
        ('One Hundred Years of Solitude', 'Gabriel Garcia Marquez', '1967-05-12'),
        ('The Divine Comedy', 'Dante Alighieri', '1320-01-20'),
        ('The Brothers Karamazov', 'Fyodor Dostoyevsky', '1880-08-4'),
        ('Madame Bovary', 'Gustave Flaubert', '1856-09-01'),
        ('The Adventures of Huckleberry Fin', 'Mark Twain', '1884-12-10'),
        ('The Iliad', 'Homer', '0008-01-01'),
        ('Lolita', 'Vladimir Nabokov', '1955-09-14'),
        ('The Hobbit', 'J.R.R Tolkien', '1937-09-21')]

        sql_insert_query = """INSERT INTO Book (Title, Author, PublishedDate) VALUES (%s,%s,%s)"""

        with self.connection.cursor() as cursor:
            result = cursor.executemany(sql_insert_query, books_to_insert)
            self.connection.commit()

            print(cursor.rowcount, " Book Records inserted successfully")

    def populateBookBorrowed(self):
        bookBorrowed_to_insert = [
            ('1', '1', 'borrowed', '2019-05-17', '11111'),
            ('1', '2', 'borrowed', '2019-05-17', '22222'),
            ('1', '3', 'borrowed', '2019-05-17', '33333'),
            ('2', '4', 'borrowed', '2019-05-18', '44444'),
            ('2', '5', 'borrowed', '2019-05-18', '55555'),
            ('2', '6', 'borrowed', '2019-05-18', '66666'),
            ('3', '7', 'borrowed', '2019-05-19', '77777'),
            ('3', '8', 'borrowed', '2019-05-19', '88888'),
            ('3', '9', 'borrowed', '2019-05-19', '99999'),
            ('4', '10', 'borrowed', '2019-05-20', '10101'),
            ('4', '11', 'borrowed', '2019-05-20', '12121'),
            ('4', '12', 'borrowed', '2019-05-20', '13131'),
            ('1', '13', 'borrowed', '2019-05-21', '14141'),
            ('2', '14', 'borrowed', '2019-05-21', '15151'),
            ('3', '15', 'borrowed', '2019-05-22', '16161'),
            ('4', '16', 'borrowed', '2019-05-22', '17171')]

        sql_insert_query = """INSERT INTO BookBorrowed (LmsUserID, BookID, Status, BorrowedDate, eventID) VALUES (%s,%s,%s,%s,%s)"""

        with self.connection.cursor() as cursor:
            result = cursor.executemany(sql_insert_query, bookBorrowed_to_insert)
            self.connection.commit()

            print(cursor.rowcount, "Book Borrowed records inserted succesfully")
    
    def populateBookReturned(self):
        bookReturnd = [
            ('returned', '2019-05-24', '1'),
            ('returned', '2019-05-24', '2'),
            ('returned', '2019-05-25', '3'),
            ('returned', '2019-05-25', '4'),
            ('returned', '2019-05-25', '5'),
            ('returned', '2019-05-26', '6'),
            ('returned', '2019-05-27', '7'),
            ('returned', '2019-05-27', '8'),
            ('returned', '2019-05-27', '9'),
            ('returned', '2019-05-27', '10'),
            ('returned', '2019-05-28', '11'),
            ('returned', '2019-05-28', '12'),
            ('returned', '2019-05-29', '13'),
            ('returned', '2019-05-30', '14'),
            ('returned', '2019-05-30', '15'),
            ('returned', '2019-05-31', '16')]

        sql_update_query = """UPDATE BookBorrowed SET Status = %s, ReturnedDate = %s WHERE BookBorrowedID = %s"""
        with self.connection.cursor() as cursor:
            result = cursor.executemany(sql_update_query, bookReturnd)
            self.connection.commit()

            print(cursor.rowcount, "Book Update records updated successfully")


    
    
    def populateUser(self):
        user_to_insert = [
            ('erelf', 'elijah@relf.com'),
            ('bjudde', 'brendan@judde.com'),
            ('cmoreno', 'cris@moreno.com'),
            ('lnaik', 'liriya@naik.com')]

        sql_insert_query = """INSERT INTO LmsUser (UserName, Email) VALUES (%s,%s)"""

        with self.connection.cursor() as cursor:
            result = cursor.executemany(sql_insert_query, user_to_insert)
            self.connection.commit()

            print(cursor.rowcount, 'User Records inserted sucessfully')
    
    def listBook(self):
        select_all_books_table = PrettyTable()
        select_all_books_table = ['BookID', 'Title', 'Author', 'Published Date']
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM  Book")
            select_all_books_table = from_db_cursor(cursor)
            print(select_all_books_table)
            return cursor.fetchall()

    
    def listUsers(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM LmsUser")
            return cursor.fetchall()

    def listBB(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM BookBorrowed")
            return cursor.fetchall()

