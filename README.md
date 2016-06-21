# timetracker
*timetracker* is a simple commandline tool fro tracking your time.

## Dependencies And Requirements
It requires `python3` and `linux`.
Furthermore, one has to have `mysql` and `mysql-config`. To install it, invoke
`sudo apt-get install python3-dev libmysqlclient-dev`. Afterwards, you can install `mysqlclient` using `sudo pip3 install mysqlclient`. Finally, you have to copy `settings.cfg.default` to `settings.cfg` and set all your db configurations

## Current State Of Development
To run timetracker, simply invoke `.src/tt.py` from your commandline. *timetracker* supports the options listed below. Note that timetracker supports autocompletion and history for all commands.

### start an activity
To start an activity, type `start <name_of_activity>`

### stop the current activity
To stop the current activity, simple type `stop`

### list current activities
To list activities type `list <pattern>`. All activities beginning with the given pattern will be listed. They are grouped by their name and their overall time is summed up. When no pattern is given, all activities will be listed.

## Things To Do

+ **sync**: use rsync to download / upload your timings.db

+ **hierachical queries**: timings should be listed hierachically, e.g. in
  addition to showing timings for *work.project1* and *work.project2*, timetracker should also show the overall time for *work*.

+ **extended code completion**: activities already known by the database should
  be included in autocompletion.
