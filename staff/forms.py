from django import forms
from .models import Brigade


class BrigadeForm(forms.ModelForm):
    class Meta:
        model = Brigade
        fields = ['name', 'foreman', 'project']