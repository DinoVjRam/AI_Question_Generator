from django import forms
from .models import StudyMaterial


class StudyMaterialForm(forms.ModelForm):

    class Meta:
        model = StudyMaterial

        fields = [
            "course_code",
            "title",
            "subject",
            "department",
            "semester",
            "academic_year",
            "uploaded_file",
        ]

        widgets = {
            "course_code": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "title": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "subject": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "department": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "semester": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "academic_year": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "uploaded_file": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
        }


# =====================================================
# AI QUESTION GENERATION FORM
# =====================================================

class QuestionGenerationForm(forms.Form):

    DIFFICULTY_CHOICES = [

        ("easy", "Easy"),

        ("medium", "Medium"),

        ("hard", "Hard"),

    ]


    BLOOM_CHOICES = [

        ("remember", "Remember"),

        ("understand", "Understand"),

        ("apply", "Apply"),

        ("analyze", "Analyze"),

        ("evaluate", "Evaluate"),

        ("create", "Create"),

    ]


    QUESTION_TYPE_CHOICES = [

        ("mixed", "Mixed"),

        # ("mcq", "MCQ"),

        # ("short", "Short Answer"),

        # ("long", "Long Answer"),

    ]


    difficulty = forms.ChoiceField(

        choices=DIFFICULTY_CHOICES,

        initial="medium",

        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )


    bloom = forms.ChoiceField(

        choices=BLOOM_CHOICES,

        initial="understand",

        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )


    question_type = forms.ChoiceField(

        choices=QUESTION_TYPE_CHOICES,

        initial="mixed",

        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )