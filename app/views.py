#This file is about the views for this application

from app import  app
from flask import render_template
from flask import Flask,redirect
from flask import request
from flask import g
from flask import redirect
from flask import flash
from flask import url_for
import commands
import time
import os
import time
import sqlite3
import hashlib
from flask import session
from app import database as data

'''supporting methods for views'''

#checks to see if logged in
def logged_in(admin,*args):
    try:
        if session['logged_in']:
            if admin==True:
                if session['admin']:
                    return args
                else:
                    return redirect('/stats')
            else:
                return args
        return redirect('/login')
    except KeyError:
        return redirect("/login")

def maintain_logs(user,msg):
    '''This method is for maintaining logs'''
    log_fp = open("server_side/user_logs/" + user, "a")
    to_write = "\t".join([time.strftime("%c"), msg])
    log_fp.write(to_write + "\n")


def get_contests():
    '''fetch the inactive contests from the database'''
    post=[]
    open_contests=[]
    for row in data.query_db('select * from contest_checker where is_started="0"'):
        open_contests.append(row['cid'])
    for row in data.query_db('select * from contest'):
        if row['cid'] in open_contests:
            temp={}
            temp['cid']=row['cid']
            temp['date']=str(row['date'])
            temp['time']=row['time']
            temp['maxusers']=row['maxusers']
            post.append(temp)
    return post

def get_opcontests():
    '''fetch the inactive contests from the database'''
    post=[]
    open_contests=[]
    for row in data.query_db('select * from contest_checker where is_started="1"'):
        open_contests.append(row['cid'])
        print(row['cid'])
    for row in data.query_db('select * from contest'):
        if row['cid'] in open_contests:
            temp={}
            temp['cid']=row['cid']
            temp['date']=str(row['date'])
            temp['time']=row['time']
            temp['maxusers']=row['maxusers']
            post.append(temp)
    return post

def get_questions(cid):
    '''fetch the questions from the database for a cid'''
    qstore=[]
    query="select * from questions where cid='"+str(cid)+"'"
    for row in data.query_db(query):
        temp={}
        temp['cid']=row['cid']
        temp['qnum']=row['qnum']
        temp['qtitle']=row['qtitle']
        temp['question']=row['question']
        temp['input']=row['input']
        temp['output']=row['output']
        qstore.append(temp)
    return qstore

def logparticipation(uname,cid, qtitle,is_success,pep8_score,pyscore,exec_time):
    '''this method is for logging the participation of the user'''
    mx=0
    for x in data.query_db("select max(attempts) from participation where contestant_id='"+uname+"' and cid='"+cid+"' and qtitle='"+qtitle+"'"):
        if x[0]:
            mx = x[0]
            break
    mx+=1
    print(mx)
    query="insert into participation values ('"+uname+"','"+cid+"','"+qtitle+"','"+is_success+"',"+str(mx)+",'"+str(pep8_score)+"','"+str(pyscore)+"','"+str(exec_time)+"'"+")"
    print(query)
    data.add_query(query)

def getstatcontent():
    '''This method is for displaying the user stats in his home page'''
    cont =[]
    query="select * from participation where contestant_id='"+session['user']+"'"
    for row in data.query_db(query):
        temp={}
        temp['cid'] = row['cid']
        temp['contestant_id'] = row['contestant_id']
        temp['qtitle'] = row['qtitle']
        if row['is_success'] == '1':
            temp['is_success'] = "CORRECT"
        else:
            temp['is_success'] = "INCORRECT"
        temp['attempts'] = row['attempts']
        cont.append(temp)
    return cont

def getresults(cid):
    '''This method is for getting the results for a contest-admin only'''
    res = []
    query = "select * from participation where cid='"+cid+"'"
    for row in data.query_db(query):
        temp={}
        temp['cid'] = row['cid']
        temp['contestant_id'] = row['contestant_id']
        temp['qtitle'] = row['qtitle']
        if row['is_success'] == '1':
            temp['is_success'] = "CORRECT"
        else:
            temp['is_success'] = "INCORRECT"
        temp['attempts'] = row['attempts']
        temp['pep8'] = row['pep8']
        temp['pylint'] = row['pylint']
        temp['exec_time'] = row['exectime']
        res.append(temp)
    return res

'''-------------------The below views are for the admin-----------------'''

# populates page with stats from all users, 
# temporary until data is moved to template
@app.route('/stats')
def stats():
    html = "<table><tr><td>Problem</td><td>User</td><td>Contest</td><td>Resp</td></tr>"
    for row in data.query_db('select * from participation'):
        html += "<tr><td>%d</td><td>%d</td><td>%d</td><td>%d</td></tr>" % (row['pid'], row['contestant_id'], row['contest_id'], row['response_id'])
    return html
    

