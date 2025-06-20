# Whatsapp_Read-BOT

# 📲 WhatsApp Unread Message Extractor – Automation Bot

This Python automation script extracts unread messages from WhatsApp Web using Selenium. It works by using a saved Chrome user session to skip QR logins after the first time and filters chats by unread messages using the green bubble count. The script reads each unread chat and saves details like contact name/number, message, timestamp, and unread count into a CSV file.

---

## ✅ Features

- Automatically opens WhatsApp Web
- Uses previously logged-in Chrome session (no repeated QR scans)
- Clicks on the **Unread filter** to view only unread chats
- Extracts:
  - Contact Name or Number
  - Unread Message Content
  - Timestamp
  - Number of Unread Messages
- Saves all data to a file: `messages_with_unread_counts.csv`

---

## 🛠 Requirements

- Python 3.x
- Google Chrome (64-bit)
- ChromeDriver matching your Chrome version

### Python Libraries

pip install selenium pandas

#🔧 Setup Instructions
### Step 1: Download and Setup ChromeDriver
### Go to https://chromedriver.chromium.org/downloads

Download the version that matches your installed Google Chrome

Extract it and copy the path to chromedriver.exe


# Step 2: Login to WhatsApp (Only Once)
Open Chrome manually like this:

### chrome.exe --user-data-dir="C:\path\to\your\chrome\profile"
### Navigate to: https://web.whatsapp.com

Scan the QR code to log in

Close the browser — your login will be saved for future use

# Step 3: Update Script Paths
Edit these two lines in your script to match your system:

chrome_driver_path = r"Path\to\chromedriver.exe"
user_data_path = r"Path\to\Chrome\User Data\Profile"

# ▶️ How to Run the Script

### python whatsapp_unread_extractor.py


# The script will:
Open WhatsApp Web
Apply the "Unread" filter
Go through each unread chat
Extract message data
Save everything to messages_with_unread_counts.csv




