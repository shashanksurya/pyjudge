from app import app
from flask import Flask
from flask import session
from flask import request
import subprocess
import os
from users_passwords import USERS_PASSWORDS
import time
from flask import render_template
from app import database as data

# remove before production
app.config.update(dict(DEBUG=True))
app.secret_key = 'pyNE#tKRA5?zffuL#b7M-yX7hMrsHY-'#changed
'''
#<<<<<<< local
# populates page with stats from all users, 
# temporary until data is moved to template
@app.route('/admin')
def stats():
    html = "<table><tr><td>Problem</td><td>User</td><td>Contest</td><td>Exec</td><td>Success</td></tr>"
    for row in data.query_db('select * from contestant'):
        html += "<tr><td>%d</td><td>%s</td><td>%d</td><td>%d</td><td>%d</td></tr>" % (row['x'], row['username'], row['name'], row['password'], row['admin'])
    return html

#http://127.0.0.1:5000/user/$pyclass_username/password/$pyclass_password/upload/$1
@app.route('/adminx', methods=('GET', 'POST'))
def adminx():
	user=''
	password=''
	chkpass=[]
	if request.method == 'POST':
		print(request.form) # debug line, see data printed below
		user=request.form['uname']
		password=request.form['password']
		query="select pass from logins where uname='"+user+"'"
		print(query)
		chkpass=data.query_db(query)
		if password==str(chkpass[0][0]):
			session['user']=user
			return render_template("controls.html",admin=user)
		else:
			return "Bad user name and password supplied"+str(chkpass[0][0])+"is "+password
        #user = User.get(request.form['your_name'])
        #if user and request.form['password'] == user._password:
         #   login_user(user, remember=True)  # change remember as preference
          #  return redirect('/home/')
	else:
		return 'GET on login not supported'
#=======
#>>>>>>> other
'''
def maintain_logs(user, prob_no, msg):
    '''This method is for maintaining logs'''
    log_fp = open("server_side/user_logs/" + user, "a")
    to_write = "\t".join([str(prob_no), time.strftime("%c"), msg])
    log_fp.write(to_write + "\n")
    data.add_db(user, prob_no, msg)

def verify_username_password(username, password):
    try:
        if USERS_PASSWORDS[username] == password:
            return 1    # "Verified user. Welcome!!"
        else:
            return 0    # "Wrong password!"
    except:
        return -1       # "User doesn't exist!"

#http://127.0.0.1:5000/user/$pyclass_username/password/$pyclass_password/upload/$1
@app.route('/user/<username>/password/<password>/upload/<int:prob_no>',
           methods=['GET', 'POST'])
def upload_file(username, password, prob_no):
    '''command prompt submission mechanism'''
    if verify_username_password(username, password) > 0:
        if request.method == 'POST':
            f = request.files['file']
            submitted = username + "_" + str(prob_no) + "_submission.py"
            f.save(submitted)
            no_of_tests = 0
            for i in range(10):
                input_file = str(prob_no) + "/" + "input_" + str(i) + ".dat"
                output_file = str(prob_no) + "/" + "output_" + str(i) + ".txt"
                temp_file = str(prob_no) + "/" + username + ".txt"
                cmd = "python " + submitted + " < " +\
                      input_file + " > " + temp_file

                #print(os.path.isfile(input_file))
                #check if file exists
                if os.path.isfile(input_file):
                    no_of_tests += 1
                    status, output = subprocess.getstatusoutput(cmd)
                    if status != 0:
                        maintain_logs(username, prob_no, "Error during execution")
                        return "*" * 40 +\
                               "\nError encountered while executing code\n" +\
                               "*" * 40 + "\n"
                    diff_cmd = " ".join(["diff", temp_file, output_file])
                    status, output = subprocess.getstatusoutput(diff_cmd)

                    if len(output) > 2:
                        print(output)
                        maintain_logs(username, prob_no, "Incorrect implementation")
                        return "Incorrect output\n"

            if no_of_tests < 1:
                maintain_logs(username, prob_no, "Program not tested")
                msg = "Failure!\nProgram could not be tested.\n"
            else:
                maintain_logs(username, prob_no, "$$pass$$")
                msg = "Correct!!\nPassed " + str(no_of_tests) + " tests\n"

            return msg
        else:
            return '''
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form action="" method=post enctype=multipart/form-data>
            <p><input type=file name=file>
            <input type=submit value=Upload>
            </form>
            '''
    else:
        return "User doesn't exist!"


if __name__ == '__main__':
    #app.run()
    #pass
    app.run()
