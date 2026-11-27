
from django import forms

from .models import ConstructionProject, HouseType


class HouseTypeForm(forms.ModelForm):
    class Meta:
        model = HouseType
        fields = [
            "title",
            "description",
            "area",
            "floors",
            "price",
            "image",
        ]


class ConstructionProjectForm(forms.ModelForm):
    class Meta:
        model = ConstructionProject
        fields = [
            "title",
            "address",
            "house_type",
            "foreman",
            "start_date",
            "end_date",
            "status",
        ]

        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }
