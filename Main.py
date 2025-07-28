import yt_dlp
import os
import sys
import time
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def is_ffmpeg_available(ffmpeg_path='ffmpeg'):
    try:
        subprocess.run([ffmpeg_path, '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False

FFMPEG_PATH = rf"{SCRIPT_DIR}\ffmpeg\bin\ffmpeg.exe"  # Update this to match your local path

# Progress bar simulation (used with hooks)
def progress_function(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '').strip().replace('%', '')
        speed = d.get('_speed_str', '').strip()
        try:
            percent_float = float(percent)
        except:
            percent_float = 0

        bar_len = 40
        filled_len = int(bar_len * percent_float // 100)
        bar = '\033[42m' + ' ' * filled_len + '\033[0m' + ' ' * (bar_len - filled_len)
        sys.stdout.write(f"\r{percent_float:5.1f}% [{bar}] {speed}")
        sys.stdout.flush()

ydl_opts = {
    'ffmpeg_location': FFMPEG_PATH,
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',
    'progress_hooks': [progress_function]
}

if not is_ffmpeg_available(FFMPEG_PATH):
    print("❌ FFmpeg not found! Please check the path.")


# Metadata preview
def GetYoutubeVideoData(URL: str):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(URL, download=False)
            return True, info
    except Exception as e:
        return False, str(e)

# Download logic
def download_content(URL, option, directory):
    if option == "1":
        format_code = 'bestvideo+bestaudio/best'
    else:
        format_code = 'bestaudio/best'

    ydl_opts = {
        'format': format_code,
        'ffmpeg_location': FFMPEG_PATH,  # 👈 Add this!
        'outtmpl': os.path.join(directory, '%(title)s.%(ext)s'),
        'merge_output_format': 'mkv',
        'progress_hooks': [progress_function],
    }

    print("\nStarting download...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([URL])
    print(f"\n✅ Download completed to: {directory}")

# Main program flow
def Entry():
    print(f"Welcome to ZakYT Youtube Video/Audio Downloader!\nThis product is licenced with the GPL-V3 License. This means this program's code is FREE open-source and must stay open-source and FREE for any derivative works of this product!\nThe original version of this program can be found at ZakDevOnGitHub/ZakYT\n\n⚠️  Legal Disclaimer: It is YOUR SOLE RESPONSIBILITY to use this program within legal boundaries. Any unauthorized use of copyrighted content is a violation of applicable copyright laws. ZakDevOnGitHub holds NO LIABILITY for the misuse of this program!")
    print("\nPlease select an option from the menu below:")
    print("\n1. Download a video from YouTube")
    print("2. Download an audio from YouTube")
    print("CTRL + C to exit")

    option = input("Select Option: ")
    if option not in ["1", "2"]:
        print("❌ Invalid option.")
        return Entry()

    url = input("Enter YouTube URL: ")
    if not url.startswith("https://www.youtube.com/watch?v="):
        print("❌ Invalid URL format.")
        return Entry()

    success, data = GetYoutubeVideoData(url)
    if not success:
        print(f"❌ Error: {data}")
        return Entry()

    print(f"\nTitle: {data.get('title')}")
    print(f"Author: {data.get('uploader')}")
    print(f"Views: {data.get('view_count')}")
    print(f"Length: {int(data.get('duration'))} sec")
    print(f"Description: {data.get('description', '')[:200]}...")
    confirm = input("Is this the correct video? (y/n): ").lower()
    if confirm != "y":
        print("Restarting...\n")
        return Entry()

    directory = input("Enter download directory: ")
    if not os.path.exists(directory):
        create = input("Directory not found. Create it? (y/n): ").lower()
        if create == "y":
            os.makedirs(directory)
            print(f"📁 Created: {directory}")
        else:
            print("Exiting...")
            return

    download_content(url, option, directory)

Entry()