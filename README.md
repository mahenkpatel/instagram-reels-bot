# 🎥 Instagram Reels to Telegram Bot  

![Instagram Automation](https://img.shields.io/badge/Instagram-Automation-red?style=for-the-badge)  
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg?style=flat-square)  

> 🚀 **Automatically download trending Instagram reels and send them directly to your Telegram account—stay in control of your content consumption!**  

---

## 📖 Table of Contents  

- [📖 Table of Contents](#-table-of-contents)  
- [🔍 Overview](#-overview)  
- [✨ Features](#-features)  
- [🛠 Installation](#-installation)  
  - [Clone the Repository](#1️⃣-clone-the-repository)  
  - [Create a Virtual Environment](#2️⃣-create-a-virtual-environment-recommended)  
  - [Install Dependencies](#3️⃣-install-dependencies)  
- [⚙️ Configuration](#-configuration)  
  - [Customizing Reel Collection](#-customizing-reel-collection)  
- [🚀 How to Use](#-how-to-use)  
  - [First Run](#-first-run)  
  - [Subsequent Runs](#-subsequent-runs)  
- [📅 Automate with Cron](#-automate-with-cron)  
  - [What does this do?](#-what-does-this-do)  
- [📜 Disclaimer](#-Disclaimer)  

---

## 🔍 Overview  

The **Instagram Reels to Telegram Bot** automates downloading top reels from Instagram and sends them to a specified Telegram account.  

✔️ **No more endless scrolling**—control your Instagram reel consumption.  
✔️ **Automate the process** so reels appear in your Telegram chat without manual effort.  

> _I created this tool to eliminate doomscrolling while still getting periodic reels. I deleted the Instagram app and now have full control over how many reels I watch per day._  

---

## ✨ Features  

✅ **Automated Reel Downloading** – Fetch trending Instagram reels effortlessly.  
✅ **Customizable Limits** – Define how many reels to download per cycle.  
✅ **Telegram Integration** – Videos are sent directly to your Telegram chat via a bot.  
✅ **Smart Folder Structure** – Organizes downloaded videos in `data/videos` for easy access.  
✅ **Cookie-based Login** – Saves login credentials for seamless Instagram authentication.  
✅ **Robust Error Handling** – Built-in retry mechanism prevents failures.  

---

## 🛠 Installation  

### 1️⃣ Clone the Repository  

```bash
git clone https://github.com/yourusername/instagram-reels-bot.git
cd instagram-reels-bot
```

### 2️⃣ Create a Virtual Environment (Recommended)

```
python -m venv venv
source venv/bin/activate  # Windows users: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

> ⚠️ Note: Python 3.8+ is required. Ensure you have Chromedriver installed for Selenium to function properly.

### ⚙️ Configuration

Rename `.env.template` to `.env` and populate with your own Instagram and Telegram credentials.

```
# Instagram Credentials  
INSTAGRAM_USERNAME=your_instagram_username  
INSTAGRAM_PASSWORD=your_instagram_password  
REELS_TO_COLLECT=20  

# Telegram Bot Credentials  
TELEGRAM_BOT_TOKEN=your_telegram_bot_token  
TELEGRAM_CHAT_ID=your_telegram_chat_id  
```

### 🔹 Customizing Reel Collection

The script downloads ±5 reels from the defined REELS_TO_COLLECT value to prevent Instagram from detecting automation. Set a number higher than 5 for reliability.

### 🚀 How to Use

```
chmod +x run_all.sh  
./run_all.sh
```

### ✅ First Run

- Opens Instagram via Selenium for login.

- Saves login session as cookies for future runs.

### 🔄 Subsequent Runs

- Uses stored cookies instead of logging in again.

- If cookies expire, the script automatically reauthenticates using the browser.

📅 Automate with Cron

```
0 */2 * * * /home/ubuntu/instagram-reels-bot/run_all.sh >> /home/ubuntu/instagram-reels-bot/cronoutput.log 2>&1
```

### 🕒 What does this do?

✅ Runs the script every 2 hours ✅ Logs output in cronoutput.log for debugging

> 🔹 Customize the cron frequency to align with your reel-watching habits!

### 📜 Disclaimer

> This project is provided "as is" without any warranties or guarantees. The author(s) and contributors assume no responsibility for any issues, damages, or consequences resulting from the use of this code. Use at your own risk.
