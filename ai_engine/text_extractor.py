import fitz
from docx import Document
from pathlib import Path


class TextExtractor:
    """
    Extracts plain text from supported document types.
    """

    @staticmethod
    def extract(file_path):
        file_path = Path(file_path)

        extension = file_path.suffix.lower()

        if extension == ".pdf":
            return TextExtractor._extract_pdf(file_path)

        elif extension == ".docx":
            return TextExtractor._extract_docx(file_path)

        elif extension == ".txt":
            return file_path.read_text(encoding="utf-8")

        else:
            raise ValueError(f"Unsupported file type: {extension}")

    @staticmethod
    def _extract_pdf(file_path):
        text = ""

        pdf = fitz.open(file_path)

        for page in pdf:
            text += page.get_text()

        pdf.close()

        return text

    @staticmethod
    def _extract_docx(file_path):
        doc = Document(file_path)

        return "\n".join(
            paragraph.text
            for paragraph in doc.paragraphs
        )