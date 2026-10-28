from django.db import models
from django.contrib.auth.models import User


class StudyMaterial(models.Model):
    """
    Stores study materials uploaded by teachers.
    """

    DOCUMENT_TYPES = [
        ("SYLLABUS", "Syllabus"),
    ]

    FILE_TYPES = [
        ("PDF", "PDF"),
        ("DOCX", "DOCX"),
        ("PPTX", "PPTX"),
        ("TXT", "TXT"),
    ]

    STATUS_CHOICES = [
    ("UPLOADED", "Uploaded"),
    ("TEXT_EXTRACTED", "Text Extracted"),
    ("UNITS_EXTRACTED", "Units Extracted"),
    ("GENERATING_QUESTIONS", "Generating Questions"),
    ("QUESTIONS_GENERATED", "Questions Generated"),
    ("FAILED", "Failed"),
    ]

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="study_materials",
    )

    course_code = models.CharField(max_length=20)

    title = models.CharField(max_length=200)

    subject = models.CharField(max_length=100)

    department = models.CharField(max_length=100)

    semester = models.CharField(max_length=20)

    academic_year = models.CharField(max_length=20)

    document_type = models.CharField(
        max_length=30,
        choices=DOCUMENT_TYPES,
        default="SYLLABUS",
    )

    uploaded_file = models.FileField(
        upload_to="study_materials/"
    )

    extracted_text = models.TextField(
    blank=True,
    default=""
    )

    units_json = models.JSONField(
        blank=True,
        null=True
    )

    file_type = models.CharField(
        max_length=10,
        choices=FILE_TYPES,
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="UPLOADED",
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.course_code} - {self.title}"
    
class GeneratedQuestionPaper(models.Model):

    material = models.ForeignKey(
        StudyMaterial,
        on_delete=models.CASCADE,
        related_name="question_papers"
    )

    selected_units = models.JSONField()

    difficulty = models.CharField(max_length=20)

    bloom = models.CharField(max_length=20)

    question_count = models.IntegerField()

    questions_json = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.material.course_code} - {self.created_at}"