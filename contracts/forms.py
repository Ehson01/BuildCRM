from django import forms
from django.db.models import Sum
from .models import Client,Contract,Payment
from decimal import Decimal

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['full_name', 'phone', 'email', 'passport_data', 'address']


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['client', 'house', 'number', 'total_amount', 'end_date', 'status']
        widgets = {'end_date': forms.DateInput(attrs={'type': 'date'}),}

    def clean_tottal_amount(self):
        amount = self.cleaned_data.get('total_amount')
        if amount is None and amount<=0:
            raise forms.ValidationError('Total amount must be greater than 0.')
        return amount


class PaymentForm(forms.ModelForm):
    model = Payment
    fields = ['amount', 'payment_method', 'payment_date', 'comment']
    widgets = {'payment_date': forms.DateInput(attrs={'type': 'date'}),}

    def __init__(self, *args, contract=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.contract = contract

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is None:
            return amount

        if amount <= 0:
            raise forms.ValidationError('Payment amount must be greater than 0.')

        if self.contract:
            paid = self.contract.payments.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
            remaining = self.contract.total_amount - paid
            if amount > remaining:
                raise forms.ValidationError(
                    f'Payment amount cannot exceed the remaining balance ({remaining:.2f}).'
                )

        return amount