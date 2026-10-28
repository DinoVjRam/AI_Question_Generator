from django import forms


class GenerateQuestionForm(forms.Form):

    difficulty = forms.ChoiceField(
        choices=[
            ("Easy", "Easy"),
            ("Medium", "Medium"),
            ("Hard", "Hard"),
        ],
        initial="Medium",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    bloom = forms.ChoiceField(
        choices=[
            ("Remember", "Remember"),
            ("Understand", "Understand"),
            ("Apply", "Apply"),
            ("Analyze", "Analyze"),
            ("Evaluate", "Evaluate"),
            ("Create", "Create"),
        ],
        initial="Analyze",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    question_type = forms.ChoiceField(
        choices=[
            # ("MCQ", "MCQ"),
            # ("Short Answer", "Short Answer"),
            # ("Long Answer", "Long Answer"),
            ("Mixed", "Mixed"),
        ],
        initial="Mixed",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    marks = forms.ChoiceField(
        choices=[
            (1, "1 Marks"),
            (2, "2 Marks"),
            (5, "5 Marks"),
            (10, "10 Marks"),
            (15, "15 Marks"),
        ],
        initial=10,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    total_questions = forms.IntegerField(
        initial=10,
        min_value=1,
        max_value=100,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )