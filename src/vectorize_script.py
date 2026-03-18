import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()

# ── CONFIG ────────────────────────────────────────────────────────────────────
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHROMA_DIR      = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")
TOP_K           = 5   # number of chunks to retrieve per query

# All available collections (must match names used in vectorize_book.py)
COLLECTIONS = {
    "1":   "agentic_ai",
    "2":   "deep_learning",
    "3":   "large_language_model",  # fixed: was "large_language_Model"
    "4":   "machine_learning",
    "5":   "nlp",                   # fixed: was "Natural_language_Processing"
    "all": "all",
}
# ─────────────────────────────────────────────────────────────────────────────


def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def load_vectorstore(collection_name: str, embeddings):
    """Load an existing ChromaDB collection."""
    return Chroma(
        collection_name   = collection_name,
        embedding_function= embeddings,
        persist_directory = CHROMA_DIR,
    )


def retrieve(query: str, collection_name: str = "all", top_k: int = TOP_K):
    """
    Retrieve the top-k most relevant chunks for a query.

    Parameters
    ----------
    query           : the user question / search string
    collection_name : one of COLLECTIONS values, or 'all' to merge results
    top_k           : number of results to return

    Returns
    -------
    list of (Document, score) tuples, sorted by relevance
    """
    embeddings = get_embeddings()

    if collection_name == "all":
        # Search every collection and merge results
        all_results = []
        for name in COLLECTIONS.values():
            if name == "all":
                continue
            try:
                vs      = load_vectorstore(name, embeddings)
                results = vs.similarity_search_with_score(query, k=top_k)
                for doc, score in results:
                    doc.metadata["collection"] = name
                all_results.extend(results)
            except Exception as e:
                print(f"  Warning: could not search '{name}': {e}")

        # Sort by score (lower = more similar for cosine distance)
        all_results.sort(key=lambda x: x[1])
        return all_results[:top_k]

    else:
        vs      = load_vectorstore(collection_name, embeddings)
        results = vs.similarity_search_with_score(query, k=top_k)
        for doc, score in results:
            doc.metadata["collection"] = collection_name
        return results


def format_results(results):
    """Pretty-print retrieved chunks."""
    if not results:
        print("No results found.")
        return

    for i, (doc, score) in enumerate(results, 1):
        collection = doc.metadata.get("collection", "unknown")
        source     = doc.metadata.get("source", "unknown")
        page       = doc.metadata.get("page_number", "?")
        print(f"\n{'─'*60}")
        print(f"[{i}] Collection : {collection}  |  Score : {score:.4f}")
        print(f"     Source     : {os.path.basename(source)}  |  Page : {page}")
        print(f"     Content    :\n{doc.page_content[:400]}{'...' if len(doc.page_content) > 400 else ''}")


def interactive_search():
    """Simple CLI to test retrieval interactively."""
    print("RAGwise — vectorize_script.py  (retrieval tester)")
    print("="*60)
    print("Collections:")
    for key, name in COLLECTIONS.items():
        print(f"  {key} → {name}")

    collection_key = input("\nChoose collection (number or 'all') [all]: ").strip() or "all"
    collection     = COLLECTIONS.get(collection_key, "all")

    print(f"\nSearching in: {collection}  |  top_k={TOP_K}")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("Query: ").strip()
        if query.lower() in ("exit", "quit", "q"):
            break
        if not query:
            continue

        results = retrieve(query, collection_name=collection, top_k=TOP_K)
        format_results(results)
        print()


# ── Public helper used by your chatbot / Streamlit app ───────────────────────

def get_relevant_chunks(query: str, collection_name: str = "all", top_k: int = TOP_K):
    """
    Convenience function for the RAG pipeline.

    Usage in your chatbot:
        from src.vectorize_script import get_relevant_chunks
        chunks = get_relevant_chunks("What is attention mechanism?", "large_language_model")
        context = "\\n\\n".join([doc.page_content for doc, _ in chunks])
    """
    return retrieve(query, collection_name=collection_name, top_k=top_k)


if __name__ == "__main__":
    interactive_search()