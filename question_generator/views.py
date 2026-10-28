from django.shortcuts import render, redirect, get_object_or_404
import threading
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from materials.models import StudyMaterial
from .forms import GenerateQuestionForm
from .services import QuestionGenerationService
from .models import QuestionPaper
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa


# def question_generator_home(request):

#     materials = StudyMaterial.objects.filter(
#         status="UNITS_EXTRACTED"
#     )

#     return render(
#         request,
#         "materials/material_list.html",
#         {
#             "materials": materials
#         }
#     )

@login_required
def export_papers(request):

    materials = StudyMaterial.objects.filter(
        teacher=request.user
    ).order_by("-uploaded_at")

    return render(
        request,
        "question_generator/export_papers.html",
        {
            "materials": materials
        }
    )

@login_required
def generate_questions(request, material_id):

    material = get_object_or_404(
        StudyMaterial,
        id=material_id,
        teacher=request.user
    )

    if not material.units_json:

        return JsonResponse({
            "error": "Units not found. Please analyze syllabus first."
        }, status=400)


    if request.method != "POST":

        return JsonResponse({
            "error": "Invalid request method."
        }, status=405)


    # =================================================
    # FORM
    # =================================================

    form = GenerateQuestionForm(request.POST)


    if form.is_valid() or request.POST.getlist("marks[]"):


        # =================================================
        # Selected Units
        # =================================================

        units = request.POST.getlist(
            "units"
        )


        # =================================================
        # Question Pattern
        # =================================================

        sections = request.POST.getlist(
            "sections[]"
        )

        pattern_units = request.POST.getlist(
            "pattern_units[]"
        )

        marks = request.POST.getlist(
            "marks[]"
        )

        counts = request.POST.getlist(
            "counts[]"
        )


        question_pattern = []


        for section, unit, mark, count in zip(
            sections,
            pattern_units,
            marks,
            counts,
        ):

            question_pattern.append(
                {
                    "section": section,
                    "unit": int(unit),
                    "marks": int(mark),
                    "count": int(count),
                }
            )


        # =================================================
        # START BACKGROUND GENERATION
        # =================================================

        thread = threading.Thread(

            target=generate_questions_background,

            args=(
                material.id,
                request.user.id,
                units,
                form.cleaned_data.get(
                    "difficulty",
                    "Medium"
                ),
                form.cleaned_data.get(
                    "bloom",
                    "Understand"
                ),
                form.cleaned_data.get(
                    "question_type",
                    "Mixed"
                ),
                question_pattern,
            )
        )


        thread.daemon = True

        thread.start()


        # =================================================
        # REDIRECT IMMEDIATELY
        # =================================================

        return redirect(
            "question_paper_list",
            material.id
        )


    else:

        return render(
            request,
            "question_generator/question_preview.html",
            {
                "material": material,
                "form": form,
            },
        )

def generate_questions_background(
    material_id,
    user_id,
    units,
    difficulty,
    bloom,
    question_type,
    question_pattern,
):

    try:

        # =================================================
        # Get material
        # =================================================

        material = StudyMaterial.objects.get(
            id=material_id
        )


        # =================================================
        # Get user
        # =================================================

        user = User.objects.get(
            id=user_id
        )


        # =================================================
        # Generate Question Paper
        # SAME CALL AS YOUR ORIGINAL WORKING CODE
        # =================================================

        paper = QuestionGenerationService.generate_and_save_paper(

            teacher=user,

            material=material,

            units=units,

            difficulty=difficulty,

            bloom=bloom,

            question_type=question_type,

            question_pattern=question_pattern,

        )

        material.status = "QUESTIONS_GENERATED"

        material.save(
            update_fields=["status"]
        )

    except Exception as e:

        print("=" * 80)
        print("QUESTION GENERATION ERROR")
        print(str(e))
        print("=" * 80)

@login_required
def question_paper_list(request, material_id):

    material = get_object_or_404(
        StudyMaterial,
        id=material_id,
        teacher=request.user
    )

    papers = QuestionPaper.objects.filter(
        study_material=material
    ).order_by("-created_at")

    return render(
        request,
        "materials/question_paper_list.html",
        {
            "material": material,
            "papers": papers,
        }
    )