@app.route('/admin/', methods=('GET', 'POST'))
def adminx():
    '''landing page for admin'''
    user=''
    password=''
    chkpass=[]    
    if request.method == 'POST':
        #print(request.form) # debug line, see data printed below
        user=request.form['uname']
        password=request.form['password']
        query="select pass from contestant where uname='"+user+"'"
#        salt=b'\xbf\xf8\xd4\xeb\xc7b+\xe4\xcc\xa4\xa3\x11\x88\n}\xe0'
        chkpass=data.query_db(query)
#        p_hash=hashlib.sha224(str.encode(password))
 #       p_hash.update(salt)
  #      if str(p_hash.hexdigest())==str(chkpass[0][0]):
        if (str(chkpass) == str(password)):
            session['user']=user
            maintain_logs(user, "login success!")
            return render_template("controls.html",page={},contests=get_contests())
        else:
            maintain_logs(user, "login failed!")
            return "Bad user name and password supplied"
        #user = User.get(request.form['your_name'])
        #if user and request.form['password'] == user._password:
         #   login_user(user, remember=True)  # change remember as preference
          #  return redirect('/home/')
    else:
        if (session['admin']):
            maintain_logs(session['user'],"logged in with session!")
            return render_template("controls.html",page={},contests=get_contests())
        else:
            return 'GET on login not supported'


@app.route('/admin/newcontest')
def newcontest():
    '''new contest create page'''
    return logged_in(True,render_template("newcontest.html"))

@app.route('/admin/postcontest', methods=['GET', 'POST'])
def postcontest():
    '''save the contest posted from new contest page'''
    try:
        if not session['admin']:
            return redirect("/login")
        else:
            cname=str(request.form['cname'])
            fdate=str(request.form['date'])
            fdate=fdate.replace("/","-")
            fhour=str(request.form['hours'])
            fmin=str(request.form['min'])
            userlimit=str(request.form['maxusers'])
            query="insert into contest values ('"+cname[0:2]+fdate+fhour+fmin+"','"+fdate+"','"+fhour+fmin+"',"+userlimit+")"
            data.add_query(query)
            query="insert into contest_checker values('"+cname[0:2]+fdate+fhour+fmin+"','"+"0')"
            data.add_query(query)
            page={'content':'Contest posted sucessfully!'}
            #DEBUG:page["content"]=query
            return render_template("controls.html",page=page,contests=get_contests())
    except KeyError:
        return redirect("/login")

@app.route('/admin/question', methods=['GET', 'POST'])
def question():
    '''new page for posting questions to a contest'''
    try:
        if not session['admin']:
            return redirect("/login")
        else:
            return render_template("newquestion.html")
    except KeyError:
        return redirect("/login")

@app.route('/admin/newquestion', methods=['GET', 'POST'])
def newquestion():
    '''save the questions posted from question page'''
    return logged_in(True,render_template("newquestion.html",contests=get_contests()))
    '''
    try:
        if session['user']!="admin":
            return redirect("/login")
        else:
            return render_template("newquestion.html",contests=get_contests())
    except KeyError:
        return redirect("/login")
    '''

@app.route('/admin/newquestion/contest_load/<contest_id>',methods=['GET'])
def contest_load(contest_id):
    '''supporting function for the AJAX on the new question page
       populates all the questions which were previously posted'''
    try:
        if not session['admin']:
            return redirect("/login")
        else:
            qstore=get_questions(contest_id)
            html_send="<table><tr><td>Q.No</td><td>Title</td><td>Input</td><td>Output</td></tr>"
            for question in qstore:
                html_send += "<tr><td>"+str(question['qnum'])+"</td>"
                html_send += "<td>"+str(question['qtitle'])+"</td>"
                html_send += "<td>"+str(question['input'])+"</td>"
                html_send += "<td>"+str(question['output'])+"</td></tr>"
            html_send += "</table>"
            return html_send
    except KeyError:
        return redirect("/login")

@app.route('/admin/postquestion', methods=['GET', 'POST'])
def postquestion():
    '''save the questions posted from question page'''
    try:
        if not session['admin']:
            return redirect("/login")
        else:
            cid=str(request.form['contestids'])
            qnum=str(request.form['qnum'])
            qtitle=str(request.form['qtitle'])
            question=str(request.form['question'])
            qinput=str(request.form['input'])
            qoutput=str(request.form['output'])
            db=data.get_db()
            db.execute("insert into questions values(?,?,?,?,?,?)",(cid,qnum,qtitle,question,qinput,qoutput))
            db.commit()
            return redirect("/admin/newquestion")
    except KeyError:
        return redirect("login")

