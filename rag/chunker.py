from rag.document_loader import load_documents


def chunk_text(text, chunk_size=120):

    chunks = []

    for i in range(0, len(text), chunk_size):

        chunk = text[i:i + chunk_size]

        chunks.append(chunk)

    return chunks


# ---------- Test ----------
if __name__ == "__main__":

    documents = load_documents()

    all_chunks = []

    for doc in documents:

        chunks = chunk_text(doc["content"])

        for chunk in chunks:

            all_chunks.append({
                "source": doc["filename"],
                "chunk": chunk
            })

    # ---------- Display chunks ----------
    for i, item in enumerate(all_chunks):

        print("\n-------------------")
        print("Chunk Number:", i + 1)

        print("Source:", item["source"])

        print("\nChunk Content:")
        print(item["chunk"])