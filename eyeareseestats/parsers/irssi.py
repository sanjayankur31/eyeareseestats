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

time = pp.Regex('([01]\d|2[0-3]):([0-5]\d)')
nick = pp.Regex('[a-zA-Z0-9\-_|^]+')
userhost = pp.Literal('[') + pp.Regex('[a-zA-Z0-9\-_|^.@~]+') + pp.Literal(']')
detail = pp.restOfLine

chat = pp.Literal('<') + nick + pp.Literal('>') + detail
action = pp.Literal('*') + nick + detail
notification = pp.Literal('-!-') + nick + pp.Optional(userhost) + detail

sentence = pp.Or([action, chat, notification])
logentry = time + sentence
