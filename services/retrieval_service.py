# services/retrieval_service.py

import faiss

index = None
stored_data = []


def create_faiss_index(embeddings, chunks, source_name="document"):
    global index, stored_data

    dim = embeddings.shape[1]

    if index is None:
        index = faiss.IndexFlatL2(dim)

    index.add(embeddings)

    for chunk in chunks:
        stored_data.append({
            "text": chunk,
            "source": source_name
        })


def search(query_embedding, k=5):
    global index, stored_data

    if index is None:
        return []

    distances, indices = index.search(query_embedding, k)

    results = []
    for i in indices[0]:
        if i < len(stored_data):
            results.append(stored_data[i])

    return results