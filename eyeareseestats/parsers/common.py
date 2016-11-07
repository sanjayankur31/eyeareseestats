#!/usr/bin/env python3
"""
Common functions.

File: eyeareseestats/parsers/common.py

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


import pyparsing as pp
from metrics import nicklist


ppurl = pp.Regex('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+').setResultsName('url')


def getnewnick(sentence):
    """Parse detail to get new nick."""
    nick = pp.Regex('[a-zA-Z0-9\-_|^]+').setResultsName('nick')
    parser = pp.Literal('is now known as') + nick + pp.restOfLine
    try:
        result = parser.parseString(sentence)
        return result.nick
    except pp.ParseException as x:
        pass


def findmentionednicks(thisnick, detail):
    """Parse the detail to find mentioned nicks."""
    mentioned = []
    for nickset in nicklist:
        for nick in nickset:
            if nick and (nick in detail):
                mentioned.append(nick)

    return mentioned
