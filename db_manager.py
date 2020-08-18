import sqlite3
from sqlite3 import Error
import datetime
from settings import lease_days


class Database(object):
    def __init__(self, fileN):
        self.file = fileN
        self.est_conn()
        self.db_check()
        self.c.execute('''PRAGMA foreign_keys = 1''')
        
    def est_conn(self):
        self.conn = None
        try:
            self.conn = sqlite3.connect(self.file)
            self.c = self.conn.cursor()
        except Error as e:
            print(e)

    def close_conn(self):
        if self.conn:
            self.conn.commit()
            self.c.close()
            self.conn.close()

    def executor(self, query, values=None):
        if values:
            if values is tuple:
                self.c.execute(query, values)
            else:
                print(f'The argument "value" should be a tuple, it is {values}')
        else:
            self.c.execute(query)
        self.conn.commit()

    def db_check(self):
        student_table = '''
            CREATE TABLE IF NOT EXISTS Students (
            Reg_No TEXT PRIMARY KEY,
            Name TEXT NOT NULL,
            Phone INTEGER NOT NULL,
            Email TEXT)
            '''
        self.executor(student_table)

        book_table = '''
            CREATE TABLE IF NOT EXISTS Books (
            Book_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Author TEXT,
            Quantity INTEGER NOT NULL)
            '''
        self.executor(book_table)

        relation_table = '''
            CREATE TABLE IF NOT EXISTS Borrowed_Books (
            Student_reg TEXT NOT NULL,
            Book_id INTEGER NOT NULL,
            Book_name TEXT NOT NULL,
            Borrow_date TIMESTAMP NOT NULL,
            Return_date TIMESTAMP NOT NULL,
            Days_to_return INTEGER,
            FOREIGN KEY (Student_reg) REFERENCES Students(Reg_No),
            FOREIGN KEY (Book_id) REFERENCES Books(Book_ID) ON DELETE CASCADE,
            PRIMARY KEY (Student_reg, Book_id))
        '''
        self.executor(relation_table)

    def add_student(self, SName, Reg_No, Phone, Email):
        query = '''
            INSERT INTO Students(Reg_No, Name, Phone, Email)
            VALUES(?,?,?,?)'''
        self.executor(query, (Reg_No, SName, Phone, Email,))

    def add_book(self, BName, Q=1, Author=None):
        query = '''
        INSERT INTO Books(Name, Author, Quantity) VALUES(?, ?, ?)
        '''
        self.executor(query, (BName, Author, Q,))

    def remove_student(self, Reg):  ####Do not cascade delete the records###
        try:
            query = '''
            DELETE FROM Students WHERE Reg_No=?
            '''
            self.executor(query, (Reg,))
        except Error as e:
            query = '''
            SELECT Book_name FROM Borrowed_Books WHERE Student_reg = ?
            '''
            self.executor(query, (Reg,))
            owed = []
            for i in self.c.fetchall():
                owed.append(i[0])
            print(f"Cannot remove student! The books owed are: {owed}")
            print(f'The error was: {e}')

    def remove_book(self, Name): ####Cascade delete the borrowed record check###
        try:
            query = '''
            DELETE FROM Books WHERE Name=?
            '''
            self.executor(query, (Name,))
        except Error as e:
            print(e)

    def borrow_book(self, Student_Name, Reg_No, Book_ID, today=datetime.date.today(), days=lease_days):
        query = 'SELECT Quantity, Name FROM Books where Book_id = ?'
        self.executor(query, (Book_ID,))
        Total, BName = self.c.fetchall()[0]
        self.executor('SELECT * FROM Borrowed_Books WHERE Book_id = ?', (Book_ID,))
        borrowed = len(self.c.fetchall())
        if Total - borrowed > 0:
            return_date = today + datetime.timedelta(days=days)
            values = (Reg_No, Book_Name, today, return_date,)
            query = '''
            INSERT INTO Borrowed_Books(Student_reg, Book_id, Book_name, Borrow_date, Return_date)
            VALUES(?, ?, ?, ?)
            '''
            self.executor(query, (values,))
        else:
            print("Book not available")

    def return_book(self, Reg, Book_id):
        try:
            query = '''DELETE FROM Borrowed_Books WHERE Student_reg = ? AND Book_id = ?'''
            self.executor(query, (Reg, Book_id,))
        except Error as e:
            print(f'The book id or the reg number is wrong!')
            print(e)

    def check_book(self, BName):
        query = '''
        SELECT Name FROM Books WHERE Name LIKE "%"||?||"%"
        '''
        self.executor(query, (BName,))
        return self.c.fetchall()

    def check_student(self, Name=None, Reg=None):
        query = '''
        SELECT Name, Reg_No FROM Students WHERE Name LIKE "%"||?||"%" OR Reg_No LIKE "%"||?||"%"
        '''
        self.executor(query, (Name, Reg,))
        return self.c.fetchall()
        

    def check_leases(self):
        today = datetime.date.today()
        query = '''SELECT Student_reg, Book_name, Return_date FROM Borrowed_Books WHERE Return_date >= ?'''
        self.executor(query, (today))
        all_books = {}
        data = self.c.fetchall()
        for i in data:
            if i[0] not in all_books:
                all_books[i[0]] = list()
            all_books[i[0]].append([i[1], i[2]])
        



