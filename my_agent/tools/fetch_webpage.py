import requests
from bs4 import BeautifulSoup


def fetch_webpage(url: str) -> str:
    """Fetch a webpage and return its text content.

    Use this tool when you have a specific URL and need to read its content.
    Use this after web_search to read a specific result, or when a question
    provides a URL directly.

    Args:
        url: The full URL of the webpage to fetch.

    Returns:
        The text content of the webpage (truncated to 10000 characters).
    """
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove script and style elements
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)
        if len(text) > 10000:
            text = text[:10000] + "\n...(truncated)"
        return text
    except Exception as e:
        return f"Error fetching webpage: {str(e)}"