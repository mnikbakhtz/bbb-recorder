# bbb-recorder
This script takes multiple bigbluebutton session page and creates a 720p mp4 video file as result.
Note that this only works if the presenter shared the DESKTOP and does not support Chat, Poll or Slides.

# Usage
1. Put your session url in url.txt file.
2. Run the script.
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 bbb-recorder.py -f url.txt
```
# Note: You have to have ffmpeg and Google Chrome installed on your OS.
```
sudo apt install ffmpeg
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
# You might need to run these two as well
sudo apt-get install -f
sudo dpkg -i google-chrome-stable_current_amd64.deb

```
