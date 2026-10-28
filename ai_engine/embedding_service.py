import ollama

from django.conf import settings


class EmbeddingService:

    def __init__(self):

        self.client = ollama.Client(
            host=settings.OLLAMA_HOST
        )

        self.model = "nomic-embed-text"

    def embed(self, text):

        response = self.client.embed(
            model=self.model,
            input=text
        )

        return response["embeddings"][0]