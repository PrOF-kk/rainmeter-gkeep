# Copyright (c) 2021 Valerio Colella
# SPDX-License-Identifier: MIT

# Build script: move everything in the correct Rainmeter Skins folder for testing

import shutil
import os

print(shutil.copytree("Skins\\Keep", os.environ["USERPROFILE"] + "\\Documents\\Rainmeter\\Skins\\Keep\\", dirs_exist_ok=True))
