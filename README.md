# RAGwise

> A local RAG (Retrieval-Augmented Generation) chatbot that lets you ask questions about AI/ML books and get answers with source references and YouTube video links — all running 100% free and offline.


## ✨ Features

- 📖 **5 AI/ML Books** — Agentic AI, Deep Learning (Ian Goodfellow), LLM, Machine Learning, NLP
- 🔍 **Semantic Search** — Retrieves the most relevant passages using vector similarity
- 🤖 **Local AI Answers** — Generates answers using a free HuggingFace QA model, no API key needed
- 📄 **Source References** — Every answer shows the exact book, page number, and passage
- ▶️ **YouTube Videos** — Automatically finds related YouTube tutorials for every question
- 🎨 **Sleek Dark UI** — Black and dark red Streamlit interface with persistent chat history
- 💾 **Fully Local** — All embeddings and vector storage run on your machine

---

## 🖥️ Demo

```
User: What is the attention mechanism?

RAGwise: Attention is a mechanism that helps the model incorporate context
as it's processing a specific token. It allows the model to attend to
certain parts of sequences that relate more or less to one another...

📄 Source: LLM.pdf — Page 112
▶️ YouTube: "Attention Mechanism in Transformers Explained" — Andrej Karpathy
```

---

## 📁 Project Structure

```
RAGwise/
├── data/
│   ├── pdf/
│   │   ├── Agentic_AI/               # Agentic-AI.pdf
│   │   ├── Deep_Learning/            # Deep+Learning+Ian+Goodfellow.pdf
│   │   ├── Large_Language_Model/     # LLM.pdf
│   │   ├── Machine_Learning/         # machine_learning.pdf
│   │   └── Natural_language_Processing/ # Natural Language Processing-1.pdf
│   └── chroma_db/                    # Auto-generated (run vectorize_book.py)
├── src/
│   ├── main.py                       # Streamlit chatbot UI
│   ├── chatbot_utility.py            # RAG pipeline (retrieve + answer)
│   ├── get_youtube_video.py          # YouTube video search
│   ├── vectorize_book.py             # PDF → ChromaDB embeddings
│   └── vectorize_script.py          # CLI retrieval tester
├── .env                              # Environment variables
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python **3.11.15** (recommended — other versions may have compatibility issues)
- Git

### 1. Clone the repository
```bash
git clone https://github.com/your-username/RAGwise.git
cd RAGwise
```

### 2. Create a virtual environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your PDF books
Place your PDF files in the correct folders under `data/pdf/`:

```
data/pdf/Agentic_AI/Agentic-AI.pdf
data/pdf/Deep_Learning/Deep+Learning+Ian+Goodfellow.pdf
data/pdf/Large_Language_Model/LLM.pdf
data/pdf/Machine_Learning/machine_learning.pdf
data/pdf/Natural_language_Processing/Natural Language Processing-1.pdf
```

### 5. Vectorize the books
This step processes all PDFs and stores embeddings in ChromaDB. Run it once:
```bash
python src/vectorize_book.py
```

> ⏳ This may take several minutes depending on book size. Deep Learning (Ian Goodfellow) has ~25,000 chunks.

### 6. Run the chatbot
```bash
python -m streamlit run src/main.py
```

Open your browser at `http://localhost:8501`

---

## 🧪 Testing Retrieval (Optional)

Before running the full chatbot, you can test retrieval from the CLI:
```bash
python src/vectorize_script.py
```

Then choose a collection and type a query to see the raw retrieved chunks.

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| streamlit | 1.49.1 | Web UI |
| langchain-community | 0.3.29 | PDF loading, vector utils |
| langchain-chroma | 0.2.5 | ChromaDB integration |
| langchain-huggingface | 0.3.1 | HuggingFace embeddings |
| langchain-text-splitters | 0.3.11 | Document chunking |
| sentence-transformers | 5.1.0 | Embedding model |
| transformers | 4.56.0 | QA model |
| unstructured[pdf] | 0.18.14 | PDF parsing |
| chromadb | latest | Vector database |
| youtube-search-python | 1.6.6 | YouTube search |
| python-dotenv | 1.1.1 | Environment variables |

---

## 🤖 Models Used

| Model | Task | Source |
|---|---|---|
| `sentence-transformers/all-MiniLM-L6-v2` | Text embeddings | HuggingFace |
| `deepset/roberta-base-squad2` | Question answering | HuggingFace |

Both models are free, local, and require no API key.

---

## 🗂️ Collections

| Collection Name | Book |
|---|---|
| `agentic_ai` | Agentic AI |
| `deep_learning` | Deep Learning — Ian Goodfellow |
| `large_language_model` | Build a Large Language Model |
| `machine_learning` | Machine Learning |
| `nlp` | Natural Language Processing |

---

## ⚠️ Notes

- `data/chroma_db/` is excluded from Git (too large). Regenerate it locally by running `vectorize_book.py`.
- PDF files are also excluded. Add them manually after cloning.
- The `Cannot set stroke color` warnings during vectorization are harmless — they come from the PDF renderer and don't affect text extraction.
- For best compatibility use **Python 3.11.15**. Python 3.13+ may cause DLL issues with ChromaDB on Windows.

---

## 📄 License

This project is for educational purposes.

---

<div align="center">
  Built with ❤️ using LangChain · ChromaDB · HuggingFace · Streamlit
</div>
