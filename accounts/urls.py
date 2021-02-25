from django.contrib.auth import views as auth_views
from django.urls import path
from django.views import generic as generic_views

from accounts import forms, views

urlpatterns = [
    path(
        "login",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html",
            authentication_form=forms.UserAuthenticationForm,
        ),
        name="login",
    ),
    path(
        "logout",
        auth_views.LogoutView.as_view(template_name="home.html"),
        name="logout",
    ),
    path(
        "employees", views.ManageEmployeeView.as_view(), name="manage-employees"
    ),
    path(
        "profile/detail/(?P<pk>\d+)/$",
        views.ProfileDetail.as_view(),
        name="profile-detail",
    ),
    path(
        "profile/create/$", views.ProfileCreate.as_view(), name="profile-create"
    ),
    path(
        "profile/edit/(?P<pk>\d+)/$",
        views.ProfileUpdate.as_view(),
        name="profile-edit",
    ),
    path(
        "profile/lock/(?P<pk>\d+)/$",
        views.ProfileLock.as_view(),
        name="profile-lock",
    ),
    path(
        "profile/reset-password/(?P<pk>\d+)/$",
        views.ProfileResetPassword.as_view(),
        name="profile-reset-password",
    ),
]
