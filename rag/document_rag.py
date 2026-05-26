import faiss
import pickle
import numpy as np

from sentence_transformers import SentenceTransformer

# ---------- Load embedding model ----------
model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------- Load FAISS index ----------
index = faiss.read_index("data/document_index.faiss")

# ---------- Load chunk metadata ----------
with open("data/document_chunks.pkl", "rb") as file:

    chunks = pickle.load(file)


def search_documents(query):

    # ---------- Convert query to embedding ----------
    query_vector = model.encode([query])

    # ---------- Convert to numpy ----------
    query_vector = np.array(query_vector).astype("float32")

    # ---------- Search Top 3 Matches ----------
    distances, indices = index.search(query_vector, 3)

    results = []

    # ---------- Process Results ----------
    for i in range(len(indices[0])):

        chunk_index = indices[0][i]

        chunk_distance = distances[0][i]

        print(
            f"Match {i+1} Distance:",
            chunk_distance
        )

        # ---------- Similarity Threshold ----------
        if chunk_distance < 1.5:

            matched_chunk = chunks[chunk_index]

            results.append({

                "source": matched_chunk["source"],

                "content": matched_chunk["chunk"],

                "distance": float(chunk_distance)
            })

    return results