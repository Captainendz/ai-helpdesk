import faiss
import pickle
import numpy as np

from sentence_transformers import SentenceTransformer

# ---------- Load embedding model ----------
model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------- Load FAISS index ----------
index = faiss.read_index("document_index.faiss")

# ---------- Load chunk metadata ----------
with open("document_chunks.pkl", "rb") as file:

    chunks = pickle.load(file)


def search_documents(query):

    # ---------- Convert query to embedding ----------
    query_vector = model.encode([query])

    # ---------- Convert to numpy ----------
    query_vector = np.array(query_vector).astype("float32")

    # ---------- Search FAISS ----------
    distances, indices = index.search(query_vector, 1)

    # ---------- Best match ----------
    best_index = indices[0][0]

    best_distance = distances[0][0]

    print("Best vector distance:", best_distance)

    # ---------- Similarity threshold ----------
    if best_distance < 1.5:

        best_chunk = chunks[best_index]

        return {
            "source": best_chunk["source"],
            "content": best_chunk["chunk"]
        }

    return None