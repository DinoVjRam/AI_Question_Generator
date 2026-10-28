from django.urls import path

from . import views

urlpatterns = [
    # path(
    #     "",
    #     views.question_generator_home,
    #     name="question_generator_home",
    # ),
    path(
        "", 
        views.export_papers, 
        name="export_papers"
    ),
    path(
        "generate/<int:material_id>/",
        views.generate_questions,
        name="generate_questions",
    ),
     # Question generation form
    path(
        "generate-form/<int:material_id>/",
        views.question_generator_form,
        name="question_generator_form",
    ),
    path(
           "preview/<int:paper_id>/",
           views.question_preview,
           name="question_preview",
       ),
    path(
        "papers/<int:material_id>/",
        views.question_paper_list,
        name="question_paper_list",
    ),
    path(
        "paper/<int:paper_id>/",
        views.question_paper_detail,
        name="question_paper_detail",
    ),   
    path(
    "paper/<int:paper_id>/download-answer-key/",
    views.download_answer_key_word,
    name="download_answer_key_word"
    ),
    path(
    "paper/<int:paper_id>/download-word/",
    views.download_question_word,
    name="download_question_word"
    ),
    path(
    "paper/<int:paper_id>/download-pdf/",
    views.download_question_pdf,
    name="download_question_pdf"
    ),
    path(
    "status/<int:material_id>/",
    views.question_generation_status,
    name="question_generation_status",
    ),
]