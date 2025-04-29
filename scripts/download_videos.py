import os
import json
import instaloader
import shutil
import re
import time
import random
from datetime import datetime

def get_data_directory():
    """
    Returns the absolute path of a 'data' folder located one level above the script's directory.
    Creates the folder if it doesn't exist.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(parent_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

# Global data directory used for all file operations.
DATA_DIR = get_data_directory()

def login_with_cookies(loader, cookie_file):
    """
    Loads cookies from the specified JSON file within the DATA_DIR and sets the session cookies
    for instaloader.
    """
    cookie_path = os.path.join(DATA_DIR, cookie_file)
    with open(cookie_path, 'r') as f:
        cookies = json.load(f)
    session = {cookie['name']: cookie['value'] for cookie in cookies}
    loader.context._session_cookies = session

def sanitize_filename(name):
    """
    Removes illegal characters from file names.
    """
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()

def truncate_filename(name, max_length=50):
    """
    Truncates the file name to ensure its length does not exceed max_length.
    Leaves room for a file extension.
    """
    return name[:max_length - 4] if len(name) > max_length - 4 else name

def log(message):
    """
    Logs a message to the console with a timestamp.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")

def download_reels(file_path, cookie_file, max_retries=3):
    """
    Downloads reels based on a list of URLs provided in the file (located in DATA_DIR) and saves
    them in a subdirectory called 'videos' (also under DATA_DIR). Retries downloads upon errors.
    Once processing is complete, the URL file is cleared.
    """
    # Build the path to the videos folder (renamed from 'downloads') and ensure it exists.
    videos_dir = os.path.join(DATA_DIR, "videos")
    os.makedirs(videos_dir, exist_ok=True)
    
    # Create an instaloader instance
    loader = instaloader.Instaloader(
        dirname_pattern="temp_reel_download",
        download_comments=False,
        save_metadata=False,
        post_metadata_txt_pattern='',
        download_video_thumbnails=False
    )
    login_with_cookies(loader, cookie_file)

    # Build full path for the URL file.
    file_path_full = os.path.join(DATA_DIR, file_path)
    with open(file_path_full, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    total_urls = len(urls)
    for i, url in enumerate(urls, 1):
        retries = 0
        success = False
        while retries < max_retries:
            temp_dir = "temp_reel_download"  # Temporary directory used by instaloader.
            try:
                shortcode = url.rstrip('/').split("/")[-1]
                log(f"⬇️ Downloading Reel {i}/{total_urls}: {url} (Attempt {retries + 1})")
                post = instaloader.Post.from_shortcode(loader.context, shortcode)
                loader.download_post(post, target=temp_dir)

                # Construct a base file name using the shortcode and a snippet of the caption.
                base_name = post.shortcode
                if post.caption:
                    caption_snippet = "_".join(post.caption.strip().split()[:6])
                    base_name += "_" + sanitize_filename(caption_snippet)
                base_name = truncate_filename(base_name)

                # Locate the downloaded video file and move it to the videos directory.
                for file in os.listdir(temp_dir):
                    if file.endswith(".mp4"):
                        src = os.path.join(temp_dir, file)
                        dst = os.path.join(videos_dir, f"{base_name}.mp4")
                        shutil.move(src, dst)
                        log(f"✅ Saved: {dst}")
                        success = True
                        break
                break  # Exit retry loop if the download succeeded.

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
                shutil.rmtree(temp_dir, ignore_errors=True)

    # Clear the URL file after processing all downloads.
    log(f"🧹 Clearing {file_path_full}")
    with open(file_path_full, 'w') as f:
        f.truncate(0)
    log("📁 Done. reels_urls.txt cleared.")

if __name__ == "__main__":
    download_reels("reels_urls.txt", "instagram_cookies.json")
