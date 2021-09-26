# Copyright (c) 2021 Valerio Colella
# SPDX-License-Identifier: MIT

import shutil
import os
import configparser

SOURCE = "Skins\\Keep"
INSTALL_LOCATION = os.environ["USERPROFILE"] + "\\Documents\\Rainmeter\\Skins\\Keep\\"

# Move everything in the correct Rainmeter Skins folder for testing
print(shutil.copytree(SOURCE, INSTALL_LOCATION, dirs_exist_ok=True))

# Overwrite placeholder variables with debug ones
config = configparser.ConfigParser()
config.read("debug_settings.ini")
with open(INSTALL_LOCATION + "@Resources\\Settings.inc") as configfile:
    config.write(configfile)
