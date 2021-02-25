import rolepermissions
from django import views
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.messages import views as message_views
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic as generic_views

from accounts import models, roles


class ManageEmployeeView(generic_views.ListView):
    template_name = "accounts/employee-list.html"
    context_object_name = "employees"
    queryset = models.User.objects.filter(
        groups__name__in=[roles.StoreEmployee.get_name()]
    )

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class ProfileDetail(generic_views.DetailView):
    model = models.User
    template_name = "accounts/profile-detail.html"


class ProfileCreate(
    message_views.SuccessMessageMixin, generic_views.edit.CreateView
):
    model = models.User
    fields = [
        "username",
        "first_name",
        "last_name",
        "email",
        "birth_date",
        "address",
    ]
    template_name = "accounts/profile-create.html"
    success_url = reverse_lazy("manage-employees")
    success_message = "%(first_name)s %(last_name)s's profile has been created."

    def form_valid(self, form):
        response = super().form_valid(form)
        rolepermissions.roles.assign_role(
            self.object, roles.StoreEmployee.get_name()
        )

        return response


class ProfileUpdate(
    message_views.SuccessMessageMixin, generic_views.edit.UpdateView
):
    model = models.User
    fields = ["first_name", "last_name", "email", "birth_date", "address"]
    template_name = "accounts/profile-update.html"
    success_url = reverse_lazy("manage-employees")
    success_message = (
        "%(first_name)s %(last_name)s's profile was updated successfully."
    )


class ProfileLock(views.View):
    def get(self, request, pk):
        user = models.User.objects.get(pk=pk)
        return render(request, "accounts/profile-lock.html", {"user": user})

    def post(self, request, pk):
        user = models.User.objects.get(pk=pk)
        user.locked = True
        user.save()

        messages.success(
            request, f"{user.get_full_name()}'s profile has been locked."
        )

        return redirect("manage-employees")


class ProfileResetPassword(
    message_views.SuccessMessageMixin, generic_views.edit.UpdateView
):
    model = models.User
    fields = ["password"]
    template_name = "accounts/profile-password-reset.html"
    success_url = reverse_lazy("home")
    success_message = "Your password has been reset"


class ProfileResetPassword(views.View):
    def get(self, request, pk):
        user = models.User.objects.get(pk=pk)
        return render(
            request, "accounts/profile-reset-password.html", {"user": user}
        )

    def post(self, request, pk):
        new_password = models.User.objects.make_random_password()
        user = models.User.objects.get(pk=pk)
        user.set_password(new_password)
        user.save()

        messages.success(
            request, f"{user.get_full_name()}'s password has been reset."
        )

        return render(
            request,
            "accounts/profile-reset-password.html",
            {"user": user, "new_password": new_password},
        )
