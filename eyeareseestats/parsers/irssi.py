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
