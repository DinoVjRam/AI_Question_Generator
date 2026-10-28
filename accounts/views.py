from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from materials.models import StudyMaterial
from question_generator.models import QuestionPaper, Question


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")


@login_required
def dashboard_view(request):

    # -----------------------------------------
    # Teacher's syllabus materials
    # -----------------------------------------

    total_materials = StudyMaterial.objects.filter(
        teacher=request.user
    ).count()


    # -----------------------------------------
    # Teacher's generated question papers
    # -----------------------------------------

    total_papers = QuestionPaper.objects.filter(
        teacher=request.user
    ).count()


    # -----------------------------------------
    # Teacher's generated questions
    # -----------------------------------------

    total_questions = Question.objects.filter(
        paper__teacher=request.user
    ).count()


    # -----------------------------------------
    # Recent generated papers
    # -----------------------------------------

    recent_papers = (
        QuestionPaper.objects
        .filter(
            teacher=request.user
        )
        .select_related(
            "study_material"
        )
        .order_by(
            "-created_at"
        )[:5]
    )


    context = {

        "total_materials": total_materials,

        "total_papers": total_papers,

        "total_questions": total_questions,

        "recent_papers": recent_papers,

    }


    return render(
        request,
        "accounts/dashboard.html",
        context
    )


def logout_view(request):
    logout(request)
    return redirect("login")