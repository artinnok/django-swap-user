from django import forms


class BaseUserForm(forms.ModelForm):
    password_1 = forms.CharField(
        label="Enter a new password.", widget=forms.PasswordInput, required=False,
    )
    password_2 = forms.CharField(
        label="Repeat a new password.", widget=forms.PasswordInput, required=False,
    )

    class Meta:
        exclude = ["password"]

    def clean(self):
        cleaned_data = super().clean()

        password_1 = self.cleaned_data["password_1"]
        password_2 = self.cleaned_data["password_2"]

        if not password_1 or not password_2:
            return cleaned_data

        if password_1 != password_2:
            raise forms.ValidationError(
                message="Passwords should be same", code="password_should_be_same",
            )

        return cleaned_data

    def save(self, commit=False):
        instance = super().save(commit)
        password_1 = self.cleaned_data["password_1"]

        if password_1:
            instance.set_password(password_1)

        instance.save()

        return instance
