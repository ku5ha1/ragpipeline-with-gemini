from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from utils import collection

# Load the embedding model
embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Initialize FAISS index
dimension = 384  # Dimension of the embeddings
faiss_index = faiss.IndexFlatL2(dimension)

# Generate embeddings
def generate_embedding(text: str):
    return embedding_model.encode(text)

# Add embeddings to FAISS index
def add_to_faiss(embedding: np.ndarray, prompt: str, task_type: str, response: str):
    faiss_index.add(np.array([embedding]))
    collection.insert_one({"prompt": prompt, "embedding": embedding.tolist(), "task_type": task_type, "response": response})

# Search for similar vectors in FAISS index
def search_in_faiss(embedding: np.ndarray, k: int = 1):
    distances, indices = faiss_index.search(np.array([embedding]), k)
    return distances, indices
