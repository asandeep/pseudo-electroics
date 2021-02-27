import rolepermissions
from django import views
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.messages import views as message_views
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic as generic_views
from rolepermissions import mixins as rolepermissions_mixins

from accounts import models, roles


class ListAccounts(rolepermissions_mixins.HasRoleMixin, generic_views.ListView):
    """A view that lists all accounts where role is StoreEmployee.

    The view provides various options to manage employees like edit account
    details, reset password, lock account etc. This view is only accessible to
    store owners.
    """

    allowed_roles = roles.StoreOwner
    context_object_name = "accounts"
    queryset = models.User.objects.filter(
        groups__name__in=[roles.StoreEmployee.get_name()]
    )
    template_name = "accounts/list.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class AccountDetails(
    rolepermissions_mixins.HasPermissionsMixin, generic_views.DetailView
):
    """A view that render the account details.

    View permission on account is required to access this view.
    """

    model = models.User
    required_permission = roles.Permission.ACCOUNT__VIEW.value
    template_name = "accounts/detail.html"


class CreateAccount(
    rolepermissions_mixins.HasRoleMixin,
    message_views.SuccessMessageMixin,
    generic_views.edit.CreateView,
):
    """A view that allows logged-in user to create new account.

    The view is only accessible to store owner to create account for new
    employees.
    """

    allowed_roles = roles.StoreOwner
    fields = [
        "username",
        "first_name",
        "last_name",
        "email",
        "birth_date",
        "address",
    ]
    model = models.User
    template_name = "accounts/create.html"
    success_message = "%(first_name)s %(last_name)s's profile has been created."
    success_url = reverse_lazy("accounts:list")

    def form_valid(self, form):
        """
        Override base implementation to assign appropriate role once account has
        been created.
        """
        response = super().form_valid(form)
        # Assign store employee role to created user.
        rolepermissions.roles.assign_role(self.object, roles.StoreEmployee)

        return response


class UpdateAccount(
    rolepermissions_mixins.HasPermissionsMixin,
    message_views.SuccessMessageMixin,
    generic_views.edit.UpdateView,
):
    """A view that allows account details to be updated.

    Logged-in user should have edit account permission to be able to access this
    view.
    """

    model = models.User
    fields = ["first_name", "last_name", "email", "birth_date", "address"]
    required_permission = roles.Permission.ACCOUNT__UPDATE.value
    template_name = "accounts/update.html"
    success_message = (
        "%(first_name)s %(last_name)s's profile was updated successfully."
    )
    success_url = reverse_lazy("accounts:list")


class LockAccount(rolepermissions_mixins.HasRoleMixin, views.View):
    """
    View that allows store owner to lock an employee and block his access to
    account.
    """

    allowed_roles = roles.StoreOwner

    def get(self, request, id):
        """Renders confirmation screen."""
        user = models.User.objects.get(pk=id)
        return render(request, "accounts/lock.html", {"user": user})

    def post(self, request, id):
        """Updates user's account to locked state."""
        user = models.User.objects.get(pk=id)
        user.locked = True
        user.save()

        messages.success(
            request, f"{user.get_full_name()}'s profile has been locked."
        )

        return redirect("accounts:list")


class ResetPassword(rolepermissions_mixins.HasRoleMixin, views.View):
    """
    View that allows store owner to reset password for any of his employee's
    account.
    """

    allowed_roles = roles.StoreOwner

    def get(self, request, id):
        """Renders the reset password confirmation page.

        Args:
            request (django.http.HttpRequest): The current request.
            id (int): ID of user whose account's password will be reset.
        """
        user = models.User.objects.get(pk=id)
        return render(request, "accounts/reset-password.html", {"user": user})

    def post(self, request, id):
        """
        Post method that generates a new random password and set to user's
        account.
        The new password will be rendered on screen and owner can share the same
        to employee offline.

        Args:
            request (django.http.HttpRequest): The current request.
            id (int): ID of user whose account's password will be reset.
        """
        new_password = models.User.objects.make_random_password()
        user = models.User.objects.get(pk=id)
        user.set_password(new_password)
        user.save()

        messages.success(
            request, f"{user.get_full_name()}'s password has been reset."
        )

        return render(
            request,
            "accounts/reset-password.html",
            {"user": user, "new_password": new_password},
        )