# def question_paper_detail(request, paper_id):

#     paper = get_object_or_404(QuestionPaper, id=paper_id)

#     return render(
#         request,
#         "materials/question_paper_detail.html",
#         {
#             "paper": paper,
#         },
#     )

@login_required
def question_paper_detail(request, paper_id):

    paper = get_object_or_404(
        QuestionPaper,
        id=paper_id
    )

    section_a = paper.questions.filter(
        section="A"
    ).order_by("sequence")

    section_b = paper.questions.filter(
        section="B"
    ).order_by("sequence")

    section_c = paper.questions.filter(
        section="C"
    ).order_by("sequence")

    return render(
        request,
        "materials/question_paper_detail.html",
        {
            "paper": paper,
            "section_a": section_a,
            "section_b": section_b,
            "section_c": section_c,
        }
    )

@login_required
def question_preview(request, paper_id): 
    paper = get_object_or_404( QuestionPaper, id=paper_id ) 
    questions = paper.questions.all().order_by( "sequence" ) 
    return render( 
        request, 
        "question_generator/generate_questions.html", 
        { 
            "paper": paper, "questions": questions, 
        } 
        )

@login_required
def question_generator_form(request, material_id):

    material = get_object_or_404(
        StudyMaterial,
        id=material_id,
        teacher=request.user
    )

    return render(
        request,
        "question_generator/generate_questions.html",
        {
            "material": material
        }
    )

@login_required
def download_answer_key_word(request, paper_id):

    paper = get_object_or_404(
        QuestionPaper,
        id=paper_id
    )

    section_a = paper.questions.filter(
        section="A"
    ).order_by("sequence")


    section_b = paper.questions.filter(
        section="B"
    ).order_by("sequence")

    section_c = paper.questions.filter(
        section="C"
    ).order_by("sequence")

    html = render_to_string(
        "question_generator/answer_key_word.html",
        {
            "paper": paper,
            "section_a": section_a,
            "section_b": section_b,
            "section_c": section_c,
        }
    )

    response = HttpResponse(
        html,
        content_type="application/msword"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="Answer_Key_{paper.id}.doc"'
    )

    return response

@login_required
def download_question_word(request, paper_id):

    paper = get_object_or_404(
        QuestionPaper,
        id=paper_id
    )

    section_a = paper.questions.filter(
        section="A"
    ).order_by("sequence")

    section_b = paper.questions.filter(
        section="B"
    ).order_by("sequence")

    section_c = paper.questions.filter(
        section="C"
    ).order_by("sequence")

    html = render_to_string(
        "materials/question_paper_detail.html",
        {
            "paper": paper,
            "section_a": section_a,
            "section_b": section_b,
            "section_c": section_c,
        },
        request=request
    )

    response = HttpResponse(
        html,
        content_type="application/msword"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="Question_Paper_{paper.id}.doc"'
    )

    return response

@login_required
def download_question_pdf(request, paper_id):

    paper = get_object_or_404(
        QuestionPaper,
        id=paper_id
    )

    section_a = paper.questions.filter(
        section="A"
    ).order_by("sequence")

    section_b = paper.questions.filter(
        section="B"
    ).order_by("sequence")

    section_c = paper.questions.filter(
        section="C"
    ).order_by("sequence")

    html = render_to_string(
        "materials/question_paper_detail.html",
        {
            "paper": paper,
            "section_a": section_a,
            "section_b": section_b,
            "section_c": section_c,
        },
        request=request
    )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="Question_Paper_{paper.id}.pdf"'
    )

    pisa_status = pisa.CreatePDF(
        html,
        dest=response
    )

    if pisa_status.err:
        return HttpResponse(
            "PDF generation failed"
        )

    return response

@login_required
def question_generation_status(request, material_id):

    try:
        material = StudyMaterial.objects.get(
            id=material_id,
            teacher=request.user
        )

        return JsonResponse({
            "status": material.status,
            "status_display": material.get_status_display(),
        })

    except StudyMaterial.DoesNotExist:

        return JsonResponse(
            {
                "status": "NOT_FOUND",
                "status_display": "Not Found",
            },
            status=404
        )