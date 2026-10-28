from ai_engine.services.syllabus_service import process_material_for_ai
from materials.models import StudyMaterial
from django.db import close_old_connections


def process_uploaded_material(material_id):

    close_old_connections()

    try:

        material = StudyMaterial.objects.get(
            id=material_id
        )

        return process_material_for_ai(material)

    finally:

        close_old_connections()