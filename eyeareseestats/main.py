#!/usr/bin/env python3
"""
Main function file.

File: main.py

Copyright 2016 Ankur Sinha
Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


import operator
import pyparsing as pp
import metrics
import notifications
from parsers.irssi import action, chatline, notification
import parsers.common as util
import sys


def parsefilelist(filelist):
    """Parse list of log files."""
    for logfile in filelist:
        parselogfile(logfile)


def parselogfile(filename):
    """Parse a log file."""
    activitylist = {}
    topiclist = []
    joinlist = {}
    quitlist = {}
    nicklist = []
    dialoguelist = {}
    mentionlist = {}
    actionlist = {}
    timelist = {}
    linklist = {}
    linetype = ''

    with open(filename, 'r') as logs:
        for line in logs:
            line = line.rstrip()
            linetype = 'none'
            result = None

            if linetype == 'none':
                try:
                    result = action.parseString(line)
                except pp.ParseException as x:
                    pass
                if result:
                    linetype = 'action'

            if linetype == 'none':
                try:
                    result = chatline.parseString(line)
                except pp.ParseException as x:
                    pass
                if result:
                    linetype = 'chat'

            if linetype == 'none':
                try:
                    result = notification.parseString(line)
                except pp.ParseException as x:
                    linetype = 'none'
                if result:
                    linetype = 'notification'

            if linetype == 'none':
                print("Malformed line: '{}'".format(line), file=sys.stderr)
                continue

            time = result.time
            hour = time.split(':')[0]
            detail = result.detail

            if hour in timelist:
                timelist[hour] += 1
            else:
                timelist[hour] = 1

            thisnick = result.nick
            nick_known = False
            for nicklistet in nicklist:
                if nicklistet and thisnick in nicklistet:
                    nick_known = True
            if not nick_known:
                nicklist.append([thisnick])

            # store activity count per nick
            if thisnick in activitylist:
                activitylist[thisnick] += 1
            else:
                activitylist[thisnick] = 1

            if linetype == 'notification':
                if 'has quit' in detail or 'has left' in detail:
                    if thisnick in quitlist:
                        quitlist[thisnick] += 1
                    else:
                        quitlist[thisnick] = 1
                if 'has joined' in detail:
                    if thisnick in joinlist:
                        joinlist[thisnick] += 1
                    else:
                        joinlist[thisnick] = 1

                # handle renames
                newknown = False
                if 'is now known as' in detail:
                    newnick = util.getnewnick(detail)
                    for nicklistet in nicklist:
                        if nicklistet:
                            # get the set current nick belongs to
                            if thisnick in nicklistet:
                                knownset1 = nicklistet

                            if newnick in nicklistet:
                                newknown = True
                                knownset2 = nicklistet

                    # it they're both known, merge the two sets
                    if newknown and knownset1 != knownset2:
                        newset = list(set(knownset1 + knownset2))
                        nicklist.remove(knownset1)
                        nicklist.remove(knownset2)
                        nicklist.append(newset)
                    else:
                        newset = list(set(knownset1 + [newnick]))
                        nicklist.remove(knownset1)
                        nicklist.append(newset)

            if linetype == 'chat':
                if thisnick in dialoguelist:
                    dialoguelist[thisnick].append([detail])
                else:
                    dialoguelist[thisnick] = [detail]

            if linetype == 'action':
                if thisnick in actionlist:
                    actionlist[thisnick].append([detail])
                else:
                    actionlist[thisnick] = [detail]

        # print(sorted(activitylist.items(), key=operator.itemgetter(1)))
        # print()
        # print(sorted(timelist.items(), key=operator.itemgetter(0)))
        # print()
        # print(sorted(quitlist.items(), key=operator.itemgetter(1)))
        # print()
        # print(sorted(joinlist.items(), key=operator.itemgetter(1)))
        # print()
        # print(nicklist)
        # print()
        # print(sorted(dialoguelist.items(), key=operator.itemgetter(1)))

if __name__ == "__main__":
    parsefilelist(['test/#fedora.10-29.log'])
