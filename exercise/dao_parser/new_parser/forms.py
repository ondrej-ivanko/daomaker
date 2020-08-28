from django import forms
from new_parser.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("parsed_url",)
