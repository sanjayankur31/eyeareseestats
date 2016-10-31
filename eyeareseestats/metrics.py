#!/usr/bin/env python3
"""
Calculate useful metrics from information that we gather from logs.

File: metrics.py

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


# For development only
debug = True

# Metrics #
# Dictionary of users with their total activity count
activitylist = {}
# Total list of topics
topiclist = []
# Dictionary of users and how many times they joined
joinlist = {}
# Dictionary of users and how many times they left or quit
quitlist = {}
# List of list of nicks - that are for the same user if we can figure that out
nicklist = []
# Dictionary of users and their dialogues - get metrics from this too
dialoguelist = {}
# Dictionary of users and list of who they mention (mentioned nicks are
# repeated so that we can count frequency of how much people speak to each
# other
mentionlist = {}
# Dictionary of users and a list of their actions
actionlist = {}
# A list of times from all activity - to find trends and frequencies
timelist = {}
# A list of links taken from the logs
# permit repetition to count how popular a URL is
urllist = {}
