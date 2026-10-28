from django.urls import path
from . import views

urlpatterns = [
    path("", views.material_list, name="material_list"),
    path("upload/", views.material_upload, name="material_upload"),
    path("analyze/<int:material_id>/", views.analyze_syllabus, name="analyze_syllabus"),
    path("units/<int:material_id>/", views.view_units, name="view_units"),
    # path("select/<int:material_id>/", views.unit_selection, name="unit_selection"),
    # path("generate-api/<int:material_id>/", views.generate_questions_api, name="generate_questions_api"),
    # path("ai/", views.ai_question_generator, name="ai_question_generator"),
]