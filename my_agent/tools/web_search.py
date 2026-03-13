from ddgs import DDGS


def web_search(query: str) -> str:
    """Search the web using DuckDuckGo and return results.

    Use this tool when you need to find information on the internet,
    look up facts, find URLs, or answer questions about real-world topics.

    Args:
        query: The search query string.

    Returns:
        A list of search results with titles, URLs, and snippets.
    """
    try:
        results = DDGS().text(query, max_results=5)
        if not results:
            return "No results found."
        output = ""
        for r in results:
            output += f"Title: {r['title']}\n"
            output += f"URL: {r['href']}\n"
            output += f"Snippet: {r['body']}\n\n"
        return output
    except Exception as e:
        return f"Error searching: {str(e)}"