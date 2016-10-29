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
import sys


def parsefilelist(filelist):
    """Parse list of log files."""
    for logfile in filelist:
        parselogfile(logfile)


def parselogfile(filename):
    """Parse a log file."""
    all_nicks = {}
    topics = []
    joins = {}
    quits = {}
    renicks = {}
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

            nick = result.nick
            # store nicks
            if nick in all_nicks:
                all_nicks[nick] += 1
            else:
                all_nicks[nick] = 1

            if linetype == 'notification':
                detail = result.detail
                if 'has quit' in detail or 'has left' in detail:
                    if nick in quits:
                        quits[nick] += 1
                    else:
                        quits[nick] = 1
                if 'has joined' in detail:
                    if nick in joins:
                        joins[nick] += 1
                    else:
                        joins[nick] = 1
                if 'is now known as' in detail:
                    if nick in renicks:
                        renicks[nick] += 1
                    else:
                        renicks[nick] = 1

            if linetype == 'chat':
                if nick in speaks:
                    speaks[nick] += 1
                else:
                    speaks[nick] = 1


        print(sorted(all_nicks.items(), key=operator.itemgetter(1)))
        print()
        print(sorted(activity_list.items(), key=operator.itemgetter(0)))
        print()
        print(sorted(quits.items(), key=operator.itemgetter(1)))
        print()
        print(sorted(joins.items(), key=operator.itemgetter(1)))
        print()
        print(sorted(renicks.items(), key=operator.itemgetter(1)))
        print()
        print(sorted(speaks.items(), key=operator.itemgetter(1)))

if __name__ == "__main__":
    parsefilelist(['test/#fedora.10-29.log'])
