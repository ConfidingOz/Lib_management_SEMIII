import db_manager
import sys

file = 'my_data.db'

def add_student(db):
	Name = input('Enter Student Name: ')
	Reg = input('Enter Student Reg. No.: ')
	Phone = input('Enter Student Phone: ')
	Email = input('Enter Student Email: ')
	try:
		db.add_student(Name, Reg, Phone, Email)
		print('\nStudent added!!\n')
	except:
		print('\nAdding Student failed!!\n')

def add_book(db):
	Name = input('Enter the book name: ')
	Author = input('Enter the author:')
	Q = input('Enter the quantity: ')
	try:
		db.add_book(Name, Q, Author)
		print('\nBook added!!\n')
	except:
		print('\nAdding Book failed!!\n')

def remove_student(db):
	Reg = input('Enter student Reg No.: ')
	db.remove_student(Reg)
	print('\n')

def remove_book(db):
	ID = int(input('Enter the Book ID: '))
	db.remove_book(ID)
	print('\n')

def lease_book(db):
	Reg = input('Enter the Reg No. of the student: ')
	Book_id = int(input('Enter the ID of the book to loan: '))
	db.borrow_book(Reg, Book_id)
	print('\n')

def return_book(db):
	Reg = input('Enter the student Reg No.: ')
	Book_id = int(input('Enter the book id: '))
	db.return_book(Reg, Book_id)
	print('\n')

def check_book(db):
	Name = input('Enter the book Name: ')
	db.check_book(Name)
	input()
	print('\n')

def check_student(db):
	print('If you don\'t know any one you can press Enter to skip!')
	Name = input('Enter name: ')
	Reg = input('Enter Reg No.: ')
	if not Name:
		Name = None
	if not Reg:
		Reg = None
	db.check_student(Name, Reg)
	input()
	print('\n')

def check_leases(db):
	db.check_leases()
	input()
	print('\n')

def menu(db):
	valid_selections = [1,2,3,4,5,6,7,8,9]
	input('This is Library management tool. Press ENTER to continue')
	functions = [add_book, add_student, remove_book, remove_student, lease_book, return_book, check_book, check_student, check_leases]
	while True:
		print('''1. Add Book
2. Add Student
3. Remove Book
4. Remove Student
5. Lease Book
6. Return Book
7. Check Book
8. Check Student
9. Check Lease
''')
		selection = input('Please Enter the number corresponding to the action.\nOr if you want to exit type EXIT.\n-->')
		# print(type(selection))
		if selection == 'exit' or selection == 'EXIT':
			########SOME SAVE FUNCTION########
			sys.exit(0)
		elif int(selection) in valid_selections:
			functions[int(selection)-1](db)
		else:
			print('Invalid operation\n\n')
	


def run():
	db = db_manager.Database(file)
	menu(db)

if __name__ == '__main__':
	run()
	



