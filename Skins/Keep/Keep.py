# Copyright (c) 2021 Valerio Colella
# SPDX-License-Identifier: MIT

import gkeepapi
import json
import sys
import os

from gkeepapi.node import TopLevelNode

# Constants
SCRIPT_STATE_FILE: str = "./script_state"
NOTES_CACHE_FILE: str = "./cache"

USERNAME: str = "YOUR.EMAIL@gmail.com"
# Not the account's main password, but one generated specifically for this script.
# In te future this could be made easier by prompting a Google sign-in
APP_PASSOWRD: str = "APP PASSWORD, see https://support.google.com/accounts/answer/185833 "

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
    state.username = USERNAME
    loginKeep(state, APP_PASSOWRD)
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

# main
func = sys.argv[1]
state = initialize()

if func == "get":
    note = getNote(state, sys.argv[2])
    print(note.text)
elif func == "cache":
    saveNoteCache(state.keep)
elif func == "title":
    note = getNote(state, sys.argv[2])
    print(note.title)
else:
    print("Unimplemented command, exiting")

print("done")