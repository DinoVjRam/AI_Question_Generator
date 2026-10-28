from django.contrib import admin
from .models import StudyMaterial


@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = (
        "course_code",
        "title",
        "academic_year",
        "department",
        "semester",
        "teacher",
        "document_type",
        "status",
        "uploaded_at",
    )
    readonly_fields = (
        "extracted_text",
        "units_json",
    )

    list_filter = (
        "department",
        "semester",
        "academic_year",
        "status",
    )

    search_fields = (
        "course_code",
        "title",
        "subject",
        "teacher__username",
    )

    ordering = ("-uploaded_at",)