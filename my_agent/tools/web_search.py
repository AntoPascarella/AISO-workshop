from urllib.parse import urlparse
from urllib.request import Request, urlopen

import pymupdf
from bs4 import BeautifulSoup
from ddgs import DDGS


_STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "that",
    "this",
    "what",
    "when",
    "where",
    "which",
    "have",
    "has",
    "had",
    "into",
    "also",
    "just",
    "give",
    "name",
    "path",
    "only",
    "using",
    "received",
}


def web_search(query: str, max_results: int = 8) -> list[dict]:
    """Search the web using DuckDuckGo and return results.

    Use this tool when a question requires up-to-date information,
    real-world facts, or anything not in your training data.

    Args:
        query: The search query string.
        max_results: Maximum number of results to return.

    Returns:
        A list of results, each with 'title', 'url', and 'snippet'.
    """
    query = (query or "").strip()
    if not query:
        return []

    safe_limit = min(max(max_results, 1), 15)
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=safe_limit)
            return [
                {
                    "title": item.get("title", ""),
                    "url": item.get("href", ""),
                    "snippet": item.get("body", ""),
                }
                for item in results
                if item.get("href")
            ]
    except Exception as exc:
        return [
            {
                "title": "web_search_error",
                "url": "",
                "snippet": f"DuckDuckGo search failed: {exc}",
            }
        ]


def _extract_pdf_text(content: bytes, max_chars: int) -> str:
    doc = pymupdf.open(stream=content, filetype="pdf")
    try:
        parts = []
        for i, page in enumerate(doc):
            parts.append(f"[Page {i + 1}]\n{page.get_text()}")
            if sum(len(part) for part in parts) >= max_chars:
                break
        return "\n\n".join(parts)[:max_chars]
    finally:
        doc.close()


def _extract_html_text(html: str, max_chars: int, fragment: str | None = None) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "form", "svg", "aside"]):
        tag.decompose()

    text = ""
    if fragment:
        anchor = soup.find(id=fragment)
        if anchor:
            parts = [f"[Anchored section: #{fragment}]", anchor.get_text(separator=" ", strip=True)]
            for sibling in anchor.find_all_next():
                if sibling is anchor:
                    continue
                if sibling.name in {"h1", "h2"}:
                    break
                chunk = sibling.get_text(separator=" ", strip=True)
                if chunk:
                    parts.append(chunk)
                if sum(len(part) for part in parts) >= max_chars:
                    break
            section_text = "\n".join(part for part in parts if part)
            if section_text.strip():
                return section_text[:max_chars]

    lines = [line.strip() for line in soup.get_text(separator="\n").splitlines() if line.strip()]
    text += "\n".join(lines)
    return text[:max_chars]


def _filter_relevant_text(text: str, question: str, max_chars: int) -> str:
    keywords = {
        token.lower().strip(".,:;!?()[]{}\"'`")
        for token in question.split()
        if len(token.strip(".,:;!?()[]{}\"'`")) >= 4
    }
    keywords -= _STOPWORDS
    if not keywords:
        return text[:max_chars]

    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        return text[:max_chars]

    scored = []
    for i, line in enumerate(lines):
        hay = line.lower()
        score = sum(1 for kw in keywords if kw in hay)
        if score > 0:
            scored.append((score, i))

    if not scored:
        return text[:max_chars]

    scored.sort(reverse=True)
    selected = set()
    for _, idx in scored[:12]:
        selected.add(idx)
        if idx - 1 >= 0:
            selected.add(idx - 1)
        if idx + 1 < len(lines):
            selected.add(idx + 1)

    filtered = "\n".join(lines[i] for i in sorted(selected))
    return filtered[:max_chars]


def fetch_webpage(url: str, question: str = "", max_chars: int = 20000) -> str:
    """Fetch a webpage and return its text content.

    Use this tool to read the full content of a URL. It supports HTML pages
    and direct PDF URLs.

    Args:
        url: The URL of the webpage to fetch.
        question: Optional original user question to focus extraction.
        max_chars: Maximum amount of extracted text to return.

    Returns:
        Extracted text content of the page.
    """
    parsed = urlparse((url or "").strip())
    if parsed.scheme not in {"http", "https"}:
        return "fetch_webpage_error: URL must start with http:// or https://"

    safe_limit = min(max(max_chars, 1000), 50000)
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/126.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/pdf;q=0.9,*/*;q=0.8",
    }

    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=15) as response:
            content_type = response.headers.get("Content-Type", "").lower()
            payload = response.read()

        if "application/pdf" in content_type or parsed.path.lower().endswith(".pdf"):
            extracted = _extract_pdf_text(payload, safe_limit)
        else:
            html = payload.decode("utf-8", errors="ignore")
            extracted = _extract_html_text(html, safe_limit, parsed.fragment or None)

        if question.strip():
            extracted = _filter_relevant_text(extracted, question, safe_limit)

        if not extracted.strip():
            return "fetch_webpage_error: page was fetched but no readable text was extracted"

        return extracted
    except Exception as exc:
        return f"fetch_webpage_error: {exc}"