@app.route('/admin/viewcontest/contest_results/<cid>')
def contest_results(cid):
    '''supporting function for the AJAX on the view results page
       populates all the results for a selected contest'''
    html_send = "<table><tr><td>User ID</td><td>Question</td><td>Result</td><td>Total Attempts</td><td>Pep8</td><td>Pylint</td><td>Exec. Time</td></tr>"
    for result in getresults(cid):
        #html_send += "<tr><td>"+result['cid'] + "</td>"
        html_send += "<tr><td>"+result['contestant_id'] + "</td>"
        html_send += "<td>"+result['qtitle'] + "</td>"
        html_send += "<td>"+result['is_success'] + "</td>"
        html_send += "<td>"+str(result['attempts']) + "</td>"
        html_send += "<td>"+result['pep8'] + "</td>"
        html_send += "<td>"+result['pylint'] + "</td>"
        html_send += "<td>"+result['exec_time'] + "</td></tr>"
    return html_send



@app.route('/admin/viewcontest')
def viewcontest():
    '''page for viewing the results of the contest'''
    return logged_in(True,render_template("contest_view.html",page={'content':''},contests=get_opcontests()))
    '''
    try:
        if not session['admin']:
            return redirect("/login")
        else:
            return render_template("controls.html",page={'content':''},contests=get_contests())
    except KeyError:
        return redirect("/login")
    '''

@app.route('/admin/start')
def stcontest():
    '''page for starting the contest'''
    return logged_in(True,render_template("stcontest.html",contests=get_contests()))

@app.route('/admin/postcontest/<cid>',methods=['GET'])
def setcontest(cid):
    '''for setting the contest starter in the db'''
    query = 'update contest_checker set is_started="1" where cid="'+cid+'"'
    print(query)
    data.add_query(query)
    return "Contest started sucessfully!"

@app.route('/admin/logout')
def logout():
    '''logout for all the users'''
    session.clear()
    return redirect("/login")

'''-------------------The below views are for the user-----------------'''

@app.route('/user/stats')
def userstats():
    '''page for displaying the contest stats for a given contest and user'''
    return render_template("userstats.html",content=getstatcontent())

@app.route('/user/arena/timeout/<cid>',methods=['GET'])
def user_timeout(cid):
    '''set the timer bit on db to stop further submissions'''
    query = 'insert into timer_check values("'+cid+'","'+session['user']+'","1")'
    print(query)
    data.add_query(query)
    return "1"


@app.route('/user/arena/<qtitle>/<cid>',methods=['GET'])
def question_load(cid,qtitle):
    '''supporting function for the AJAX on the user contest page
       populates all the results for a selected question title'''
    return_html = ''
    qu = 'select * from questions where cid="'+cid+'" and qtitle="'+qtitle+'"'
    #print(qu)
    for row in data.query_db(qu):
        return_html += '</br><b>Problem Statement</b></br><br>'+row['question']
        return_html += '</br><b>Input</b></br><br>'+ row['input']
        return_html += '</br><b>Output</b></br><br>'+row['output']
    #print(return_html)
    return return_html

