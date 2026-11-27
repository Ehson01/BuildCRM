from django import forms
from .models import Lead

class LeadFrom(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name','phone','email','comment']

        