from django.http import FileResponse
import threading
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import StudyMaterial
from .forms import (
    StudyMaterialForm,
    QuestionGenerationForm
)
from .services import process_uploaded_material
from django.http import JsonResponse
from ai_engine.services.syllabus_service import analyze_material_units
from document_export.services import PDFExportService
from question_generator.models import QuestionPaper
from question_generator.services import QuestionGenerationService



@login_required
def material_list(request):
    materials = StudyMaterial.objects.all().order_by("-uploaded_at")

    return render(request, "materials/material_list.html", {
        "materials": materials
    })


# @login_required
# def material_upload(request):
#     if request.method == "POST":
#         form = StudyMaterialForm(request.POST, request.FILES)

#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.teacher = request.user
#             obj.document_type = "SYLLABUS"
#             obj.status = "UPLOADED"
#             obj.save()

#             # ONLY TEXT EXTRACTION NOW (no AI)
#             process_uploaded_material(obj)

#             return redirect("material_list")

#     else:
#         form = StudyMaterialForm()

#     return render(request, "materials/material_upload.html", {"form": form})

@login_required
def material_upload(request):

    if request.method == "POST":

        form = StudyMaterialForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            obj = form.save(commit=False)

            obj.teacher = request.user
            obj.document_type = "SYLLABUS"
            obj.status = "UPLOADED"

            obj.save()


            # -----------------------------------------
            # Start processing in background
            # -----------------------------------------

            thread = threading.Thread(
                target=process_uploaded_material,
                args=(obj.id,),
                daemon=True
            )

            thread.start()


            # -----------------------------------------
            # Return immediately
            # -----------------------------------------

            return redirect("material_list")

    else:

        form = StudyMaterialForm()


    return render(
        request,
        "materials/material_upload.html",
        {
            "form": form
        }
    )

@login_required
def analyze_syllabus(request, material_id):

    material = StudyMaterial.objects.get(id=material_id)

    if not material.extracted_text:
        return JsonResponse({"error": "No text found"})

    result = analyze_material_units(material)

    return JsonResponse(result)

@login_required
def view_units(request, material_id):

    material = StudyMaterial.objects.get(id=material_id)

    return render(request, "materials/view_units.html", {
        "material": material,
        "units": material.units_json
    })

# @login_required
# def generate_questions(request, material_id):

#     material = get_object_or_404(
#         StudyMaterial,
#         id=material_id,
#         teacher=request.user
#     )

#     if not material.units_json:

#         return JsonResponse({
#             "error": "Units not found. Please analyze syllabus first."
#         }, status=400)


#     try:

#         # -------------------------------------------------
#         # Mark question generation as started
#         # -------------------------------------------------

#         # material.status = "GENERATING_QUESTIONS"

#         # material.save(
#         #     update_fields=["status"]
#         # )


#         # -------------------------------------------------
#         # Get generation parameters
#         # -------------------------------------------------

#         units = [
#             u["title"]
#             for u in material.units_json["units"]
#         ]

#         difficulty = request.GET.get(
#             "difficulty",
#             "medium"
#         )

#         bloom = request.GET.get(
#             "bloom",
#             "understand"
#         )

#         count = int(
#             request.GET.get(
#                 "count",
#                 10
#             )
#         )


#         # -------------------------------------------------
#         # AI + RAG QUESTION GENERATION
#         # -------------------------------------------------

#         paper = QuestionGenerationService.generate_and_save_paper(

#             teacher=request.user,

#             material=material,

#             units=units,

#             difficulty=difficulty,

#             bloom=bloom,

#             question_type="Mixed",

#             marks=10,

#             count=count,

#         )


#         # -------------------------------------------------
#         # Generation completed successfully
#         # -------------------------------------------------

#         material.status = "QUESTIONS_GENERATED"

#         material.save(
#             update_fields=["status"]
#         )


#         return JsonResponse({

#             "message":
#                 "Questions generated successfully",

#             "paper_id":
#                 paper.id,

#             "status":
#                 material.status,

#             "questions":
#                 list(
#                     paper.questions.values(
#                         "question",
#                         "answer",
#                         "unit_no",
#                         "marks"
#                     )
#                 )

#         })


#     except Exception as e:

#         # -------------------------------------------------
#         # Generation failed
#         # -------------------------------------------------

#         material.status = "FAILED"

#         material.save(
#             update_fields=["status"]
#         )


#         return JsonResponse(
#             {
#                 "error": str(e),
#                 "status": "FAILED"
#             },
#             status=500
#         )
    
# @login_required
# def unit_selection(request, material_id):

#     material = StudyMaterial.objects.get(id=material_id)


#     if request.method == "POST":

#         selected_units = request.POST.getlist("units")

#         # later:
#         # call RAG + Ollama here


#         return redirect("question_paper_list", material_id)


    # return render(
    #     request,
    #     "materials/unit_selection.html",
    #     {
    #         "material": material,
    #         "units": material.units_json.get("units", [])
    #     }
    # )

# @login_required
# def generate_questions_api(request, material_id):

#     material = StudyMaterial.objects.get(
#         id=material_id
#     )


#     if request.method == "POST":

#         data = request.POST


#         # ==========================
#         # Selected Units
#         # ==========================

#         selected_units = data.getlist(
#             "units"
#         )


#         # ==========================
#         # AI Settings
#         # ==========================

#         difficulty = data.get(
#             "difficulty",
#             "medium"
#         )

#         bloom = data.get(
#             "bloom",
#             "understand"
#         )

#         question_type = data.get(
#             "question_type",
#             "mixed"
#         )


#         # ==========================
#         # Question Pattern
#         # ==========================

#         marks = data.getlist(
#             "marks[]"
#         )

#         counts = data.getlist(
#             "counts[]"
#         )


#         question_pattern = []


#         for mark, count in zip(
#             marks,
#             counts
#         ):

#             question_pattern.append(
#                 {
#                     "marks": int(mark),
#                     "count": int(count)
#                 }
#             )


#         # ==========================
#         # Generate using RAG
#         # ==========================

#         paper = QuestionGenerationService.generate_and_save_paper(

#             teacher=request.user,

#             material=material,

#             units=selected_units,

#             difficulty=difficulty,

#             bloom=bloom,

#             question_type=question_type,

#             question_pattern=question_pattern,

#         )


#         # material.status = "QUESTIONS_GENERATED"

#         # material.save()


#         return JsonResponse({

#             "paper_id": paper.id,

#             "message":
#             "Questions generated successfully"

#         })
    
# @login_required
# def question_paper_list(request, material_id):
#     material = StudyMaterial.objects.get(id=material_id)
#     papers = QuestionPaper.objects.filter(study_material=material).order_by("-created_at")
#     return render(request, "materials/question_paper_list.html", {
#         "material": material,
#         "papers": papers
#     })

# @login_required
# def question_paper_detail(request, paper_id):
#     paper = QuestionPaper.objects.get(id=paper_id)
#     return render(request, "materials/question_paper_detail.html", {
#         "paper": paper
#     })

# @login_required
# def export_question_paper_pdf(request, paper_id):
#     paper = QuestionPaper.objects.get(id=paper_id)
#     questions = paper.questions.all().order_by("sequence")

#     file_path = f"media/question_paper_{paper.id}.pdf"
#     PDFExportService.export_question_paper(paper, questions, file_path)

#     return FileResponse(open(file_path, "rb"), as_attachment=True)

# @login_required
# def ai_question_generator(request):

#     materials = StudyMaterial.objects.all().order_by("-uploaded_at")

#     return render(request, "materials/ai_question_generator.html", {
#         "materials": materials
#     })
