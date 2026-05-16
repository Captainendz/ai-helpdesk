import os


def load_documents():

    documents = []

    # ---------- Documents folder ----------
    folder = "data/documents"

    # ---------- Read all text files ----------
    for filename in os.listdir(folder):

        if filename.endswith(".txt"):

            filepath = os.path.join(folder, filename)

            with open(filepath, "r", encoding="utf-8") as file:

                content = file.read()

                documents.append({
                    "filename": filename,
                    "content": content
                })

    return documents