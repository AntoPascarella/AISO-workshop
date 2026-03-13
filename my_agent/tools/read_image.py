import base64
import os
from google import genai


def read_image(file_path: str, question: str) -> str:
    """Analyze an image file and answer a question about it.

    Use this tool whenever a question mentions an attached image,
    a .png or .jpg file, or any visual content that needs to be interpreted.

    Args:
        file_path: The path to the image file (e.g. 'benchmark/attachments/14.png').
        question: The specific question to answer about the image.

    Returns:
        A description or answer based on the image content.
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: File not found at '{file_path}'"

        with open(file_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")

        ext = file_path.split(".")[-1].lower()
        mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg"}.get(ext, "image/png")

        client = genai.Client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                {
                    "parts": [
                        {"inline_data": {"mime_type": mime, "data": image_data}},
                        {"text": question},
                    ]
                }
            ],
        )
        return response.text
    except Exception as e:
        return f"Error reading image: {str(e)}"