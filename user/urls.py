from django.urls import path
from user.views import auth_view
from user.views import dashboard_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Dashboard
    path("", dashboard_view.DashboardView.as_view()),
    # Auth
    path("signin/", auth_view.SignInView.as_view(), name="signin"),
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(template_name="auth/password_reset.html"),
        name="reset_password",
    ),
    path(
        "password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="auth/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "user/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="auth/set_password.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "user/password_reset_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="auth/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
