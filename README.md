# 📚 RAGwise

> A local RAG (Retrieval-Augmented Generation) chatbot that lets you ask questions about AI/ML books and get accurate answers powered by **Groq LLM**, with source references and YouTube video links.


## ✨ Features

- 📖 **5 AI/ML Books** — Agentic AI, Deep Learning (Ian Goodfellow), LLM, Machine Learning, NLP
- 🔍 **Semantic Search** — Retrieves the most relevant passages using ChromaDB vector similarity
- ⚡ **Grok LLM Answers** — Fast, accurate answers powered by xAI's Grok API
- 📄 **Source References** — Every answer shows the exact book, page number, and passage
- ▶️ **YouTube Videos** — Automatically finds related YouTube tutorials for every question
- 🎨 **Sleek Dark UI** — Black and dark red Streamlit interface with persistent chat history
- 💾 **Local Embeddings** — HuggingFace embeddings run fully on your machine, no extra cost

---

## 🖥️ Demo

```
User: What is the attention mechanism?

RAGwise: The attention mechanism allows a model to focus on the most
relevant parts of the input sequence when generating each output token.
It computes weighted relationships between all tokens simultaneously,
enabling the model to capture long-range dependencies...

📄 Source: LLM.pdf — Page 112 — Score: 0.1857
▶️ YouTube: "Attention Mechanism in Transformers Explained"
```

---

## 📁 Project Structure

```
RAGwise/
├── data/
│   ├── pdf/
│   │   ├── Agentic_AI/                   # Agentic-AI.pdf
│   │   ├── Deep_Learning/                # Deep+Learning+Ian+Goodfellow.pdf
│   │   ├── Large_Language_Model/         # LLM.pdf
│   │   ├── Machine_Learning/             # machine_learning.pdf
│   │   └── Natural_language_Processing/  # Natural Language Processing-1.pdf
│   └── chroma_db/                        # Auto-generated (run vectorize_book.py)
├── src/
│   ├── main.py                           # Streamlit chatbot UI
│   ├── chatbot_utility.py                # RAG pipeline (retrieve + Groq answer)
│   ├── get_youtube_video.py              # YouTube video search
│   ├── vectorize_book.py                 # PDF → ChromaDB embeddings
│   └── vectorize_script.py              # CLI retrieval tester
├── .env                                  # API keys (never commit this!)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python **3.11.15** (recommended)
- An [xAI Grok API key](https://console.x.ai) — sign up at x.ai

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
pip install anthropic  # xAI Grok uses OpenAI-compatible SDK
pip install openai
```

### 4. Set up your .env file
Create a `.env` file in the project root:
```env
GROK_API_KEY=your_grok_api_key_here
```

Get your API key at 👉 https://console.x.ai

### 5. Add your PDF books
Place your PDF files in the correct folders under `data/pdf/`:
```
data/pdf/Agentic_AI/Agentic-AI.pdf
data/pdf/Deep_Learning/Deep+Learning+Ian+Goodfellow.pdf
data/pdf/Large_Language_Model/LLM.pdf
data/pdf/Machine_Learning/machine_learning.pdf
data/pdf/Natural_language_Processing/Natural Language Processing-1.pdf
```

### 6. Vectorize the books
Run once to process all PDFs and store embeddings in ChromaDB:
```bash
python src/vectorize_book.py
```

> ⏳ This may take several minutes. The Deep Learning book has ~25,000 chunks.

### 7. Run the chatbot
```bash
python -m streamlit run src/main.py
```

Open your browser at `http://localhost:8501` 🚀

---

## 🧪 Testing Retrieval (Optional)

Test raw retrieval from the CLI before running the full chatbot:
```bash
python src/vectorize_script.py
```

Choose a collection and type a query to see the retrieved chunks with scores.

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| streamlit | 1.49.1 | Web UI |
| openai | latest | xAI Grok API (OpenAI-compatible) |
| langchain-community | 0.3.29 | PDF loading, vector utils |
| langchain-chroma | 0.2.5 | ChromaDB integration |
| langchain-huggingface | 0.3.1 | HuggingFace embeddings |
| langchain-text-splitters | 0.3.11 | Document chunking |
| sentence-transformers | 5.1.0 | Embedding model |
| unstructured[pdf] | 0.18.14 | PDF parsing |
| chromadb | latest | Vector database |
| youtube-search-python | 1.6.6 | YouTube search |
| python-dotenv | 1.1.1 | Environment variables |

---

## 🤖 Models Used

| Model | Task | Provider |
|---|---|---|
| `grok-beta` | Answer generation | xAI Grok API |
| `sentence-transformers/all-MiniLM-L6-v2` | Text embeddings | HuggingFace (local) |

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

- **Never commit your `.env` file** — it contains your Grok API key. It is already in `.gitignore`.
- `data/chroma_db/` is excluded from Git (file too large). Regenerate locally by running `vectorize_book.py`.
- PDF files are excluded from Git. Add them manually after cloning.
- The `Cannot set stroke color` warnings during vectorization are harmless.
- Use **Python 3.11.15** for best compatibility. Python 3.13+ causes DLL issues with ChromaDB on Windows.

---

## 📄 License

This project is for educational purposes.

---

<div align="center">
  Built with ❤️ using xAI Grok · LangChain · ChromaDB · HuggingFace · Streamlit
</div>
