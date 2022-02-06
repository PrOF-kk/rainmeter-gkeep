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
SETTINGS_FILE_PATH = "@Resources/Settings.inc"

config = configparser.ConfigParser()
config.read(SETTINGS_FILE_PATH)
USER_EMAIL: str = config["Variables"]["USER_EMAIL"]
NOTE_ID: str = config["Variables"]["NOTE_ID"]
LOCAL_NOTE_FILE = config["Variables"]["OUTPUT_FILE"]

# Not the account's main password, but one generated specifically for this script.
# TODO this is only needed for the first login, popup a window for setup the first time
# then we save the master token in the keyring
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
        gui_login(keep) or exit()
        config_write()
        keyring.set_password("rainmeter-gkeep", USER_EMAIL, keep.getMasterToken())

    if func == "get":
        if NOTE_ID == "YOUR_NOTE_ID":
            gui_notechoice(keep) or exit()
            config_write()
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

    elif func == "notechoice":
        gui_notechoice(keep) or exit()
        config_write()

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
    except Exception:
        return None


def save_cache(keep: gkeepapi.Keep) -> None:
    """Writes note cache to disk"""

    cache = keep.dump()
    with open(NOTES_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f)


def config_write() -> None:
    config["Variables"]["USER_EMAIL"] = USER_EMAIL
    config["Variables"]["NOTE_ID"] = NOTE_ID
    config["Variables"]["OUPUT_FILE"] = LOCAL_NOTE_FILE
    config["Variables"]["APP_PASSWORD"] = APP_PASSWORD
    with open(SETTINGS_FILE_PATH, "w", encoding="utf-8") as configfile:
        config.write(configfile, space_around_delimiters=False)


# --- Gui --- #
def gui_login(keep: gkeepapi.Keep) -> bool:
    import tkinter as tk

    result = False
    padx = 10
    pady = 0

    def try_login(event=None):
        nonlocal result
        global USER_EMAIL, APP_PASSWORD
        try:
            keep.login(email.get(), pw.get())
        except gkeepapi.exception.LoginException as e:
            error_status.configure(text=f"Could not login: {repr(e)}")
        else:
            USER_EMAIL = email.get()
            APP_PASSWORD = pw.get()
            result = True
            window.destroy()

    window = tk.Tk()
    window.geometry("600x300")
    window.iconphoto(True, tk.PhotoImage(file="@Resources/rainmeter-gkeep-icon-64.png"))
    window.title("Login")

    tk.Label(text="E-mail").pack(anchor="w", padx=padx, pady=pady)
    email = tk.Entry()
    email.pack(fill="x", padx=10)

    tk.Label(text="Password").pack(anchor="w", padx=padx, pady=pady)
    pw = tk.Entry(show='•')
    pw.pack(fill="x", padx=padx, pady=pady)
    pw.bind("<Return>", try_login)

    pwinfo1 = tk.Label(text="If your account has 2-Factor-Authentication enabled, you'll need an App Password for Rainmeter-Gkeep.")
    pwinfo2 = tk.Label(text="Click here to learn more.", fg="#0077aa")
    # Avoid requiring the webbrowser library
    pwinfo2.bind("<Button-1>", lambda x: os.system("start https://support.google.com/accounts/answer/185833"))
    pwinfo1.pack(anchor="w", padx=padx, pady=pady)
    pwinfo2.pack(anchor="w", padx=padx, pady=pady)

    error_status = tk.Label(text="", fg="#cc0000")
    error_status.pack(anchor="w", padx=padx, pady=pady)

    lbtn = tk.Button(text="Login", command=try_login)
    lbtn.pack()

    window.mainloop()
    return result


def gui_notechoice(keep: gkeepapi.Keep) -> bool:
    import tkinter as tk
    import gkeepapi.node

    def select(event=None):
        nonlocal result
        global NOTE_ID
        # curselection returns a tuple (start, end)
        NOTE_ID = notes[notebox.curselection()[0]].id
        result = True
        root.destroy()

    result = False

    root = tk.Tk()
    root.geometry("600x300")
    root.iconphoto(True, tk.PhotoImage(file="@Resources/rainmeter-gkeep-icon-64.png"))
    root.title("Choose note")

    window = tk.Frame(root)
    window.rowconfigure(0, weight=4)
    window.rowconfigure(1, weight=1)
    window.columnconfigure(0, weight=1)

    notes: list[gkeepapi.node.TopLevelNode] = keep.all()
    notestrings = tuple(el.title if el.title != "" else el.text for el in notes)
    notebox = tk.Listbox(window, listvariable=tk.StringVar(value=notestrings))
    notebox.grid(row=0, column=0, sticky="news")
    notebox.select_set(0)

    selectbtn = tk.Button(window, text="Select", command=select)
    selectbtn.grid(row=1, column=0)

    window.pack(fill="both", expand=True, padx=16, pady=9)
    root.mainloop()

    return result


if __name__ == "__main__":
    main()
