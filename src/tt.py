#!/usr/bin/python3
# coding=utf-8


"""tt.py: a simple timetracking cli"""

__author__ = "Simon Gunacker"
__copyright__ = "Copyright 2016, Graz"

import cmd
import readline
import sqlite3
from os import system, makedirs
from os.path import abspath, isfile, dirname, split, expanduser
from time import time, gmtime, strftime
from threading import Timer


# configurations
# DB_NAME = split(dirname(abspath(__file__)))[0] + '/data/timings.db'
DB_NAME = expanduser('~') + '/.timetracker/timings.db'


def setup():
    makedirs(dirname(DB_NAME), mode=0o755, exist_ok=True)
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE timings(tag VARCHAR, start DATE, end DATE, delta DATE)")
    con.commit()
    con.close()


class RepeatedTimer(object):

    def __init__(self, interval, function, tag=None):
        self._timer = None
        self.interval = interval
        self.function = function
        self.tag = tag
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function("Currently working on %s" %
                      self.tag, show=self.tag is not None)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


def notify(message, show=True):
    if show:
        system("notify-send '%s'" % message)


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
        self.timer = RepeatedTimer(30 * 60, notify)

    def do_start(self, arg):
        'start timing a new activity'
        tag = arg.split(" ")
        if (len(tag) > 1):
            print("Illegal argument")
        else:
            tag = tag[0]
            self.rec = Record(tag)
            self.rec.start_time()
            self.timer.tag = tag
            notify("Currently working on %s" % tag)

    def do_stop(self, arg):
        'stop current timing activity'
        if (self.rec.start is None):
            print("No activity started")
        else:
            self.rec.end_time()
            self.rec.save(self.cur)
            notify("Done working on %s" % self.timer.tag)
            self.timer.tag = None
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
        if self.rec.start is not None and self.rec.end is None:
            self.do_stop(None)
        self.con.commit()
        self.con.close()
        self.timer.stop()
        return True

if __name__ == "__main__":
    if not isfile(DB_NAME):
        setup()
    system("clear")
    TTShell().cmdloop()
