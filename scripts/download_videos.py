import json
import os
import instaloader
import shutil
import re
import time
import random
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
VIDEOS_DIR = os.path.join(DATA_DIR, 'videos')
COOKIES_FILE = os.path.join(DATA_DIR, 'instagram_cookies.json')
URLS_FILE = os.path.join(DATA_DIR, 'reels_urls.txt')

os.makedirs(VIDEOS_DIR, exist_ok=True)

def login_with_cookies(loader, cookie_file):
    with open(cookie_file, 'r') as f:
        cookies = json.load(f)
    session = {cookie['name']: cookie['value'] for cookie in cookies}
    loader.context._session_cookies = session

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()

def truncate_filename(name, max_length=50):
    return name[:max_length - 4] if len(name) > max_length - 4 else name

def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")

def download_reels(file_path, cookie_file, max_retries=3):
    loader = instaloader.Instaloader(
        dirname_pattern="temp_reel_download",
        download_comments=False,
        save_metadata=False,
        post_metadata_txt_pattern='',
        download_video_thumbnails=False
    )
    login_with_cookies(loader, cookie_file)

    with open(file_path, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    for i, url in enumerate(urls, 1):
        retries = 0
        success = False
        while retries < max_retries:
            try:
                shortcode = url.rstrip('/').split("/")[-1]
                log(f"⬇️ Downloading Reel {i}/{len(urls)}: {url} (Attempt {retries + 1})")
                post = instaloader.Post.from_shortcode(loader.context, shortcode)
                loader.download_post(post, target="temp_reel_download")

                base_name = post.shortcode
                if post.caption:
                    caption_snippet = "_".join(post.caption.strip().split()[:6])
                    base_name += "_" + sanitize_filename(caption_snippet)
                
                base_name = truncate_filename(base_name)

                # Move the video and save the URL
                for file in os.listdir("temp_reel_download"):
                    if file.endswith(".mp4"):
                        src = os.path.join("temp_reel_download", file)
                        dst = os.path.join(VIDEOS_DIR, f"{base_name}.mp4")
                        shutil.move(src, dst)

                        # Save the URL with the same base name
                        with open(os.path.join(VIDEOS_DIR, f"{base_name}.txt"), 'w') as url_file:
                            url_file.write(url)

                        log(f"✅ Saved: {dst}")
                        success = True
                        break

                break  # Exit retry loop if successful

            except Exception as e:
                retries += 1
                log(f"❌ Error downloading Reel {i}: {e}")
                if retries < max_retries:
                    wait_time = random.randint(5, 15)
                    log(f"⏳ Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    log(f"🚫 Giving up on Reel {i} after {max_retries} attempts.")
            finally:
                shutil.rmtree("temp_reel_download", ignore_errors=True)

    # Clear the file only if all downloads were attempted
    log(f"🧹 Clearing {file_path}")
    with open(file_path, 'w') as f:
        f.truncate(0)
    log("📁 Done. reels_urls.txt cleared.")

# Run the script
if __name__ == "__main__":
    download_reels(URLS_FILE, COOKIES_FILE)
