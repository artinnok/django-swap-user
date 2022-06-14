from django.contrib import admin

from swap_user.base_forms import BaseUserOptionalFieldsForm, BaseUserRequiredFieldsForm


class BaseUserAdmin(admin.ModelAdmin):
    """
    Admin base class with overridden `add` and `edit` forms.
    """

    add_form_class = BaseUserRequiredFieldsForm
    change_form_class = BaseUserOptionalFieldsForm

    def get_form(self, request, obj=None, change=False, **kwargs):
        if change:
            form = self.change_form_class
        else:
            form = self.add_form_class

        kwargs["form"] = form

        return super().get_form(request, obj, change, **kwargs)
