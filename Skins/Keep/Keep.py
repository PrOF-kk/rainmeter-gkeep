# Copyright (c) 2021 Valerio Colella
# SPDX-License-Identifier: MIT

import json
import sys
import os
import configparser
import gkeepapi
import keyring

# Constants
NOTES_CACHE_FILE: str = "./cache"

config = configparser.ConfigParser()
config.read("@Resources/Settings.inc")
USER_EMAIL: str = config["Variables"]["USER_EMAIL"]
NOTE_ID: str = config["Variables"]["NOTE_ID"]
LOCAL_NOTE_FILE = config["Variables"]["OUTPUT_FILE"]

# Not the account's main password, but one generated specifically for this script.
#TODO this is only needed for the first login, popup a window for setup the first time
APP_PASSWORD: str = config["Variables"]["APP_PASSWORD"]

def main():
    func = sys.argv[1]

    keep = gkeepapi.Keep()
    master_token = keyring.get_password("rainmeter-gkeep", USER_EMAIL)
    # if not first time:
    if master_token is not None:
        try:
            keep.resume(USER_EMAIL, master_token, load_cache())
            keyring.get_password("rainmeter-gkeep", USER_EMAIL)
        except gkeepapi.exception.LoginException:
            keep.login(USER_EMAIL, APP_PASSWORD, load_cache())
            keyring.set_password("rainmeter-gkeep", USER_EMAIL, keep.getMasterToken())
    else:
        keep.login(USER_EMAIL, APP_PASSWORD, load_cache())
        keyring.set_password("rainmeter-gkeep", USER_EMAIL, keep.getMasterToken())

    if func == "get":
        note = keep.get(NOTE_ID)
        print(note.text)

    elif func == "upload":
        note = keep.get(NOTE_ID)
        with open(LOCAL_NOTE_FILE, encoding="utf-8") as f:
            note.text = f.read()
        keep.sync()

    elif func == "title":
        note = keep.get(NOTE_ID)
        print(note.title)

    else:
        print("Unimplemented command.")

    save_cache(keep)

def load_cache():
    """Returns a dict representing the note cache, or None if file does not exist or other error"""

    if not os.path.exists(NOTES_CACHE_FILE):
        return None
    try:
        with open(NOTES_CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

def save_cache(keep: gkeepapi.Keep) -> None:
    """Writes note cache to disk"""

    cache = keep.dump()
    with open(NOTES_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f)

if __name__ == "__main__":
    main()
