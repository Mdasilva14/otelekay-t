import json
from datetime import datetime
import os

USERS_JSON = "users.json"
VISITORS_JSON = "visitors.json"


def load_users():
    try:
        with open(USERS_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_users(users):
    with open(USERS_JSON, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

def add_user(new_user):
    filename = 'users.json'
    users = []

    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                users = []

    exists = any(u['email'] == new_user['email'] or u['username'] == new_user['username'] for u in users)

    if not exists:
        users.append(new_user)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=4)

def load_visitors():
    try:
        with open(VISITORS_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_visitors(visitors):
    with open(VISITORS_JSON, "w", encoding="utf-8") as f:
        json.dump(visitors, f, ensure_ascii=False, indent=4)

def add_visitor(visitor_dict):
    visitors = load_visitors()
    visitors.append(visitor_dict)
    save_visitors(visitors)
