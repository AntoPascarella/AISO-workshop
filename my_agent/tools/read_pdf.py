from urllib.request import Request, urlopen

import pymupdf


def read_pdf(file_path: str) -> str:
    """Read and extract all text content from a PDF file or PDF URL.

    Use this tool when a question references a PDF file, attachment, or PDF URL.
    Accepts both local file paths and http/https URLs pointing to PDF files.

    Args:
        file_path: Local path or URL to the PDF.

    Returns:
        The full text content of the PDF.
    """
    path = file_path.strip()
    if path.startswith(("http://", "https://")):
        req = Request(path, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0.0.0",
        })
        with urlopen(req, timeout=20) as resp:
            data = resp.read()
        doc = pymupdf.open(stream=data, filetype="pdf")
    else:
        doc = pymupdf.open(path)
    text = "\n".join(page.get_text() for page in doc)
    doc.close()
    return text
