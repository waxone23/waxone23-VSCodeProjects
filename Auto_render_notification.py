import os
import time
import requests

# --- CONFIGURATION ---
TOKEN = "YOUR_BOT_TOKEN_HERE"
CHAT_ID = "YOUR_CHAT_ID_HERE"
WATCH_FOLDER = r"C:\Path\To\Your\Render\Folder"


def send_telegram_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Failed to send message: {e}")


def monitor_renders():
    print(f"Monitoring folder: {WATCH_FOLDER}")
    # Get initial list of files
    before = dict([(f, None) for f in os.listdir(WATCH_FOLDER)])

    while True:
        time.sleep(5)  # Check every 5 seconds
        after = dict([(f, None) for f in os.listdir(WATCH_FOLDER)])
        added = [f for f in after if not f in before]

        if added:
            for filename in added:
                # Wait for the file to finish writing (size stops changing)
                file_path = os.path.join(WATCH_FOLDER, filename)
                last_size = -1
                while True:
                    current_size = os.path.getsize(file_path)
                    if current_size == last_size:
                        break
                    last_size = current_size
                    time.sleep(2)

                print(f"Render Finished: {filename}")
                send_telegram_msg(f"✅ Render Complete: {filename}")

        before = after


if __name__ == "__main__":
    monitor_renders()
