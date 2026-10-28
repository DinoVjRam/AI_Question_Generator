from django.db import models
from django.contrib.auth.models import User

from materials.models import StudyMaterial


class QuestionPaper(models.Model):

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    study_material = models.ForeignKey(
        StudyMaterial,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=255
    )

    difficulty = models.CharField(
        max_length=50
    )

    bloom_level = models.CharField(
        max_length=50
    )

    question_type = models.CharField(
        max_length=50
    )

    total_questions = models.IntegerField()


    question_pattern = models.JSONField(
        default=list,
        blank=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class Question(models.Model):

    paper = models.ForeignKey(
        QuestionPaper,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    section = models.CharField(
        max_length=5,
        default="A"
    )

    unit_no = models.IntegerField()

    question = models.TextField()

    answer = models.TextField()

    marks = models.IntegerField()

    difficulty = models.CharField(max_length=20)

    bloom_level = models.CharField(max_length=50)

    sequence = models.IntegerField()

    def __str__(self):
        return f"Q{self.sequence}"