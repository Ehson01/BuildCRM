
from django import forms

from .models import Stage, StageReport


class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = [  # noqa: RUF012
            "title",
            "description",
            "status",
            "order",
            "start_date",
            "end_date",
        ]

        widgets = {  # noqa: RUF012
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class StageReportForm(forms.ModelForm):
    class Meta:
        model = StageReport
        fields = [  # noqa: RUF012
            "image",
            "description",
        ]
 