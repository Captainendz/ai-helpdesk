import requests
import os
from dotenv import load_dotenv

load_dotenv()

GLPI_URL = os.getenv("GLPI_URL")
USER_TOKEN = os.getenv("USER_TOKEN")
APP_TOKEN = os.getenv("APP_TOKEN")


def get_headers():
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


def create_ticket(title, content, user_id=None):

    headers = get_headers()

    ticket_input = {
        "name": title,
        "content": content
    }

    # ---------- Attach requester ----------
    if user_id:
        ticket_input["_users_id_requester"] = user_id

    ticket_data = {
        "input": ticket_input
    }

    response = requests.post(
        f"{GLPI_URL}/Ticket",
        headers=headers,
        json=ticket_data
    )

    return response.json()