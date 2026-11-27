
from django import forms
from .models import Material, MaterialRequest


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'description', 'quantity', 'min_quantity', 'unit', 'price']


class MaterialRequestForm(forms.ModelForm):
    class Meta:
        model = MaterialRequest
        fields = ['material', 'quantity']
