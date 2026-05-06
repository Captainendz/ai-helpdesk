import requests
import os
from dotenv import load_dotenv

load_dotenv()

GLPI_URL = os.getenv("GLPI_URL")
USER_TOKEN = os.getenv("USER_TOKEN")
APP_TOKEN = os.getenv("APP_TOKEN")


def create_ticket(title, content):
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

    ticket_data = {
        "input": {
            "name": title,
            "content": content
        }
    }

    response = requests.post(
        f"{GLPI_URL}/Ticket",
        headers=headers,
        json=ticket_data
    )

    return response.json()