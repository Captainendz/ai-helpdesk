import faiss
import numpy as np
import pickle

from sentence_transformers import SentenceTransformer

from document_loader import load_documents
from chunker import chunk_text

# ---------- Load embedding model ----------
model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------- Load documents ----------
documents = load_documents()

all_chunks = []

# ---------- Chunk all documents ----------
for doc in documents:

    chunks = chunk_text(doc["content"])

    for chunk in chunks:

        all_chunks.append({
            "source": doc["filename"],
            "chunk": chunk
        })

# ---------- Extract chunk text ----------
chunk_texts = [item["chunk"] for item in all_chunks]

# ---------- Generate embeddings ----------
embeddings = model.encode(chunk_texts)

# ---------- Convert to numpy ----------
embedding_matrix = np.array(embeddings).astype("float32")

# ---------- Create FAISS index ----------
dimension = embedding_matrix.shape[1]

index = faiss.IndexFlatL2(dimension)

# ---------- Store embeddings ----------
index.add(embedding_matrix)

# ---------- Save FAISS index ----------
faiss.write_index(index, "document_index.faiss")

# ---------- Save chunk metadata ----------
with open("document_chunks.pkl", "wb") as file:

    pickle.dump(all_chunks, file)

print("Document vector database created successfully.")
print("Total chunks stored:", index.ntotal)