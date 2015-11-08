# this script will test using a python script to run another.

import sys # for sys.argv
import subprocess # for running programs with subprocess
import time # for time.clock()

# sys.argv contains the arguments
# len(sys.argv) tells you how many arguments there are
# sys.argv[x] returns x argument
'''
if len(sys.argv) is not 3:
	# if there aren't exactly two arguments quit
	print "Correct usage: python submit.py arg1 arg2"
	sys.exit(1)
else:
	print "%d and %d" % (int(sys.argv[1]), int(sys.argv[2]))
'''

def submit(uid, cid, qnum):
	test = "pep8"
	argument1 = "--statistics"
	argument2 = "-qq"
	exec_time=0
	pylint=0


	# simply running the program 
	# subprocess.call(["python", sys.argv[1]])
	try:
		start_time = time.time()
		user_output = subprocess.check_output(["python", sys.argv[1]])
		exec_time = time.time() - start_time
		# input will be taken from database of questions 
		output=data.query_db('select input from questions where cid=? qnum=?', (input, cid, qnum))
		if user_output == "This file ran\n":
			result=0
		else:
			result=1
	except subprocess.CalledProcessError, e:
		result=1

	# testing style with pep8
	try:
		pep8=subprocess.check_output([test, sys.argv[1]])
	except subprocess.CalledProcessError, e:
		pep8=1


#	print "Execution: %d" % result
#	print "Execution time: %f" % exec_time
#	print "Style: %d" % style_result

	data.add_query('insert into response values(?,?,?,?,?,?)',(NULL, qnum, exec_time, result, pep8, pylint))
	data.add_query('insert int participation values(?,?,?,(select max(rid) from response)+1'(NULL, uid, cid))
	'''
	style_results.split('\n')
	total = 0

	for result in style_results:
		total += int(result[0])

	print total
	'''