#!/usr/bin/python3
# coding=utf-8


"""migrate.py: migrates timetracking data from sqlite3 to mysql"""

__author__ = "Simon Gunacker"
__copyright__ = "Copyright 2016, Graz"

import MySQLdb
import sqlite3
import configparser
from time import gmtime, strftime, localtime
from os.path import expanduser

# path of sqlite3
DB_NAME = expanduser('~') + '/.timetracker/timings.db'

# get all data
con = sqlite3.connect(DB_NAME)
cur = con.cursor()
cur.execute("SELECT * FROM timings ORDER BY start")
res = cur.fetchall()
con.close()

# get mysql database connection information
config = configparser.ConfigParser()
config.read('settings.cfg')

host = config['Database']['host']
db = config['Database']['db']
user = config['Database']['user']
passwd = config['Database']['passwd']

# migrate
con = MySQLdb.connect(host, user, passwd, db)
cur = con.cursor()
for row in res:
    tag = row[0]
    start = strftime("%Y-%m-%d %H:%M:%S", localtime(float(row[1])))
    end = strftime("%Y-%m-%d %H:%M:%S", localtime(float(row[2])))
    cur.execute(
        "INSERT INTO timings(tag, start, end) VALUES(%s, %s, %s)", [tag, start, end])
con.commit()
con.close()
