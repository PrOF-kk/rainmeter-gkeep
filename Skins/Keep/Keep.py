# Copyright (c) 2021 Valerio Colella
# SPDX-License-Identifier: MIT

import gkeepapi
import json
import sys
import os
import configparser

from gkeepapi.node import TopLevelNode

# Constants
SCRIPT_STATE_FILE: str = "./script_state"
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
    state = initialize()

    if func == "get":
        note = getNote(state, NOTE_ID)
        print(note.text)
    elif func == "cache":
        saveNoteCache(state.keep)
    elif func == "title":
        note = getNote(state, NOTE_ID)
        print(note.title)
    else:
        print("Unimplemented command, exiting")

class State:
    '''Class representing data that should persist between script launches'''
    keep: gkeepapi.Keep = None
    username: str = None
    # This is unsafe, use a keyring in the future
    masterToken: str = None


def initialize() -> State:
    '''Initializes script for first-time run, or restores previous script state'''
    if os.path.isfile(SCRIPT_STATE_FILE):
        # State file found. Resume Keep object and return state
        return getScriptState()
    else:
        # First time setup
        return doFirstTimeSetup()

def doFirstTimeSetup() -> State:
    state = State()
    state.keep = gkeepapi.Keep()
    state.username = USER_EMAIL
    loginKeep(state, APP_PASSWORD)
    state.masterToken = state.keep.getMasterToken()
    #saveScriptState(state)
    return state

# Note handling
def getNote(state: State, noteId: str) -> TopLevelNode:
    return state.keep.get(noteId)

# Script state
def saveScriptState(state: State):
    '''Saves the current script state to json'''
    with open(SCRIPT_STATE_FILE, 'w+') as stateFile:
        json.dump(state, stateFile)

def getScriptState() -> State:
    '''Returns the script state from json file'''
    with open(SCRIPT_STATE_FILE) as stateFile:
        return json.load(stateFile)

# Keep state methods
def resumeKeep(state: State):
    k = state.keep
    k.resume(state.username, state.masterToken)

def resumeKeepCache(state: State):
    k = state.keep
    k.resume(state.username, state.masterToken, getNoteCache())

def loginKeep(state: State, password: str):
    k = state.keep
    k.login(state.username, password)

def loginKeepCache(state: State, password: str):
    k = state.keep
    k.login(state.username, password, getNoteCache())

# Note cache methods
def getNoteCache():
    with open(NOTES_CACHE_FILE, 'r') as cache:
        return json.load(cache)

def saveNoteCache(keep: gkeepapi.Keep):
    with open(NOTES_CACHE_FILE, 'w+') as cache:
        json.dump(keep.dump(), cache)

if __name__ == "__main__":
    main()
