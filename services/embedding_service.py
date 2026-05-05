# services/embedding_service.py

from sentence_transformers import SentenceTransformer
import numpy as np

# Load embedding model once
model = SentenceTransformer('all-MiniLM-L6-v2')


def generate_embeddings(chunks):
    """
    Convert list of text chunks into vector embeddings
    """
    if not chunks:
        return np.array([])

    embeddings = model.encode(
        chunks,
        show_progress_bar=False,
        convert_to_numpy=True,
        normalize_embeddings=True   # improves similarity search
    )

    return embeddings