UNIT_EXTRACTION_PROMPT = """
You are an academic syllabus analyzer.

Analyze the syllabus below.

Extract:
- Unit Number
- Unit Title
- Topics

Return ONLY valid JSON.

Example:

{{
    "units":[
        {{
            "unit_number":1,
            "title":"Introduction",
            "topics":[
                "History",
                "Applications"
            ]
        }}
    ]
}}

Syllabus:

{text}
"""