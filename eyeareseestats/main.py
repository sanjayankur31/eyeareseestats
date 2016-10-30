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
from parsers.irssi import action, chat, notification
import parsers.common as util
import sys


def parsefilelist(filelist):
    """Parse list of log files."""
    for logfile in filelist:
        parselogfile(logfile)


def parselogfile(filename):
    """Parse a log file."""
    nick_activity = {}
    topics = []
    joins = {}
    quits = {}
    nicks = []
    speaks = {}
    mentions = {}
    activity_list = {}
    links = {}
    linetype = ''

    with open(filename, 'r') as logs:
        for line in logs:
            try:
                result = action.parseString(line)
                linetype = 'action'
            except pp.ParseException as x:
                pass
            try:
                result = chat.parseString(line)
                linetype = 'chat'
            except pp.ParseException as x:
                pass
            try:
                result = notification.parseString(line)
                linetype = 'notification'
            except pp.ParseException as x:
                pass

            if linetype == '':
                print("Malformed line encountered. Skipping.", file=sys.stderr)
                print("{}".format(line), file=sys.stderr)
                continue

            # print(result)
            time = result.time
            hour = time.split(':')[0]

            if hour in activity_list:
                activity_list[hour] += 1
            else:
                activity_list[hour] = 1

            thisnick = result.nick
            nick_known = False
            for nickset in nicks:
                if nickset and thisnick in nickset:
                    nick_known = True
            if not nick_known:
                nicks.append([thisnick])

            # store activity count per nick
            if thisnick in nick_activity:
                nick_activity[thisnick] += 1
            else:
                nick_activity[thisnick] = 1

            if linetype == 'notification':
                detail = result.detail
                if 'has quit' in detail or 'has left' in detail:
                    if thisnick in quits:
                        quits[thisnick] += 1
                    else:
                        quits[thisnick] = 1
                if 'has joined' in detail:
                    if thisnick in joins:
                        joins[thisnick] += 1
                    else:
                        joins[thisnick] = 1

                # handle renames
                newknown = False
                if 'is now known as' in detail:
                    newnick = util.getnewnick(detail)
                    for nickset in nicks:
                        if nickset:
                            # get the set current nick belongs to
                            if thisnick in nickset:
                                knownset1 = nickset

                            if newnick in nickset:
                                newknown = True
                                knownset2 = nickset

                    # it they're both known, merge the two sets
                    if newknown and knownset1 != knownset2:
                        newset = list(set(knownset1 + knownset2))
                        nicks.remove(knownset1)
                        nicks.remove(knownset2)
                        nicks.append(newset)
                    else:
                        newset = list(set(knownset1 + [newnick]))
                        nicks.remove(knownset1)
                        nicks.append(newset)

            if linetype == 'chat':
                if thisnick in speaks:
                    speaks[thisnick] += 1
                else:
                    speaks[thisnick] = 1

        # print(sorted(nick_activity.items(), key=operator.itemgetter(1)))
        # print()
        # print(sorted(activity_list.items(), key=operator.itemgetter(0)))
        # print()
        # print(sorted(quits.items(), key=operator.itemgetter(1)))
        # print()
        # print(sorted(joins.items(), key=operator.itemgetter(1)))
        # print()
        print(nicks)
        # print()
        # print(sorted(speaks.items(), key=operator.itemgetter(1)))

if __name__ == "__main__":
    parsefilelist(['test/#fedora.10-29.log'])
