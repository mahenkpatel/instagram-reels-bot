import os
import requests
import time
from time import sleep
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_data_directory():
    """
    Returns the absolute path to a 'data' directory located one level above this script.
    Creates the directory if it doesn't exist.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(parent_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

# Centralize Data Directory usage.
DATA_DIR = get_data_directory()
VIDEOS_FOLDER = os.path.join(DATA_DIR, "videos")  # 'videos' folder replaces 'downloads'

def send_video_to_telegram(filepath):
    """
    Sends a single video file to Telegram using the bot API.
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"
    try:
        with open(filepath, 'rb') as video:
            files = {'video': video}
            data = {'chat_id': CHAT_ID, 'caption': os.path.basename(filepath)}
            response = requests.post(url, data=data, files=files)
        if response.status_code == 200:
            print(f"✅ Sent: {os.path.basename(filepath)}")
            return True
        else:
            print(f"❌ Failed to send: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception while sending {os.path.basename(filepath)}: {e}")
        return False

def send_all_videos():
    """
    Sends out all MP4 files found in the videos folder.
    If a video is sent successfully, it is removed from the folder.
    """
    if not os.path.exists(VIDEOS_FOLDER):
        print(f"📁 '{VIDEOS_FOLDER}' folder does not exist.")
        return

    # Gather all MP4 files from the videos folder.
    video_files = [file for file in os.listdir(VIDEOS_FOLDER) if file.lower().endswith(".mp4")]
    if not video_files:
        print("📁 No video files to send at this time.")
        return

    for file in video_files:
        filepath = os.path.join(VIDEOS_FOLDER, file)
        if send_video_to_telegram(filepath):
            os.remove(filepath)
            sleep(2)  # Adding a small delay between sends to avoid hitting Telegram rate limits.

if __name__ == "__main__":
    send_all_videos()
