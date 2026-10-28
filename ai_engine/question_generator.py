from .retrieval_service import RetrievalService
from .ai_provider import AIProvider



class QuestionGenerator:


    @staticmethod
    def generate(
    material_id,
    unit,
    difficulty,
    bloom,
    question_type,
    marks,
    count,
    section,
    previous_questions,
):


        retriever = RetrievalService()

        ai = AIProvider()



        # =================================
        # STEP 1: Retrieve RAG Context
        # =================================

        context_text = retriever.retrieve(

        material_id=material_id,

        units=[unit],

        difficulty=difficulty,

        bloom=bloom,

        top_k=8

    )
        
        # =================================
        # STEP 2: Previous Questions
        # =================================
       

        if not context_text:

            context_text = (
                "No relevant syllabus content found."
            )           


        # =================================
        # STEP 3: Build Ollama Prompt
        # =================================

        prompt = f"""
You are an experienced university examiner.

Generate examination questions using ONLY the syllabus context below.

==================================================
SYLLABUS CONTEXT
==================================================

{context_text}

==================================================
ALREADY GENERATED QUESTIONS
==================================================

{previous_questions if previous_questions else "None"}

==================================================
QUESTION REQUIREMENTS
==================================================

Section:
{section}

Unit:
{unit}

Marks per Question:
{marks}

Number of Questions:
{count}

Difficulty:
{difficulty}

Bloom Level:
{bloom}

Question Type:
{question_type}

==================================================
RULES
==================================================

1. Generate EXACTLY ONE question.
The question must:
- belong to Unit {unit}
- carry {marks} marks
- belong to Section {section}
2. Every question must carry {marks} marks.
3. Every question must belong to Unit {unit}.
4. Use ONLY the syllabus context.
5. Do NOT repeat any of the previously generated questions.
6. Do NOT generate questions that test the same concept using different wording.
7. Generate a completely different question from the previous ones.
8. Provide a model answer in 3-5 key points.Maximum 80 words..
9. If you cannot generate exactly {count} questions, regenerate internally until the count matches.
10. Return ONLY valid JSON.

==================================================
OUTPUT FORMAT
==================================================

{{
    "questions":[
        {{
            "unit_no": {unit},
            "question":"",
            "answer":"",
            "marks": {marks},
            "difficulty":"{difficulty}",
            "bloom_level":"{bloom}"
        }}
    ]
}}
"""


        result = ai.ask_json(
            prompt
        )


        return result