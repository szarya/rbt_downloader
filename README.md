# rbt_downloader
A small python3 script that downloads all the user owned videos from Ramits Brain Trust

## Prerequisites
This is a python3 script.
If you don't have python3 installed, download and install it from:
https://www.python.org/downloads/
**Be sure to tick the Add python to PATH checkbox during installation**

## Installation
You can download this script as a zip file, or just clone it from git. 
The link to the download is in the upper left corner of the page.
Once you've downloaded the files, unzip them to a folder on your drive.
*Note that the script will download the files into this folder, so make sure that you have enough free storage - the average episode takes about 1.5GB of space*

## Automatic installation - Windows
Navigate to the folder with the script, and run windows.bat


## Manual installtion - Windows/Linux/Mac OS
Now, you need to install the packages the script depends upon:
Open the terminal, and navigate to the folder with the script.
Now run:
```
pip install -r requirements.txt
```

Now, open settings.py in any text editor and replace [YOUR_EMAIL] and [YOUR_PASSWORD] with your RBT email and password.

Finally, you can start the script by running:
```
python main.py
```

The script should take several hours to complete, depending on your internet connection.
If the script fails midway, you can run it again, and it will pick up from the last episode it downloaded.

## Output
All the episoded will be in the RBT folder, named under the following convention:
[EPISODE_NUMBER]_[TITLE]_[AUTHOR]
The will four files per episode:
- mp4 for the video
- mp3 for audio
- pdf with the transcript
- html with a stripped down version of the episodes page, including the comments

Enjoy!
