#!/usr/bin/env python3
"""
Main log parsers live here.

File: logparser.py

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
from parsers.irssi import action, chatline, notification
from parsers.common import ppurl, getnewnick, findmentionednicks
from metrics import actionlist, joinlist, quitlist, urllist, mentionlist
from metrics import activitylist, timelist, dialoguelist, nicklist
from metrics import debug
from reports import reportall2rst, printdebug, reportsummary2rst
import sys
from os import listdir
from os.path import isfile, join
import re


def parsefilelistindirfromprefix(dirpath, prefix):
    """Parse a list of files when a directory is given."""
    directorylist = listdir(dirpath)
    prefixregex = re.compile(re.escape(prefix))
    filelist = []
    for entry in directorylist:
        # you can have multiple slashes, it doesn't make a difference
        fullentry = join(dirpath + '/' + entry)
        if isfile(fullentry):
            if (prefixregex.match(entry)):
                filelist.append(fullentry)

    parselogfiles(filelist)


def parsefilelistfromprefix(prefix):
    """Parse a list of files obtained using a prefix."""
    parsefilelistindirfromprefix('./', prefix)


def parselogfiles(filelist):
    """Parse a list of files.

    This is the main worker function.

    Note: please check beforehand that the list is valid.
    """
    linetype = ''
    for filename in filelist:
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
                        newnick = getnewnick(detail)
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

                # things common for chats and actions
                else:
                    mentionednicks = findmentionednicks(thisnick, detail)
                    if len(mentionednicks) > 0:
                        if thisnick in mentionlist:
                            newmentionlist = (mentionlist[thisnick]
                                              + mentionednicks)
                            mentionlist[thisnick] = newmentionlist
                        else:
                            mentionlist[thisnick] = mentionednicks

                    listoflinks = []
                    for linkintext, start, finish in ppurl.scanString(detail):
                        listoflinks.append(linkintext.url)
                    if len(listoflinks) > 0:
                        if thisnick in urllist:
                            newlist = urllist[thisnick] + listoflinks
                            urllist[thisnick] = newlist
                        else:
                            urllist[thisnick] = listoflinks

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

    # printdebug()
    with open('output-summary.rst', 'w') as output:
        reportsummary2rst(output)
    with open('output-detailed.rst', 'w') as output:
        reportall2rst(output)

if __name__ == "__main__":
    # parselogfiles(['test/#fedora.10-29.log'])
    parsefilelistindirfromprefix('/home/asinha/dump/fedora-join-stats/201610/', '#fedora-join.')
