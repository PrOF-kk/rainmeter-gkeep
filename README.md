# Rainmeter-GKeep
<img align="right" width="10%" src="res/graphics/rainmeter-gkeep-icon.svg" />

Rainmeter-GKeep is a Rainmeter meter which, alongside a note-taking skin of your choosing, allows to display and update a Google Keep note directly from your desktop

## Prerequisites

* Python ≥3.9
* [Gkeepapi](https://github.com/kiwiz/gkeepapi)
* [Keyring](https://pypi.org/project/keyring/)

```batch
pip install gkeepapi
pip install keyring
```

## Installation

1. Either clone the repository or [download it as ZIP](https://github.com/PrOF-kk/rainmeter-gkeep/archive/refs/heads/master.zip)  
2. Copy the `Skins\Keep` folder to your Rainmeter Skin installation folder, usually `C:\Users\%username%\Documents\Rainmeter\Skins`
3. Modify the `Keep\@Resources\Settings.inc` file:
   * `USER_EMAIL`: Your e-mail (example@gmail.com)
   * `APP_PASSWORD`: If you have enabled 2-factor-authentication for your Google account you'll need to create an [App Password](https://support.google.com/accounts/answer/185833), otherwise you can use your normal password
   * `NOTE_ID`: The ID of the note you want displayed, it is the last part of the URL when viewed in a web browser (`https://keep.google.com/u/0/#NOTE/COPY_THIS_PART`)
4. From the "Manage Rainmeter" screen, double-click `Keep.ini` and try it out. If it's working properly, a black window with your note's contents should appear
5. To use rainmeter-skeep with another note-taking skin, set `OUTPUT_FILE` to the relative path to your skin's note file.  
   For example, for the [Paper::Notes by Haitime](https://www.deviantart.com/haitime/art/Paper-Notes-399129789) skin you'd set it to `../Paper/Notes/Note 1/my.notes`
6. To disable the ugly default black window, set `HIDE_OUTPUT_VIEWER` to 1

## Contributing
1. Clone the repository
2. Insert your credentials in the `debug_settings.ini` file (ignored by Git)
3. To test your changes, run `build.py`
4. There's a shortcut (.lnk) file to quickly open the Installed Skins folder

## License
[MIT](https://choosealicense.com/licenses/mit/)