@app.route('/user/arena/verify',methods=['POST'])
def verfiy_prog():
    '''All the logic goes here for checking a users solution,
       against the values in the db. Powered by AJAX in the other side!'''
    '''Modify with care, currently supports single line input and output'''
    #data.get_db().execute('insert into registration values (?,?)',(request.form['contestids'],session['id']))
    qu_check='select is_expired from timer_check where cid="'+str(request.form['cid'])+'" and uname="'+str(session['user'])+'"'
    #print(qu_check)
    for row in data.query_db(qu_check):
        if row['is_expired'] == "1":
            return "Time's UP or the contest is not running now!"
        break
    program = os.getcwd()+"/temp_progs/temp"+str(session['user'])+str(request.form['cid'])+".py"
    input_proc=[]
    output_proc=[]
    exec_time = 0
    cid = request.form['cid']
    qtitle= request.form['titles']
    testcount = 0
    if request.form['sub_choice']=="form":
        fwrite = open(program,"w")
        fwrite.write(request.form['ta'])
        fwrite.close()
    elif request.form['sub_choice']=="upload":
        f = request.files['datafile']
        f.save(program)
        #prinpath+(request..filename)
    else:
        return "bad input!"
    qu= 'select * from questions where cid="'+cid+'" and qtitle="'+qtitle+'"'
    print(qu)
    for row in data.query_db(qu):
        #print(row['input'])
        #print(row['output'])
        input_proc = row['input'].split('\n')
        output_proc = row['output'].split('\n')
        #print(input_proc)
        #print(output_proc)
    for each_input in range(len(input_proc)):
        path = os.getcwd()+"/temp_progs/"
        fin = open(path+"fin.dat","w")
        fout = open(path+"fout.txt","w")
        fusr = open(path+"fusr.txt","w")
        fin.write(input_proc[each_input].strip())
        fout.write(output_proc[each_input].strip())
        fin.close()
        fout.close()
        fusr.close()
        cmd = "python3.4 " + program + " < " +\
                      path+"fin.dat" + " > " + path+"fusr.txt"
        #print(cmd)
        if os.path.isfile(path+"fin.dat"):
            testcount+=1
            sttime = time.time()
            status,output = commands.getstatusoutput(cmd)
            exec_time += time.time()-sttime
            #print(cmd)
            #print(output)
            if status!=0:
                return "Failed execution!"
            diff_cmd = " ".join(["diff -u --ignore-all-space", path+"fusr.txt", path+"fout.txt"])
            #print(diff_cmd)
            status, output = commands.getstatusoutput(diff_cmd)
            #print(output)
        if len(output) > 2:
            logparticipation(session['user'],cid,qtitle,"0","0","0","0")
            return "Incorrect Output"

    if testcount < 1:
        logparticipation(session['user'],cid,qtitle,"0","0","0","0")
        return "Didn't pass few tests"
    else:
        
        #test pep8 compliance
        try:
            pep_cmd  = "pep8 --count "+program+" |tail -0"
            status,pep8 = commands.getstatusoutput(pep_cmd)
            #print(pep8)
            pylin_cmd = "pylint "+program
            status,pylint = commands.getstatusoutput(pylin_cmd)
            length = pylint.find("rated at")
            pyscore = pylint[length+8:length+13]
            print(exec_time)
            logparticipation(session['user'],cid,qtitle,"1",pep8,pyscore,exec_time)
            return "Passed all the tests"+"\nPep8 Score:"+pep8+"\nPylint Score:"+pyscore+"\nExec Time: "+str(exec_time)
        except commands.CalledProcessError, e:
            pep8 =1
            pyscore =1
            logparticipation(session['user'],cid,qtitle,"1",pep8,pyscore,exec_time)
            return "Passed all the tests"+"\nPep8 Score:"+pep8+"\nPylint Score:"+pyscore+"\nExec Time: "+str(exec_time)

@app.route('/user/arena', methods=['GET','POST'])
def arena():
    '''not in use anymore, need to confirm to delete'''
    if request.method == 'POST':
        qnum = request.form['qnum']
        submit(session['id'], session['cid'], qnum)
        # contest start sets session['cid']=int
        # contest ends sets session['cid']=0
    return render_template("arena.html")

@app.route('/user/contest')
def contest():
    '''contest landing page for the user'''
    return logged_in(False,render_template("problem.html",contests=get_opcontests()))

@app.route('/user/test', methods=['GET', 'POST'])
def test():
    '''based on list of started contests, this page will show the interface for problem submission'''
    if request.method == 'POST':
        cid = request.form['contestids']
        qstore=get_questions(cid)
        print(type(qstore))
        return render_template("test.html",questions=qstore)

@app.route('/user/register', methods=['GET','POST']) #NEEDS TO BE WORKED AROUND
def register_contest():
    '''registration page for a contest open for registered users'''
    if request.method == 'POST':
#       print "contest: %d, user: %d" % (int(request.form['contestids']), session['id'])
        data.get_db().execute('insert into registration values (?,?)',(request.form['contestids'],session['id']))
    return logged_in(False,render_template("regcontest.html",contests=get_contests()))

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''login page for all the users'''
    error = None
    if request.method == 'POST':
        for name in data.query_db('select * from contestant'):
            if request.form['username'] == name['uname']:
                if request.form['password'] == name['pass']:
                    session['logged_in'] = True
                    session['user'] = name['uname']
                    session['id'] = name['x']
                    session['admin'] = name['admin']
                    if session['admin']:
                        return render_template("controls.html",page={},contests=get_contests())
                    else:
                        return redirect(url_for('contest'))
                else:
                    error = 'Invalid password'
            else:
                error = 'Invalid username'
    return render_template("login.html", error=error)

@app.route('/register', methods=['GET', 'POST']) 
def register():
    '''registration page for logging into system for non-admin users'''
    error = None
    if request.method == 'POST':
        list_username=[]
        list_cname=[]
        for name in data.query_db('select * from contestant'):
                list_username.append(name['uname'])
                list_cname.append(name['contestant_name'])
        if request.form['username'] in list_username:
                error = 'Username already in use'
        elif request.form['name'] in list_cname:
                error = 'User already exists'
        else:
            data.add_user(request.form['name'], request.form['username'], request.form['password'], 0)
            error = 'New user created!'                
    #return logged_in(False,render_template("register.html",error=error))
    return render_template("register.html", error=error)

