from ai_engine.text_extractor import TextExtractor
from ai_engine.syllabus_parser import SyllabusParser
from ai_engine.unit_extractor import UnitExtractor
from ai_engine.index_service import IndexService


def analyze_material_units(study_material):
    """
    Re-analyze units from an already extracted document.
    """

    text = study_material.extracted_text or ""

    # Extract only syllabus portion
    syllabus_text = SyllabusParser.get_syllabus_only(text)

    # AI extracts units
    units = UnitExtractor.extract(syllabus_text)

    study_material.units_json = units
    study_material.status = "UNITS_EXTRACTED"
    study_material.save()

    return units


def process_material_for_ai(study_material):
    """
    Complete AI processing pipeline:
        1. Extract text
        2. Extract syllabus section
        3. Extract units using AI
        4. Index the full document for RAG
    """

    # -------------------------------------------------
    # STEP 1 : Extract text from uploaded file
    # -------------------------------------------------

    text = TextExtractor.extract(
        study_material.uploaded_file.path
    )

    study_material.extracted_text = text
    study_material.status = "TEXT_EXTRACTED"
    study_material.save()

    # -------------------------------------------------
    # STEP 2 : Get syllabus only
    # -------------------------------------------------

    syllabus_text = SyllabusParser.get_syllabus_only(text)

    # -------------------------------------------------
    # STEP 3 : AI extracts units
    # -------------------------------------------------

    units = UnitExtractor.extract(syllabus_text)

    study_material.units_json = units
    study_material.status = "UNITS_EXTRACTED"
    study_material.save()

    # -------------------------------------------------
    # STEP 4 : Index FULL document for RAG
    # -------------------------------------------------

    indexer = IndexService()

    indexer.index_document(
        study_material.id,
        text
    )

    return study_material


def process_syllabus(study_material):
    """
    Backward compatibility.
    """

    return process_material_for_ai(study_material)