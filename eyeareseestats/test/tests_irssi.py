#!/usr/bin/env python3
"""
Test irssi logs.

File: tests_irssi.py

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

import unittest
import pyparsing as pp
from eyeareseestats.parsers.irssi import action, notification, nick, chatline, time


class TestIRSSILogs(unittest.TestCase):

    """Test for IRSSI parser."""

    def test_time(self):
        """Test time regex."""
        times = [
            '22:50', '22:15'
        ]
        result = None

        for entry in times:
            try:
                result = time.parseString(entry)
            except pp.ParseException as x:
                pass
            self.assertEqual(entry, result.time)

    def test_nicks(self):
        """Test the nicks regex."""
        nicks = [
            'FranciscoD_',
            'FranciscoD|Uni',
            'FranciscoD^|Uni',
            'FranciscoD-_Uni',
        ]
        result = None

        for entry in nicks:
            try:
                result = nick.parseString(entry)
            except pp.ParseException as x:
                pass
            self.assertEqual(entry, result.nick)

    def test_actions(self):
        """Test actions."""
        result = None
        example = "22:11  * FranciscoD|Uni goes off for a bit"
        try:
            result = action.parseString(example)
        except pp.ParseException as x:
            pass

        self.assertEqual("FranciscoD|Uni", result.nick)
        self.assertEqual("22:11", result.time)

    def test_chats(self):
        """Test chats."""
        result = None
        examples = [
            "21:51 < FranciscoD|new> seeing if ??I can easily extend pisg",
            "22:47 < FranciscoD__^> haha,  why f23"
        ]
        for example in examples:
            result = None
            try:
                result = chatline.parseString(example)
            except pp.ParseException as x:
                pass
            self.assertIsNotNone(result)



    def test_joins(self):
        """Test joins."""
        result = None
        example = "14:20 -!- FranciscoD [franciscod@something] has joined #fedora"
        try:
            result = notification.parseString(example)
        except pp.ParseException as x:
            pass

        self.assertEqual("FranciscoD", result.nick)
        self.assertEqual("14:20", result.time)
        self.assertTrue('has joined' in result.detail, msg=result.detail)

    def test_leaves(self):
        """Test leaves and quits."""
        result = None
        example = "20:40 -!- FranciscoD_ [franciscod@something] has quit [Ping timeout: 258 seconds]"
        try:
            result = notification.parseString(example)
        except pp.ParseException as x:
            pass

        self.assertEqual("FranciscoD_", result.nick)
        self.assertNotEqual("FranciscoD|Uni", result.nick)
        self.assertEqual("20:40", result.time)
        self.assertTrue('has quit' in result.detail or 'has left' in result.detail, msg=result.detail)

    def test_renicks(self):
        """Test nick changes."""
        result = None
        example = "21:38 -!- FranciscoD|Uni is now known as FranciscoD"
        try:
            result = notification.parseString(example)
        except pp.ParseException as x:
            pass

        self.assertEqual("FranciscoD|Uni", result.nick)
        self.assertEqual("21:38", result.time)
        self.assertTrue('is now known as' in result.detail, msg=result.detail)


if __name__ == "__main__":
    unittest.main()
