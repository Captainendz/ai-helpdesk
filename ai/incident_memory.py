import json
import os
from datetime import datetime

MEMORY_FILE = "data/incident_memory.json"


def load_memory():

    # ---------- Create file if missing ----------
    if not os.path.exists(MEMORY_FILE):

        with open(MEMORY_FILE, "w") as file:

            json.dump([], file)

    # ---------- Load memory ----------
    with open(MEMORY_FILE, "r") as file:

        return json.load(file)


def save_incident(
    user,
    device,
    issue,
    issue_types,
    resolution,
    knowledge_sources
):

    memory = load_memory()

    incident = {

        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "user": user,

        "device": device,

        "issue": issue,

        "issue_types": issue_types,

        "resolution": resolution,

        "knowledge_sources": knowledge_sources
    }

    memory.append(incident)

    with open(MEMORY_FILE, "w") as file:

        json.dump(memory, file, indent=4)


def get_user_history(user):

    memory = load_memory()

    history = []

    for incident in memory:

        if incident["user"] == user:

            history.append(incident)

    return history