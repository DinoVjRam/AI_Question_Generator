from types import SimpleNamespace
from unittest.mock import patch

from django.test import SimpleTestCase

from ai_engine.services.question_service import generate_questions_for_material


class QuestionServiceTests(SimpleTestCase):
    @patch("ai_engine.services.question_service.QuestionGenerator.generate")
    def test_generate_questions_for_material_returns_ai_payload(self, mock_generate):
        material = SimpleNamespace(extracted_text="Sample syllabus text")
        mock_generate.return_value = {
            "questions": [{"question": "What is 2+2?", "unit_no": 1}]
        }

        result = generate_questions_for_material(
            material,
            ["Unit 1"],
            difficulty="Medium",
            bloom="Understand",
            question_type="Short Answer",
            marks=5,
            count=1,
        )

        self.assertEqual(result["questions"][0]["question"], "What is 2+2?")
        mock_generate.assert_called_once()
