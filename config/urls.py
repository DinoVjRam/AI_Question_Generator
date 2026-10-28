from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("Syllabus/", include("materials.urls")),
    path("questions/",include("question_generator.urls"),),
    # path("question-generator/",include("question_generator.urls"),),
    # path("export/", include("document_export.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)