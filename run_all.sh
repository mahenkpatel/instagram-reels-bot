#!/bin/bash

# Activate venv
source /home/ubuntu/.scripts/instagram_bot/venv/bin/activate

# Navigate to script directory
cd /home/ubuntu/.scripts/instagram_bot/scripts

echo -e "\n================================================================================\n                          📅 $(date +"%F %T") 📅                          \n================================================================================"


echo "📥 Collecting Reels URLs..."
python3 collect_urls.py

echo "⬇️ Downloading Reels..."
python3 download_videos.py

echo "📤 Sending to Telegram..."
python3 send_videos_to_telegram.py

echo "✅ All done!"

# Deactivate venv
deactivate
