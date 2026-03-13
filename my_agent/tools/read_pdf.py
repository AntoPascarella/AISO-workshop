import fitz  # PyMuPDF


def read_pdf(file_path: str) -> str:
    """Read a PDF file and return all of its text content.

    Use this tool whenever a question references an attached file or PDF.
    Pass the exact file path mentioned in the question.

    Args:
        file_path: The path to the PDF file to read.

    Returns:
        The full text content of the PDF.
    """
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"