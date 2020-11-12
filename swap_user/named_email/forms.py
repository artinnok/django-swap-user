from django import forms

from swap_user.named_email.models import NamedEmailUser


class NamedUserEmailForm(forms.ModelForm):
    password_1 = forms.CharField(
        label="Enter a new password.", widget=forms.PasswordInput, required=True,
    )
    password_2 = forms.CharField(
        label="Repeat a new password.", widget=forms.PasswordInput, required=True,
    )

    class Meta:
        model = NamedEmailUser
        exclude = ["password"]

    def clean(self):
        cleaned_data = super().clean()
        password_1 = self.cleaned_data["password_1"]
        password_2 = self.cleaned_data["password_2"]

        if password_1 != password_2:
            raise forms.ValidationError(
                message="Passwords should be same", code="password_should_be_same",
            )

        return cleaned_data

    def save(self, commit=False):
        instance = super().save(commit)
        password_1 = self.cleaned_data["password_1"]

        instance.set_password(password_1)
        instance.save()

        return instance
