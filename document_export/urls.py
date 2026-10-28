from django.urls import path
from . import views

urlpatterns = [
    path(
        "export/<int:paper_id>/",
        views.export_question_paper,
        name="export_question_paper"
    ),
]