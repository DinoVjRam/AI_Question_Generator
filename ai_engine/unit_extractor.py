from .ai_provider import AIProvider
from .prompts.unit_extraction_prompt import UNIT_EXTRACTION_PROMPT


class UnitExtractor:

    @staticmethod
    def extract(text):

        prompt = UNIT_EXTRACTION_PROMPT.replace("{text}", text)

        ai = AIProvider()

        return ai.ask_json(prompt)