import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from transformers import pipeline

load_dotenv()

# ── CONFIG ────────────────────────────────────────────────────────────────────
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
QA_MODEL        = "deepset/roberta-base-squad2"   # free, local QA model
CHROMA_DIR      = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")
TOP_K           = 5

COLLECTIONS = {
    "All Books":              "all",
    "Agentic AI":             "agentic_ai",
    "Deep Learning":          "deep_learning",
    "Large Language Model":   "large_language_model",
    "Machine Learning":       "machine_learning",
    "NLP":                    "nlp",
}
# ─────────────────────────────────────────────────────────────────────────────

# Cache embeddings and QA pipeline so they load only once per session
_embeddings = None
_qa_pipeline = None


def get_embeddings():
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return _embeddings


def get_qa_pipeline():
    global _qa_pipeline
    if _qa_pipeline is None:
        _qa_pipeline = pipeline("question-answering", model=QA_MODEL)
    return _qa_pipeline


def retrieve_chunks(query: str, collection_name: str = "all", top_k: int = TOP_K):
    """Retrieve the most relevant chunks from ChromaDB."""
    embeddings = get_embeddings()

    if collection_name == "all":
        all_results = []
        for name in COLLECTIONS.values():
            if name == "all":
                continue
            try:
                vs = Chroma(
                    collection_name   = name,
                    embedding_function= embeddings,
                    persist_directory = CHROMA_DIR,
                )
                results = vs.similarity_search_with_score(query, k=top_k)
                for doc, score in results:
                    doc.metadata["collection"] = name
                all_results.extend(results)
            except Exception as e:
                print(f"Warning: could not search '{name}': {e}")

        all_results.sort(key=lambda x: x[1])
        return all_results[:top_k]

    else:
        vs = Chroma(
            collection_name   = collection_name,
            embedding_function= embeddings,
            persist_directory = CHROMA_DIR,
        )
        results = vs.similarity_search_with_score(query, k=top_k)
        for doc, score in results:
            doc.metadata["collection"] = collection_name
        return results


def build_context(chunks):
    """Combine retrieved chunks into a single context string."""
    return "\n\n".join([doc.page_content for doc, _ in chunks])


def generate_answer(query: str, context: str) -> str:
    """Use a local QA model to generate an answer from the context."""
    if not context.strip():
        return "I couldn't find relevant information to answer your question."

    qa = get_qa_pipeline()

    # QA models have a token limit — truncate context if too long
    max_context_chars = 3000
    if len(context) > max_context_chars:
        context = context[:max_context_chars]

    try:
        result = qa(question=query, context=context)
        answer = result.get("answer", "").strip()
        score  = result.get("score", 0)

        # If confidence is too low, return a fallback with context summary
        if score < 0.05 or not answer:
            return (
                "I found some relevant content but couldn't extract a precise answer. "
                "Here is the most relevant passage:\n\n"
                + context[:800]
            )

        return answer

    except Exception as e:
        return f"Error generating answer: {str(e)}"


def get_sources(chunks):
    """Extract source metadata from retrieved chunks."""
    sources = []
    seen = set()
    for doc, score in chunks:
        source   = os.path.basename(doc.metadata.get("source", "Unknown"))
        page     = doc.metadata.get("page_number", "?")
        collection = doc.metadata.get("collection", "?")
        key = f"{source}-{page}"
        if key not in seen:
            seen.add(key)
            sources.append({
                "file":       source,
                "page":       page,
                "collection": collection,
                "score":      round(score, 4),
                "snippet":    doc.page_content[:200],
            })
    return sources


def ask(query: str, book_label: str = "All Books") -> dict:
    """
    Main RAG function. Call this from Streamlit.

    Parameters
    ----------
    query      : user question
    book_label : dropdown label from COLLECTIONS keys

    Returns
    -------
    dict with keys: answer, sources, context
    """
    collection_name = COLLECTIONS.get(book_label, "all")
    chunks          = retrieve_chunks(query, collection_name=collection_name)

    if not chunks:
        return {
            "answer":  "No relevant content found. Try rephrasing your question.",
            "sources": [],
            "context": "",
        }

    context = build_context(chunks)
    answer  = generate_answer(query, context)
    sources = get_sources(chunks)

    return {
        "answer":  answer,
        "sources": sources,
        "context": context,
    }