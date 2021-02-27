from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path

from accounts import forms, views

app_name = "accounts"

urlpatterns = [
    path(
        "<int:pk>/",
        login_required(views.AccountDetails.as_view()),
        name="details",
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html",
            authentication_form=forms.UserAuthenticationForm,
        ),
        name="login",
    ),
    path(
        "logout/",
        login_required(
            auth_views.LogoutView.as_view(template_name="home.html")
        ),
        name="logout",
    ),
    path("list/", login_required(views.ListAccounts.as_view()), name="list"),
    path(
        "create/", login_required(views.CreateAccount.as_view()), name="create"
    ),
    path(
        "update/<int:id>/",
        login_required(views.UpdateAccount.as_view()),
        name="update",
    ),
    path(
        "lock/<int:id>/",
        login_required(views.LockAccount.as_view()),
        name="lock",
    ),
    path(
        "reset-password/<int:id>/",
        login_required(views.ResetPassword.as_view()),
        name="reset-password",
    ),
]
