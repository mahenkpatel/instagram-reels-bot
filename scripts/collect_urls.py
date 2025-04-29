import os
import json
import time
import re
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Determine the absolute path of the script's directory, its parent, and then the 'data' directory.
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
data_dir = os.path.join(parent_dir, "data")

# If the data directory doesn't exist, create it.
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# File paths updated to point to the 'data' directory one level above the script.
COOKIE_FILE = os.path.join(data_dir, "instagram_cookies.json")
REELS_URLS_FILE = os.path.join(data_dir, "reels_urls.txt")

# Load and randomize target count
base_count = int(os.getenv("REELS_TO_COLLECT", 20))  # fallback to 20 if not set
randomized_count = random.randint(base_count - 5, base_count + 5)

# Configuration
INSTAGRAM_URL = "https://www.instagram.com/"
USERNAME = os.getenv("INSTAGRAM_USERNAME")
PASSWORD = os.getenv("INSTAGRAM_PASSWORD")
WAIT_TIME = random.randint(20, 30)
NUM_OF_REELS = randomized_count

print(f"Collecting {NUM_OF_REELS} URLs")

def save_cookies(driver, filename):
    cookies = driver.get_cookies()
    with open(filename, 'w') as f:
        json.dump(cookies, f)
    print(f"✅ Cookies saved to {filename}")

def load_cookies(driver, filename):
    if not os.path.exists(filename):
        return False
    with open(filename, 'r') as f:
        cookies = json.load(f)
    driver.get("https://www.instagram.com/")
    time.sleep(3)
    driver.delete_all_cookies()
    for cookie in cookies:
        if 'sameSite' in cookie and cookie['sameSite'] not in ['Strict', 'Lax', 'None']:
            cookie['sameSite'] = 'Lax'
        driver.add_cookie(cookie)
    print(f"✅ Cookies loaded from {filename}")
    return True

def login_to_instagram(driver, username, password):
    print("🔐 Attempting to login...")
    driver.get(INSTAGRAM_URL)
    time.sleep(3)
    try:
        WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "input"))
        )
        inputs = driver.find_elements(By.TAG_NAME, "input")
        if len(inputs) < 2:
            raise NoSuchElementException("Couldn't find login fields")
        inputs[0].send_keys(username)
        inputs[1].send_keys(password)
        login_buttons = driver.find_elements(By.TAG_NAME, "button")
        for button in login_buttons:
            if button.text.lower() in ['log in', 'login']:
                button.click()
                break
        time.sleep(5)
        for label in ["Not Now", "Turn On Notifications"]:
            try:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"//button[contains(., '{label}')]"))
                ).click()
            except (NoSuchElementException, TimeoutException):
                pass
        WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(@aria-label, 'Home')]"))
        )
        save_cookies(driver, COOKIE_FILE)
        print("✅ Login successful!")
        return True
    except Exception as e:
        print(f"❌ Login failed: {str(e)}")
        return False

def is_logged_in(driver):
    try:
        driver.get("https://www.instagram.com/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(@aria-label, 'Home')]"))
        )
        return True
    except:
        return False

def collect_reels(driver, count=20):
    print("📽️ Navigating to Reels player feed...")
    driver.get("https://www.instagram.com/reels/")
    time.sleep(random.uniform(5, 7))  # Human-like initial wait

    print("🔄 Scrolling through Reels and collecting URLs from address bar...")
    collected = set()
    scroll_attempts = 0
    max_total_scrolls = 200
    total_scrolls = 0

    actions = ActionChains(driver)

    while len(collected) < count and scroll_attempts < 10 and total_scrolls < max_total_scrolls:
        raw_url = driver.execute_script("return window.location.href")
        current_url = raw_url.rstrip('/#').split("?")[0]

        if re.match(r'https://www\.instagram\.com/reels/[A-Za-z0-9_-]+$', current_url):
            if current_url not in collected:
                collected.add(current_url)
                print(f"➕ Found ({len(collected)}): {current_url}")
                scroll_attempts = 0
            else:
                scroll_attempts += 1
                print(f"🔁 Duplicate URL, attempts: {scroll_attempts}")
        else:
            print(f"❌ Not a valid Reel URL: {current_url}")
            scroll_attempts += 1

        actions.send_keys(Keys.ARROW_DOWN).perform()

        # 🕒 Wait like a human would
        watch_time = random.uniform(5, 15)
        print(f"🕒 Watching Reel for {watch_time:.2f} seconds...")
        time.sleep(watch_time)

        total_scrolls += 1

    print(f"✅ Done. Collected {len(collected)} unique Reels.")
    return list(collected)

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run headless
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)

    try:
        if not load_cookies(driver, COOKIE_FILE) or not is_logged_in(driver):
            print("🧹 No valid cookies or session expired. Logging in...")
            if not login_to_instagram(driver, USERNAME, PASSWORD):
                print("❌ Exiting. Login failed.")
                return
        reels = collect_reels(driver, NUM_OF_REELS)

        if reels:
            with open(REELS_URLS_FILE, "w") as f:
                for url in reels:
                    f.write(url + "\n")
            print(f"📁 Saved reel URLs to {REELS_URLS_FILE}")
        else:
            print("❌ Reels collection failed.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
