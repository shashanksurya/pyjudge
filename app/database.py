# This file contains the methods that maintain the database. 

import sqlite3
from app import app
from flask import g

def connect_db():
    '''# Database connection and querying'''
    # connects to the specific database
    rv = sqlite3.connect('pyjudge.db')
    rv.row_factory = sqlite3.Row
    return rv

@app.teardown_appcontext
def close_db(error):
    '''# closes the database at the end of the request'''
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def query_db(query, args=(), one=False):
    '''# will allow you to grab one piece of data from the database at a time'''
    cursor = get_db().execute(query, args)
    rv = cursor.fetchall()
    cursor.close()
    return (rv[0] if rv else None) if one else rv

def get_db():
    '''# returns the db connection'''
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def add_query(query, args=None):
    '''#execute insert queries'''
    db = get_db()
    if args:
        db.execute(query, args) # figured out what args was for
    else:
        db.execute(query) 
    db.commit()

def add_user(name, uname, pwd, admin):
    '''for DML queries'''
    db = get_db()
    mx=0
    for x in query_db("select max(x) from contestant"):
        mx = x[0]
        break
    db.execute('insert into contestant (x,contestant_name, uname, pass, admin) values (?,?, ?, ?, ?)', [mx+1,name, uname, pwd, admin])
    db.commit()


def add_db(user, prob_no, msg):
    '''# used in maintain logs to push data to db'''
    succ = 2
    if msg is "$$pass$$":
        succ = 1
    else:
        succ = 0
    db = get_db()
    db.execute('insert into participation (prob_id, user, contest_id, execution, success) values (?, ?, ?, ?, ?)',[prob_no,user,1,1,succ])
    db.commit()