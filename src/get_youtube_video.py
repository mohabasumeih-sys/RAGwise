from youtubesearchpython import VideosSearch


# ── CONFIG ────────────────────────────────────────────────────────────────────
MAX_RESULTS = 3   # number of YouTube videos to return per query

# Topic-specific search prefixes to get better results
COLLECTION_PREFIXES = {
    "agentic_ai":           "agentic AI tutorial",
    "deep_learning":        "deep learning explained",
    "large_language_model": "large language model LLM tutorial",
    "machine_learning":     "machine learning tutorial",
    "nlp":                  "natural language processing tutorial",
    "all":                  "AI machine learning tutorial",
}
# ─────────────────────────────────────────────────────────────────────────────


def search_youtube(query: str, collection_name: str = "all", max_results: int = MAX_RESULTS):
    """
    Search YouTube for videos relevant to the query.

    Parameters
    ----------
    query           : user question / topic
    collection_name : collection key to add topic context
    max_results     : number of videos to return

    Returns
    -------
    list of dicts with keys: title, url, thumbnail, channel, duration, views
    """
    # Add topic prefix for better search results
    prefix       = COLLECTION_PREFIXES.get(collection_name, "")
    search_query = f"{prefix} {query}".strip()

    try:
        search  = VideosSearch(search_query, limit=max_results)
        results = search.result().get("result", [])

        videos = []
        for video in results:
            videos.append({
                "title":     video.get("title", "Unknown"),
                "url":       video.get("link", ""),
                "thumbnail": video.get("thumbnails", [{}])[0].get("url", ""),
                "channel":   video.get("channel", {}).get("name", "Unknown"),
                "duration":  video.get("duration", "N/A"),
                "views":     video.get("viewCount", {}).get("short", "N/A"),
            })

        return videos

    except Exception as e:
        print(f"YouTube search error: {e}")
        return []


def get_video_references(query: str, collection_name: str = "all") -> list:
    """
    Convenience function called from Streamlit / chatbot_utility.

    Usage:
        from src.get_youtube_video import get_video_references
        videos = get_video_references("what is attention mechanism?", "large_language_model")
    """
    return search_youtube(query, collection_name=collection_name)


if __name__ == "__main__":
    # Quick test
    results = get_video_references("what is attention mechanism?", "large_language_model")
    for i, v in enumerate(results, 1):
        print(f"\n[{i}] {v['title']}")
        print(f"     Channel  : {v['channel']}")
        print(f"     Duration : {v['duration']}  |  Views : {v['views']}")
        print(f"     URL      : {v['url']}")