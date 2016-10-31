#!/usr/bin/env python3
"""
Print reports, generate graphs.

File: reports.py

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


import sys
import operator
from metrics import actionlist, joinlist, quitlist, urllist, mentionlist
from metrics import activitylist, timelist, dialoguelist, nicklist


def escapeforrst(item):
    """Escape special rst characters."""
    specialchars = ['*', '`', '_']
    for char in specialchars:
        item = item.replace(char, '\\' + char)

    return item


def printrstlist(dictionary):
    """Print a RST list from a dictionary."""


def reportall2rst(output=sys.stdout):
    """Dump everything to an rst file."""
    print("All collected metrics", file=output)
    print("=====================", file=output)
    print(file=output)

    print("Activity in ascending order", file=output)
    print("---------------------------", file=output)
    print(file=output)
    for nick, frequency in sorted(activitylist.items(),
                                  key=operator.itemgetter(1)):
        print("#. {}: {}".format(escapeforrst(nick), frequency), file=output)
    print(file=output)

    print("Hours in order of time", file=output)
    print("----------------------", file=output)
    print(file=output)
    for hour, frequency in sorted(timelist.items(),
                                  key=operator.itemgetter(0)):
        print("- {}: {}".format(hour, frequency), file=output)
    print(file=output)

    print("Joiners in ascending order", file=output)
    print("--------------------------", file=output)
    print(file=output)
    for nick, frequency in sorted(joinlist.items(),
                                  key=operator.itemgetter(1)):
        print("#. {}: {}".format(escapeforrst(nick), frequency), file=output)
    print(file=output)

    print("Quitters in ascending order", file=output)
    print("---------------------------", file=output)
    print(file=output)
    for nick, frequency in sorted(quitlist.items(),
                                  key=operator.itemgetter(1)):
        print("#. {}: {}".format(escapeforrst(nick), frequency), file=output)
    print(file=output)

    print("Complete nicklist with aliases", file=output)
    print("------------------------------", file=output)
    print(file=output)
    for nickset in nicklist:
        print("#. {}".format(escapeforrst(', '.join(nickset))), file=output)

    print(file=output)

    print("Dialog frequency", file=output)
    print("----------------", file=output)
    print(file=output)
    for nick, dialogs in sorted(dialoguelist.items(),
                                key=operator.itemgetter(1)):
        print("#. {}: {}".format(
            escapeforrst(nick), len(dialogs)), file=output)
    print(file=output)

    print("List of mentions", file=output)
    print("----------------", file=output)
    print(file=output)
    for nick, mentions in mentionlist.items():
        print("#. {}: {}".format(
            escapeforrst(nick),
            escapeforrst(', '.join(sorted(mentions)))), file=output)
    print(file=output)

    print("List of URLs", file=output)
    print("------------", file=output)
    print(file=output)
    for nick, urls in urllist.items():
        print("#. {}: {}".format(
            escapeforrst(nick), ', '.join(urls)), file=output)


def printdebug():
    """Print debug info, for development only."""
    if debug:
        print("Activity in ascending order")
        print(sorted(activitylist.items(), key=operator.itemgetter(1)))
        print()
        print("Hours in order of time")
        print(sorted(timelist.items(), key=operator.itemgetter(0)))
        print()
        print("Joiners in ascending order")
        print(sorted(joinlist.items(), key=operator.itemgetter(1)))
        print()
        print("Quitters in ascending order")
        print(sorted(quitlist.items(), key=operator.itemgetter(1)))
        print()
        print("Complete nicklist")
        print(nicklist)
        # print()
        # print(sorted(dialoguelist.items(), key=operator.itemgetter(1)))
        print()
        print("List of mentions")
        print(mentionlist)
        print()
        print("List of URLs")
        print(urllist)
