# populate.py will populate my db
import sqlite3
import sys

connection = None

try:

	connection = sqlite3.connect('pyjudge.db')
	cursor = connection.cursor()
	print "bullshit"
	'''	
	cursor.execute("INSERT INTO contestant VALUES(1, 'Malik Butler', 'mb11r', '123', 0)")
	print "not a primary key, but ok"
	cursor.execute("INSERT INTO contestant VALUES(2, 'Jordan', 'jobi1', '123', 1)")
	print "what the fuck?? so zero is unique but 2 isn't?"
	cursor.execute("INSERT INTO contestant VALUES(3, 'Joe', 'jd12', '123', 1)")
	cursor.execute("INSERT INTO contestant VALUES(4, 'Patrick', 'pad1', '123', 1)")
	print "fuck contestant"
	cursor.execute("INSERT INTO contest VALUES(1, '2014-11-07', '09:00', 100)")
	print "fuck contest"
	cursor.execute("INSERT INTO response VALUES(1, 1, 5, 0, 0, 0)")
	cursor.execute("INSERT INTO response VALUES(2, 1, 10, 0, 0, 0)")
	cursor.execute("INSERT INTO response VALUES(3, 1, 5, 0, 0, 0)")
	cursor.execute("INSERT INTO response VALUES(4, 2, 100, 0, 0, 0)")
	cursor.execute("INSERT INTO response VALUES(5, 2, 10, 0, 0, 0)")
	cursor.execute("INSERT INTO response VALUES(6, 2, 10, 0, 0, 0)")
	cursor.execute("INSERT INTO response VALUES(7, 3, 1, 0, 0, 0)")
	cursor.execute("INSERT INTO response VALUES(8, 3, 100, 0, 0, 0)")
	cursor.execute("INSERT INTO response VALUES(9, 3, 50, 0, 0, 0)")
	print "fuck response"
	cursor.execute("INSERT INTO participation VALUES(1, 1, 1, 1)")
	cursor.execute("INSERT INTO participation VALUES(2, 2, 1, 2)")
	cursor.execute("INSERT INTO participation VALUES(3, 3, 1, 3)")
	cursor.execute("INSERT INTO participation VALUES(4, 1, 1, 4)")
	cursor.execute("INSERT INTO participation VALUES(5, 2, 1, 5)")
	cursor.execute("INSERT INTO participation VALUES(6, 3, 1, 6)")
	cursor.execute("INSERT INTO participation VALUES(7, 1, 1, 7)")
	cursor.execute("INSERT INTO participation VALUES(8, 2, 1, 8)")
	cursor.execute("INSERT INTO participation VALUES(9, 3, 1, 9)")
	print "these are also different!"
	connection.commit()
	'''
	cursor.execute("SELECT * from contestant")
	rows = cursor.fetchall()
	for row in rows:
		print row
	
	cursor.execute("SELECT * from contest")
	rows = cursor.fetchall()
	for row in rows:
		print row

	cursor.execute("SELECT * from registration")
	rows = cursor.fetchall()
	for row in rows:
		print row


except sqlite3.Error, e:
	print "Error: %s." % e.args[0]
	sys.exit(1)

finally:
	if connection:
		connection.close()