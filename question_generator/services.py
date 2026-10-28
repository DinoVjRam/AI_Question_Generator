from ai_engine.services.question_service import generate_questions_for_material
from .models import QuestionPaper, Question

class QuestionGenerationService:

    @staticmethod
    def generate_and_save_paper(
        teacher,
        material,
        units,
        difficulty,
        bloom,
        question_type,
        question_pattern,
    ):

        all_questions = []
        previous_questions = []

        # ==========================================
        # Generate questions pattern by pattern
        # ==========================================

        for pattern in question_pattern:

            for question_no in range(pattern["count"]):
                ai_result = generate_questions_for_material(
                    material=material,
                    unit=pattern["unit"],
                    difficulty=difficulty,
                    bloom=bloom,
                    question_type=question_type,
                    marks=pattern["marks"],
                    count=1,
                    section=pattern["section"],
                    previous_questions=previous_questions,

                )

                if ai_result and ai_result.get("questions"):
                    question = ai_result["questions"][0]
                    previous_questions.append(question["question"])
                    question["section"] = pattern["section"]
                    all_questions.append(question)

        merged_result = {
            "questions": all_questions
        }

        return QuestionGenerationService.save_questions(
            teacher=teacher,
            material=material,
            ai_result=merged_result,
            difficulty=difficulty,
            bloom=bloom,
            question_type=question_type,
            question_pattern=question_pattern

        )
    

    @staticmethod
    def save_questions(
        teacher,
        material,
        ai_result,
        difficulty,
        bloom,
        question_type,
        question_pattern
    ):


        total_questions = len(
            ai_result.get(
                "questions",
                []
            )
        )


        paper = QuestionPaper.objects.create(
            teacher=teacher,
            study_material=material,
            title=f"{material.title} - Generated Paper",
            difficulty=difficulty,
            bloom_level=bloom,
            question_type=question_type,
            total_questions=total_questions,
            question_pattern=question_pattern,

        )

        for idx, q in enumerate(
            ai_result["questions"],
            start=1
        ):

            Question.objects.create(
                paper=paper,
                section=q.get(
                    "section",
                    "A"
                ),

                unit_no=q.get(
                    "unit_no",
                    1
                ),

                question=q.get(
                    "question",
                    ""
                ),

                answer=q.get(
                    "answer",
                    ""
                ),

                marks=q.get(
                    "marks",
                    1
                ),

                difficulty=q.get(
                    "difficulty",
                    difficulty
                ),

                bloom_level=q.get(
                    "bloom_level",
                    bloom
                ),

                sequence=idx
            )

        return paper