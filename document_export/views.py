import os
from django.http import FileResponse
from django.shortcuts import get_object_or_404

from question_generator.models import QuestionPaper
from .services import PDFExportService


def export_question_paper(request, paper_id):

    paper = get_object_or_404(QuestionPaper, id=paper_id)

    questions = paper.questions.all().order_by("sequence")

    file_path = f"media/question_paper_{paper.id}.pdf"

    PDFExportService.export_question_paper(paper, questions, file_path)

    return FileResponse(open(file_path, "rb"), as_attachment=True)