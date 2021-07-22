# Rainmeter-GKeep

Rainmeter-GKeep is a proof-of-concept Rainmeter meter to display a note from Google Keep on the desktop

## Prerequisites

Python and the gkeepapi library are required

```batch
pip install gkeepapi
```

## Installation

1. Clone the repository
```batch
git clone https://github.com/PrOF-kk/rainmeter-gkeep
```
2. Copy the downloaded folder to your Rainmeter Skin installation folder, usually `C:\Users\%username%\Documents\Rainmeter\Skins`
3. Modify the following variables:
  * Keep.py
    * `USERNAME`: Your e-mail (example@gmail.com)
    * `APP_PASSWORD`: A new app-specific password, see https://support.google.com/accounts/answer/185833
  * Keep.ini
    * `NOTE_ID`: The ID of the note you want displayed, it is the last part of the URL when viewed in a web browser (`https://keep.google.com/u/0/#NOTE/COPY_THIS_PART`)
4. From the "Manage Rainmeter" screen, double-click `Keep.ini`

## Contributing
Pull requests are welcome

## License
[MIT](https://choosealicense.com/licenses/mit/)