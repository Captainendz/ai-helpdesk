import requests
import os
from dotenv import load_dotenv

load_dotenv()

GLPI_URL = os.getenv("GLPI_URL")
USER_TOKEN = os.getenv("USER_TOKEN")
APP_TOKEN = os.getenv("APP_TOKEN")


def get_session_headers():
    headers = {
        "Authorization": f"user_token {USER_TOKEN}",
        "App-Token": APP_TOKEN,
        "Content-Type": "application/json"
    }

    session_response = requests.get(
        f"{GLPI_URL}/initSession",
        headers=headers
    )

    session_token = session_response.json()["session_token"]

    headers["Session-Token"] = session_token

    return headers


def find_user(username):
    headers = get_session_headers()

    response = requests.get(
        f"{GLPI_URL}/User",
        headers=headers
    )

    users = response.json()

    for user in users:
        if user["name"].lower() == username.lower():
            return user

    return None


user = find_user("normal")

if user:
    print("User found")
    print("ID:", user["id"])
    print("Username:", user["name"])
else:
    print("User not found")