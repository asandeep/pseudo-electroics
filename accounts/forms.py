from django import forms
from django.contrib.auth import forms as auth_forms

from accounts import models


class UserAuthenticationForm(auth_forms.AuthenticationForm):
    """
    Override default authentication form to add vaildation for user whose
    account is locked by store owner.
    """

    def confirm_login_allowed(self, user):
        if user.locked:
            raise forms.ValidationError(
                "User account is locked. Please contact store owner."
            )

        return super().confirm_login_allowed(user)


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = models.User
        fields = ("birth_date", "address")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = auth_forms.ReadOnlyPasswordHashField()

    class Meta:
        model = models.User
        fields = ("birth_date", "address")

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
