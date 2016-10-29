#!/usr/bin/env python3
"""
Test irssi logs

File:

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
from eyeareseestats.parsers.irssi import logentry


class TestIRSSILogs(unittest.TestCase):

    """Test for IRSSI parser."""

    def test_parser(self):
        """Match with test strings."""
        fullstatements = [
            "21:51 <FranciscoD|Uni> seeing if I can easily extend pisg",
            "20:40 -!- satya4ever [~sbulage@103.25.3.2] has quit [Ping timeout: 258 seconds]",
            "14:20 -!- chillsuk [~ch@host-92-18-149-93.as13285.net] has joined #fedora",
            "22:11  * FranciscoD|Uni goes off for a bit",
            "21:38 -!- jhunt|kcs is now known as jhunt"
        ]

        nicks = [
            'FranciscoD_',
            'FranciscoD|Uni',
            'FranciscoD^|Uni',
            'FranciscoD\$Uni',
            'FranciscoD-_Uni',
        ]

        for sentence in fullstatements:
            try:
                result = logentry.parseString(sentence)
                print("Matches: {}".format(result))
            except pp.ParseException as x:
                print("{} does not match".format(sentence))

if __name__ == "__main__":
    unittest.main()
