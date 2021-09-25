# Copyright (c) 2021 Valerio Colella
# SPDX-License-Identifier: MIT

import gkeepapi
import json
import sys
import os
import configparser

from gkeepapi.node import TopLevelNode

# Constants
NOTES_CACHE_FILE: str = "./cache"

config = configparser.ConfigParser()
config.read("@Resources/Settings.inc")
USER_EMAIL: str = config["Variables"]["USER_EMAIL"]
NOTE_ID: str = config["Variables"]["NOTE_ID"]

# Not the account's main password, but one generated specifically for this script.
#TODO this is only needed for the first login, popup a window for setup the first time
APP_PASSWORD: str = "APP PASSWORD, see https://support.google.com/accounts/answer/185833 "

def main():
    func = sys.argv[1]
    
    # if first time:
    keep = gkeepapi.Keep()
    keep.login(USER_EMAIL, APP_PASSWORD)
    #TODO state cache
    #TODO else load master token and resume

    if func == "get":
        note = keep.get(NOTE_ID)
        print(note.text)
    elif func == "title":
        note = keep.get(NOTE_ID)
        print(note.title)
    else:
        print("Unimplemented command.")

if __name__ == "__main__":
    main()
