from ai_engine.question_generator import QuestionGenerator


def generate_questions_for_material(
    material,
    unit,
    difficulty,
    bloom,
    question_type,
    marks,
    count,
    section,
    previous_questions=None,
):

    return QuestionGenerator.generate(
        material_id=material.id,
        unit=unit,
        difficulty=difficulty,
        bloom=bloom,
        question_type=question_type,
        marks=marks,
        count=count,
        section=section,
        previous_questions=previous_questions or [],
    )