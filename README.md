# 📚 AI Research Assistant (RAG-Based System)

An AI-powered research assistant that enables users to upload PDFs or fetch research papers from arXiv and ask questions.  
The system uses Retrieval-Augmented Generation (RAG) to provide accurate, context-based answers.

---

## 🚀 Features

- 📄 Upload and analyze PDF research papers  
- 🔍 Search research papers from arXiv  
- 🤖 Ask questions and get AI-generated answers  
- 🧠 Semantic search using embeddings + FAISS  
- 📑 Summarization and explanation of research content  
- ⬇️ Download research papers directly  

---

## 🧠 How it Works

1. Extracts text from PDFs using PyMuPDF  
2. Splits text into smaller chunks  
3. Converts chunks into embeddings using Sentence Transformers  
4. Stores embeddings in FAISS for fast similarity search  
5. Retrieves relevant context based on user query  
6. Uses Gemini API to generate structured answers  

---

## 🛠 Tech Stack

- Python  
- Flask  
- FAISS  
- Sentence Transformers  
- Google Gemini API  
- PyMuPDF  
- JavaScript (Frontend)  

---

## ⚙️ Setup Instructions

### 1. Clone the repository

git clone https://github.com/bhavya3966/Research-Paper-Assistant-RAG-Based-.git
cd Research-Paper-Assistant-RAG-Based

###  2. Create virtual environment

python -m venv venv
venv\Scripts\activate   # Windows

### 3. Install dependencies

pip install -r requirements.txt

### 4. Add API key

Add Your Api Key iin .env File.

"" GEMINI_API_KEY=your_api_key_here ""

### 5. Run the application

python app.py



