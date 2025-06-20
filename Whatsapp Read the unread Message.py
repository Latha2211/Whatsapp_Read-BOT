import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize WebDriver
chrome_driver_path = r"C:\Users\INC\OneDrive - \Documents\AI bot\chromedriver\chromedriver-win64\chromedriver.exe"
user_data_path = r"C:\Users\INC\OneDrive - \Documents\AI bot\Profile 2"

chrome_options = Options()
chrome_options.add_argument(f"user-data-dir={user_data_path}")
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 120)

try:
    # Click on "Unread" filter
    unread_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='unread-filter']/div/div")))
    unread_button.click()
    print("Clicked on 'Unread' filter.")
    time.sleep(3)  # Allow chats to load

    # Find all unread chats and extract unread counts
    unread_chats = driver.find_elements(By.XPATH, "//*[@id='pane-side']/div/div/div/div")
    unread_chat_counts = {}

    for chat in unread_chats:
        try:
            # ⬇️ Extract title/contact name using the specified XPath inside each chat element
            try:
                title_element = chat.find_element(By.XPATH, ".//div[@class='_ak8q']/div/div/span")  # Relative version
                contact_name = title_element.text.strip()
            except:
                contact_name = chat.text.strip()

            if not contact_name:
                continue

            contact_number = ''.join(filter(str.isdigit, contact_name.split('\n')[0]))
            if not contact_number:
                contact_number = contact_name.split('\n')[0]

            # Extract unread message count using the provided XPath
            try:
                unread_count_element = chat.find_elements(By.XPATH, ".//div[2]/div[2]/div[2]/span[1]/div/span")
                unread_count_text = unread_count_element[0].text.strip() if unread_count_element else "0"
                unread_count = int(unread_count_text) if unread_count_text.isdigit() else 0
            except:
                unread_count = 0

            unread_chat_counts[contact_number] = unread_count

        except Exception as e:
            print(f"Error extracting unread count for chat: {e}")

    chat_data = []

    for chat in unread_chats:
        try:
            # Re-extract the contact title for each chat
            try:
                title_element = chat.find_element(By.XPATH, ".//div[@class='_ak8q']/div/div/span")
                contact_name = title_element.text.strip()
            except:
                contact_name = chat.text.strip()

            if not contact_name:
                continue

            contact_number = ''.join(filter(str.isdigit, contact_name.split('\n')[0]))
            if not contact_number:
                contact_number = contact_name.split('\n')[0]

            unread_count = unread_chat_counts.get(contact_number, 0)

            chat.click()
            time.sleep(3)

            message_elements = wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//div[contains(@class, 'message-in')]")
          
          
                )
            )

            if not message_elements:
                print(f"No unread messages found for {contact_number}")
                continue

            for message_element in message_elements:
                try:
                    message_text_element = message_element.find_element(By.XPATH, ".//div[@class='copyable-text']")
                    message_text = message_text_element.get_attribute("data-pre-plain-text") or ""
                    message_content = message_text_element.text.strip() if message_text_element.text else "No message found"

                    if message_text:
                        timestamp = message_text.split(']')[0][1:].strip()
                        timestamp = ' '.join(timestamp.split(',')[0].split()[:2]).upper()
                    else:
                        timestamp_element = message_element.find_element(By.XPATH, ".//div[contains(@class, 'copyable-text')]/span[last()]")
                        timestamp = timestamp_element.text.strip() if timestamp_element else "No timestamp found"

                    chat_data.append({
                        "Contact": contact_number,
                        "Name": contact_name,
                        "Message": message_content,
                        "Timestamp": timestamp,
                        "Unread_Count": unread_count
                    })

                    print(f"Extracted: {contact_name} ({contact_number}) | {message_content} | {timestamp} | Unread Count: {unread_count}")

                except Exception as e:
                    print(f"Error extracting message data for {contact_number}: {e}")

            driver.find_element(By.XPATH, "//*[@id='app']").click()
            time.sleep(1)

        except Exception as e:
            print("Error extracting chat data:", e)

    df = pd.DataFrame(chat_data)
    df.to_csv("messages_with_unread_counts.csv", index=False)
    print("Messages saved to messages_with_unread_counts.csv")
    print("\nSample of saved data:")
    print(df.head())

except Exception as e:
    print("Error:", e)

input("Press Enter to exit the script and close the browser...")
