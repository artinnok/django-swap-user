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

        try:
            password_1 = self.cleaned_data["password_1"]
            password_2 = self.cleaned_data["password_2"]
        except KeyError:
            return cleaned_data

        if password_1 != password_2:
            raise forms.ValidationError(
                message="Passwords should be same", code="password_should_be_same",
            )

        return cleaned_data

    def save(self, commit=False):
        instance = super().save(commit)

        try:
            password_1 = self.cleaned_data["password_1"]
            instance.set_password(password_1)
        except KeyError:
            pass
        finally:
            instance.save()

        return instance
