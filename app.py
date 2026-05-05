from flask import Flask, request, jsonify, render_template
import os

from services.pdf_service import extract_text
from utils.chunking import chunk_text
from services.embedding_service import generate_embeddings, model as embed_model
from services.retrieval_service import create_faiss_index, search
from services.llm_service import generate_answer
from services.arxiv_service import search_arxiv, download_pdf

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_pdf():
    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    text = extract_text(filepath)
    chunks = chunk_text(text)
    embeddings = generate_embeddings(chunks)

    create_faiss_index(embeddings, chunks, file.filename)

    return jsonify({"message": f"{file.filename} processed"})


@app.route('/ask', methods=['POST'])
def ask():
    query = request.json.get('query', '')

    query_embedding = embed_model.encode([query])
    context_chunks = search(query_embedding, k=5)

    if not context_chunks:
        return jsonify({"answer": "Upload or load a document first."})

    answer = generate_answer(query, context_chunks)

    return jsonify({"answer": answer})


@app.route('/search_arxiv', methods=['POST'])
def search_papers():
    data = request.json

    query = data.get('query', '').strip()

    print("DEBUG QUERY:", query)   # <-- ADD THIS

    if not query:
        return jsonify({"error": "Query is empty"}), 400

    papers = search_arxiv(query)

    return jsonify({"papers": papers})

@app.route('/load_arxiv', methods=['POST'])
def load_arxiv():
    data = request.json

    pdf_url = data.get('pdf_url')
    title = data.get('title')

    filename = title.replace(" ", "_")[:50] + ".pdf"

    filepath = download_pdf(pdf_url, filename)

    text = extract_text(filepath)
    chunks = chunk_text(text)
    embeddings = generate_embeddings(chunks)

    create_faiss_index(embeddings, chunks, filename)

    return jsonify({"message": f"{title} loaded"})


if __name__ == '__main__':
    app.run(debug=True)