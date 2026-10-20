# 📥 YouTube Downloader Pro (Linux GUI)

A high-performance, modern Linux graphical user interface (GUI) built with Python and CustomTkinter. It acts as a visual wrapper for **yt-dlp** and **FFmpeg**, allowing users to download single videos or full playlists easily with real-time progress tracking.

---

## 🚀 Features
* **Modern Dark UI**: Clean, professional, and responsive interface built with `CustomTkinter`.
* **Automatic Playlist Detection**: Automatically detects whether the pasted URL is a single video or a full playlist based on URL patterns.
* **Interactive Playlist Filter**: View a collapsible list of all playlist videos and deselect/exclude any items you don't want to download.
* **Dynamic Quality Selection**: Fetch and select exact video resolutions dynamically.
* **Real-time Progress Tracker**: Live progress bar showing download percentage, speed, and status.
* **Quick Path Manager**: Save and instantly select from your favorite download directories.
* **Font Scaling Support**: Adjust UI font size on the fly (Base, Large, X-Large).
* **Built-in Developer Docs**: Integrated documentation window inside the app.

---

## 🛠️ Prerequisites & Dependencies
Make sure your Linux system (Kali Linux / Ubuntu) has Python 3, pip, and FFmpeg installed:

```bash
sudo apt update
sudo apt install python3 python3-pip ffmpeg -y
```

## ⚙️ Installation Guide

1- Clone the repository:

git clone [https://github.com/osmahdy/yt-gui-pro.git](https://github.com/osmahdy/yt-gui-pro.git)
cd yt-gui-pro

2- Create and activate a Python Virtual Environment:

python3 -m venv myenv
source myenv/bin/activate

3- Install required dependencies:

pip install -r requirements.txt

To install the required `customtkinter` library and any other dependencies listed in the project, run:
   
   pip install -r requirements.txt

## 🖥️ Desktop Integration (Kali Linux Application Menu)

To add the application to your system application menu for single-click launching without using the terminal:

1-  Create a .desktop entry file:
    Bash

nano ~/.local/share/applications/ytdl-pro.desktop

2- Paste the following configuration (make sure to replace /home/yt-gui-pro with your actual project directory path):
Code snippet

[Desktop Entry]
Name=YouTube Downloader Pro
Comment=Advanced YouTube Downloader with GUI
Exec=/home/yt-gui-pro/myenv/bin/python /home/yt-gui-pro/ytdl_pro.py
Icon=applications-multimedia
Terminal=false
Type=Application
Categories=AudioVideo;Network;

3- Save the file and grant executable permissions:
Bash

  chmod +x ~/.local/share/applications/ytdl-pro.desktop

Now you can search for YouTube Downloader Pro directly in your Kali Linux application launcher!

## 📖 Usage

1- Run the script from terminal:

python ytdl_pro.py

(Or launch it from your desktop applications menu).

2- Paste any YouTube video or playlist link.

3- Choose your save directory or pick from Quick Paths.

4- Click Fetch Data to load qualities or playlist items.

5- Click Start Download and track the progress.

## 📄 License

This project is open-source and available under the MIT License.
