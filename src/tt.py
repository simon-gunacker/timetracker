#!/usr/bin/python3
import cmd
import readline
import sqlite3
from os import system, makedirs
from os.path import abspath, isfile, dirname
from time import time, gmtime, strftime

# configurations
DB_NAME = '../data/timings.db'


def setup():
    path = abspath(DB_NAME)
    makedirs(dirname(path), mode=0o755, exist_ok=True)
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE timings(tag VARCHAR, start DATE, end DATE, delta DATE)")
    con.commit()
    con.close()


class Record:

    def __init__(self, tag=None, start=None, end=None, delta=None):
        self.tag = tag
        self.start = start
        self.end = end
        self.delta = delta

    def start_time(self):
        self.start = time()

    def end_time(self):
        self.end = time()
        self.delta = self.end - self.start

    def save(self, cur):
        cur.execute("INSERT INTO timings VALUES(?, ?, ?, ?)",
                    (self.tag, self.start, self.end, self.delta))

    def __str__(self):
        timestr = strftime("%H:%M", gmtime(float(self.delta)))
        return "%-25s: %s" % (self.tag, timestr)


class TTShell(cmd.Cmd):
    intro = 'Welcome to tt shell. Type help or ? to list commands\n'
    prompt = 'tt> '

    def __init__(self, *args, **kwargs):
        super(TTShell, self).__init__(*args, **kwargs)
        self.con = sqlite3.connect(DB_NAME)
        self.con.row_factory = lambda cur, row: Record(*row)
        self.cur = self.con.cursor()
        self.rec = Record()

    def do_start(self, arg):
        'start timing a new activity'
        tag = arg.split(" ")
        if (len(tag) > 1):
            print("Illegal argument")
        else:
            self.rec = Record(tag[0])
            self.rec.start_time()

    def do_stop(self, arg):
        'stop current timing activity'
        if (self.rec.start is None):
            print("No activity started")
        else:
            self.rec.end_time()
            self.rec.save(self.cur)
            print(self.rec)

    def do_list(self, arg):
        'list all recorded timings'
        tag = "%s%%" % arg if arg is not None else "%"
        self.cur.execute(
            "SELECT tag, '1', '1', sum(delta)  FROM timings WHERE tag LIKE ? GROUP BY tag", [tag])
        for row in self.cur:
            print(row)

    def do_sync(self, arg):
        'syncs to database file to webserver using rysnc command'

    def do_exit(self, arg):
        'exit current session'
        self.con.commit()
        self.con.close()
        return True

if __name__ == "__main__":
    if not isfile(DB_NAME):
        setup()
    system("clear")
    TTShell().cmdloop()
