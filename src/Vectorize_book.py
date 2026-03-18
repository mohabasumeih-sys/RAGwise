import os
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.vectorstores.utils import filter_complex_metadata

load_dotenv()

# ── CONFIG ────────────────────────────────────────────────────────────────────
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHROMA_DIR      = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")
CHUNK_SIZE      = 1000  # larger = more context per chunk
CHUNK_OVERLAP   = 150   # overlap keeps context between chunks
MIN_CHUNK_LEN   = 50    # skip chunks shorter than this (headers, single words)

# Map each PDF to a collection name (one collection per topic)
BOOK_MAP = {
    os.path.join("data", "pdf", "Agentic_AI",                "Agentic-AI.pdf"):                     "agentic_ai",
    os.path.join("data", "pdf", "Deep_Learning",              "Deep+Learning+Ian+Goodfellow.pdf"):   "deep_learning",
    os.path.join("data", "pdf", "Large_Language_Model",       "LLM.pdf"):                            "large_language_model",
    os.path.join("data", "pdf", "Machine_Learning",           "machine_learning.pdf"):               "machine_learning",
    os.path.join("data", "pdf", "Natural_language_Processing","Natural Language Processing-1.pdf"):  "nlp",
}
# ─────────────────────────────────────────────────────────────────────────────


def load_and_split(pdf_path: str):
    """Load a PDF and split it into clean, deduplicated chunks."""
    print(f"  Loading : {pdf_path}")
    loader = UnstructuredPDFLoader(pdf_path, mode="elements")
    docs   = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(docs)

    # Remove chunks that are too short (single words, headers, page numbers)
    chunks = [c for c in chunks if len(c.page_content.strip()) >= MIN_CHUNK_LEN]

    # Remove duplicate chunks (same content appearing twice)
    seen   = set()
    unique = []
    for c in chunks:
        text = c.page_content.strip()
        if text not in seen:
            seen.add(text)
            unique.append(c)
    chunks = unique

    print(f"  Chunks  : {len(chunks)} (after dedup + min-length filter)")
    return chunks


def vectorize_book(pdf_path: str, collection_name: str):
    """Embed chunks of one PDF and persist them in a ChromaDB collection."""
    print(f"\n{'='*60}")
    print(f"Collection : {collection_name}")

    # Resolve path relative to project root (one level above src/)
    project_root = os.path.join(os.path.dirname(__file__), "..")
    full_path    = os.path.join(project_root, pdf_path)

    if not os.path.exists(full_path):
        print(f"  WARNING  : file not found → {full_path}")
        return

    chunks     = load_and_split(full_path)
    chunks     = filter_complex_metadata(chunks)  # strip nested dicts ChromaDB can't store
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    # Delete existing collection first to avoid duplicate data on re-runs
    vectorstore = Chroma(
        collection_name   = collection_name,
        embedding_function= embeddings,
        persist_directory = CHROMA_DIR,
    )
    vectorstore.delete_collection()

    vectorstore = Chroma.from_documents(
        documents         = chunks,
        embedding         = embeddings,
        collection_name   = collection_name,
        persist_directory = CHROMA_DIR,
    )
    print(f"  Saved    : {len(chunks)} chunks → {CHROMA_DIR}/{collection_name}")
    return vectorstore


def main():
    print("RAGwise — vectorize_book.py")
    print(f"Chroma DB : {CHROMA_DIR}")
    print(f"Embedding : {EMBEDDING_MODEL}\n")

    for pdf_path, collection_name in BOOK_MAP.items():
        vectorize_book(pdf_path, collection_name)

    print("\n✅ All books vectorized successfully!")


if __name__ == "__main__":
    main()