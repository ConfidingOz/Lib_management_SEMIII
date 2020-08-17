import sqlite3
from sqlite3 import Error
import datetime
from settings import lease_days


class Database(object):
    def __init__(self, fileN):
        self.file = fileN
        self.est_conn()
        self.db_check()
        
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
            self.c.execute(query, values)
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
            Name TEXT PRIMARY KEY,
            Author TEXT,
            Quantity INTEGER NOT NULL,)
            '''
        self.executor(book_table)

        relation_table = '''
        CREATE TABLE IF NOT EXISTS Borrowed_Books (
        Student_reg TEXT NOT NULL,
        Book_name TEXT NOT NULL,
        Borrow_date TIMESTAMP NOT NULL,
        Return_date TIMESTAMP NOT NULL,
        FOREIGN KEY (Student_reg) REFERENCES Students(Reg_No)),
        FOREIGN KEY (Book) REFERENCES Books(Name)),
        PRIMARY KEY (Student_reg, Book)
        '''
        self.executor(relation_table)

    def add_student(self, SName, Reg_No, Phone, Email):
        query = '''
            INSERT INTO Students(Reg_No, Name, Phone, Email)
            VALUES(?,?,?,?)'''
        self.executor(query, (Reg_No, SName, Phone, Email))

    def add_book(self, BName, Author, Q):
        query = '''
        INSERT INTO Books(Name, Author, Quantity) VALUES(?, ?, ?)
        '''
        self.executor(query, (BName, Author, Q))

    def borrow_book(self, Student_Name, Reg_No, Book_Name):
        if self.check_availiblity(Book_Name)
            today = datetime.datetime.now()
            return_date = today + datetime.timedelta(days=lease_days)
            data = (Reg_No, Book_Name, today, return_date)
            query = '''
            INSERT INTO Borrowed_Books(Student_reg, Book_name, Borrow_date, Return_date)
            VALUES(?, ?, ?, ?)
            '''
            self.executor(query, data)

    def remove_student(self):
        pass

    def remove_book(self, Name):
        
        query = '''
        DELETE FROM Books WHERE Name=?
        '''
        self.executor(query, (id,))

    def return_book(self):
        pass

    def check_leases(self):
        pass

    def check_availiblity(self, BName):
        pass
