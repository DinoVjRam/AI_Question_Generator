from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.forms import CustomPasswordChangeForm
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("logout/", views.logout_view, name="logout"),
    path(
    "password-change/",
    auth_views.PasswordChangeView.as_view(
        template_name="accounts/password_change.html",
        success_url="/password-change/done/"
    ),
    name="password_change"
    ),
    path(
    "password-change/done/",
    auth_views.PasswordChangeDoneView.as_view(
        template_name="accounts/password_change_done.html"
    ),
    name="password_change_done"
    ),
    path(
    "password-change/",
    auth_views.PasswordChangeView.as_view(
        form_class=CustomPasswordChangeForm,
        template_name="accounts/password_change.html",
        success_url="/password-change/done/"
    ),
    name="password_change"
    ),
]