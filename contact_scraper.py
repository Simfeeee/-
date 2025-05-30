import requests
from bs4 import BeautifulSoup
import json
import time

TGSTAT_URL = "https://tgstat.ru/channels?query=новости"
CONTACTS_FILE = "contacts.json"
MAX_CONTACTS = 20

def extract_usernames_from_page(html):
    soup = BeautifulSoup(html, "html.parser")
    usernames = []
    for link in soup.select("a.link-muted"):
        href = link.get("href", "")
        if href.startswith("https://t.me/") and "joinchat" not in href:
            username = href.split("https://t.me/")[-1].split("?")[0]
            if username.startswith("@"):
                usernames.append(username)
            else:
                usernames.append("@" + username)
    return list(set(usernames))

def load_existing_contacts():
    try:
        with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_contacts(contacts):
    with open(CONTACTS_FILE, "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)

def append_new_contacts(new_usernames):
    existing = load_existing_contacts()
    existing_usernames = {c["username"] for c in existing}
    added = 0

    for username in new_usernames:
        if username not in existing_usernames:
            existing.append({"username": username})
            added += 1
            if added >= MAX_CONTACTS:
                break

    save_contacts(existing)
    return added

def run_scraper():
    try:
        r = requests.get(TGSTAT_URL, timeout=10)
        usernames = extract_usernames_from_page(r.text)
        added_count = append_new_contacts(usernames)
        print(f"✅ Добавлено {added_count} новых контактов.")
    except Exception as e:
        print(f"❌ Ошибка парсинга: {e}")

if __name__ == "__main__":
    run_scraper()
