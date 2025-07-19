import os
import requests
from notion_client import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print(f"Loaded vars:\nNOTION_TOKEN = {NOTION_TOKEN}\nDATABASE_ID = {DATABASE_ID}\nTELEGRAM_TOKEN = {TELEGRAM_TOKEN}\nCHAT_ID = {CHAT_ID}")

notion = Client(auth=NOTION_TOKEN)

def get_incomplete_tasks():
    response = notion.databases.query(
        **{
            "database_id": DATABASE_ID,
            "filter": {
                "property": "Done",
                "checkbox": {
                    "equals": False
                }
            }
        }
    )
    tasks = []
    for result in response.get("results", []):
        title_property = result["properties"].get("Name")
        if title_property and title_property["title"]:
            tasks.append(title_property["title"][0]["plain_text"])
    return tasks

def send_telegram_message(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

def main():
    tasks = get_incomplete_tasks()
    if tasks:
        message = "🔔 You have incomplete tasks:\n" + "\n".join(f"• {t}" for t in tasks)
    else:
        message = "✅ All tasks are completed!"
    send_telegram_message(message)

if __name__ == "__main__":
    main()
