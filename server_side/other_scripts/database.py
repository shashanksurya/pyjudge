# This file contains the methods that maintain the database. 

import sqlite3
from app import app
from flask import g

# Database connection and querying
def connect_db():
    # connects to the specific database
    rv = sqlite3.connect('pyjudge.db')
    rv.row_factory = sqlite3.Row
    return rv

# closes database upon teardown
@app.teardown_appcontext
def close_db(error):
    # closes the database at the end of the request
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# will allow you to grab one piece of data from the database at a time
def query_db(query, args=(), one=False):
    cursor = get_db().execute(query, args)
    rv = cursor.fetchall()
    cursor.close()
    return (rv[0] if rv else None) if one else rv

# returns the db connection
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

#execute insert queries
def add_query(query):
    db = get_db()
    db.execute(query,args)
    db.commit()

def add_user(name, uname, pwd, admin):
    db = get_db()
    db.execute('insert into contestant (contestant_name, uname, pass, admin) values (?, ?, ?, ?)', [name, uname, pwd, admin])
    db.commit()

# used in maintain logs to push data to db
def add_db(user, prob_no, msg):
    succ = 2
    if msg is "$$pass$$":
        succ = 1
    else:
        succ = 0
    db = get_db()
    db.execute('insert into participation (prob_id, user, contest_id, execution, success) values (?, ?, ?, ?, ?)',[prob_no,user,1,1,succ])
    db.commit()