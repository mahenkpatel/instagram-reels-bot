import os
import requests
from time import sleep
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
VIDEOS_DIR = os.path.join(DATA_DIR, 'videos')

def send_video_to_telegram(filepath, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"
    with open(filepath, 'rb') as video:
        files = {'video': video}
        data = {'chat_id': CHAT_ID, 'caption': caption}
        response = requests.post(url, data=data, files=files)

    if response.status_code == 200:
        print(f"✅ Sent: {os.path.basename(filepath)}")
        return True
    else:
        print(f"❌ Failed to send {os.path.basename(filepath)}: {response.text}")
        return False

def send_all_videos():
    if not os.path.exists(VIDEOS_DIR):
        print(f"📁 'videos' folder does not exist: {VIDEOS_DIR}")
        return

    for file in os.listdir(VIDEOS_DIR):
        if file.lower().endswith(".mp4"):
            filepath = os.path.join(VIDEOS_DIR, file)

            # Check for URL file
            url_file = os.path.splitext(filepath)[0] + ".txt"
            caption = "NO URL AVAILABLE"
            if os.path.exists(url_file):
                with open(url_file, 'r') as f:
                    caption = f.read().strip()

            if send_video_to_telegram(filepath, caption):
                os.remove(filepath)
                if os.path.exists(url_file):
                    os.remove(url_file)

                sleep(2)

if __name__ == "__main__":
    send_all_videos()
