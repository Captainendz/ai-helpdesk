import os


def load_documents(folder="documents"):

    documents = []

    for filename in os.listdir(folder):

        filepath = os.path.join(folder, filename)

        if filename.endswith(".txt"):

            with open(filepath, "r", encoding="utf-8") as file:

                content = file.read()

                documents.append({
                    "filename": filename,
                    "content": content
                })

    return documents


# ---------- Test ----------
if __name__ == "__main__":

    docs = load_documents()

    for doc in docs:

        print("\nDOCUMENT:")
        print(doc["filename"])

        print("\nCONTENT:")
        print(doc["content"])