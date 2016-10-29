#!/usr/bin/env python3
"""
Parser for irssi log files.

- topic
- joins/leaves (-!- nick [username@host] has joined/left channel)
- bans/kicks
- actions ( * nick action)
- chats (< nick> says something)
- mentions (special case of chats when the sentence has nick in it)
- nick changes (-!- nick is now known as newnick) NOTE: for logger, "You're..")
- op/deop (-!- mode/channel [+-]o nick by nick)
- links (check actions, chats)

"""

import pyparsing as pp

time = pp.Regex('([01]\d|2[0-3]):([0-5]\d)').setResultsName('time')
nick = pp.Regex('[a-zA-Z0-9\-_|^]+').setResultsName('nick')
userhost = pp.Literal('[') + pp.Regex('[a-zA-Z0-9\-_|^.@~]+') + pp.Literal(']')
detail = pp.restOfLine.setResultsName('detail')

chat = time + pp.Literal('<') + nick + pp.Literal('>') + detail
action = time + pp.Literal('*') + nick + detail
notification = time + pp.Literal('-!-') + nick + pp.Optional(userhost) + detail
