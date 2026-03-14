import os
import pathlib

from google import genai


def read_image(file_path: str, question: str) -> str:
    """Analyze an image file and answer a question about it.

    Use this tool when a question references an image file (PNG, JPG, etc.).
    Pass the file path and the full question so the image can be analyzed.

    Args:
        file_path: Path to the image file to analyze.
        question: The question to answer about the image.

    Returns:
        A detailed analysis of the image relevant to the question.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=api_key)
    image_path = pathlib.Path(file_path)
    uploaded = client.files.upload(file=image_path)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            uploaded,
            question + " Be extremely detailed and precise in your analysis.",
        ],
    )
    return response.text
