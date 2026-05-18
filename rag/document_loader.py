import os


def detect_category(filename):

    name = filename.lower()

    if "vpn" in name:
        return "vpn"

    elif "email" in name:
        return "email"

    elif "printer" in name:
        return "printer"

    elif "login" in name:
        return "authentication"

    elif "wifi" in name or "network" in name:
        return "network"

    elif "performance" in name or "slow" in name:
        return "performance"

    else:
        return "general"


def load_documents():

    documents = []

    # ---------- Project Root ----------
    BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    # ---------- Documents Folder ----------
    folder = os.path.join(
        BASE_DIR,
        "data",
        "documents"
    )

    # ---------- Load TXT Files ----------
    for filename in os.listdir(folder):

        filepath = os.path.join(folder, filename)

        if filename.endswith(".txt"):

            with open(filepath, "r", encoding="utf-8") as file:

                content = file.read()

                documents.append({

                    "filename": filename,

                    "category": detect_category(filename),

                    "content": content
                })

    return documents


# ---------- Test ----------
if __name__ == "__main__":

    docs = load_documents()

    for doc in docs:

        print("\n------------------")
        print("File:", doc["filename"])
        print("Category:", doc["category"])