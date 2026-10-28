import json
import ollama

from django.conf import settings


class AIProvider:
    """
    Handles communication with the configured AI provider.
    Currently supports Ollama.
    """

    def __init__(self):

        self.model = settings.OLLAMA_MODEL

        self.client = ollama.Client(
            host=settings.OLLAMA_HOST
        )

    def ask(self, prompt):

        response = self.client.chat(
        model=self.model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "num_predict": 4096,
            "temperature": 0.2,
        }
    )

        return response["message"]["content"].strip()

    def ask_json(self, prompt):

        for attempt in range(3):

            try:

                result = self.ask(prompt)

                # Remove markdown if the model wraps JSON
                result = (
                    result
                    .replace("```json", "")
                    .replace("```", "")
                    .strip()
                )

                return json.loads(result)

            except json.JSONDecodeError:

                if attempt == 2:
                    raise

                print("Retrying AI generation...\n")