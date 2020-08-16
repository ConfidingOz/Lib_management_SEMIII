import db_manager


def menu():
	valid_selections = {1,2,3,4,5,6}
	input('This is Library management tool. Press ENTER to continue')

	menu_selection = True
	while menu_selection:
		print('''
			1. Add Book
			2. Check availiblity.
			3.
			''')
		selection = input('Please Enter the number corresponding to the action.\nOr if you want to exit type EXIT.')

		if selection == 'exit' or selection == 'EXIT':
			########SOME SAVE FUNCTION########
			exit()

		elif selection in valid_functions:
			menu_selection = break

	return selection


def run():
	



