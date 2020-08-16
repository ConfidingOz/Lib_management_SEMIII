import sqlite3
from sqlite3 import Error

db_file = 'library_data'

def est_conn():
	conn = None
	try:
		conn = sqlite3.connect(':memory:')
		c = conn.cursor()
		return (conn, c)
	except Error as e:
		print(e)

def close_conn(conn,c):
	if conn:
		conn.commit()
		c.close()
		conn.close()

def db_check():
	conn, c = est_conn()
	c.execute('CREATE TABLE IF NOT EXISTS randstuff(inix REAL, string TEXT)')

def insert_data(inix, string):
	c.execute('INSERT into randstuff (inix, string) VALUES(?, ?)', (inix, string ))

def view():
	c.execute

db_check()
insert_data()