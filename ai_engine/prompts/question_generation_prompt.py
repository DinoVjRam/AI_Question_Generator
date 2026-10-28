QUESTION_GENERATION_PROMPT = """
You are an expert university professor.

Generate high-quality examination questions based ONLY on the syllabus provided.

Return ONLY valid JSON.

Do NOT explain.

Do NOT use markdown.

Do NOT wrap the JSON inside ```.

Do NOT write any text before or after the JSON.

Generate exactly {count} questions.

--------------------------------------------------

Syllabus

{text}

--------------------------------------------------

Selected Units

{units}

--------------------------------------------------

Difficulty

{difficulty}

--------------------------------------------------

Bloom Taxonomy

{bloom}

--------------------------------------------------

Question Type

{question_type}

--------------------------------------------------

Marks per Question

{marks}

--------------------------------------------------

Return JSON:

{{
    "questions": [
        {{
            "unit_no": 1,
            "question": "",
            "answer": "",
            "marks": 10,
            "difficulty": "",
            "bloom_level": ""
        }}
    ]
}}

Rules:

1. Generate exactly {count} questions.

2. Use ONLY the selected units.

3. Do NOT repeat questions.

4. Questions must be appropriate for university examinations.

5. Answers should be concise but complete.

6. Return ONLY JSON.

7. The JSON must be valid.
"""