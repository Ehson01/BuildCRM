from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, ListView
from leads.models import Lead
from .forms import ClientForm, ContractForm, PaymentForm
from .models import Client, Contract, Payment


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'contracts/client_list.html'
    context_object_name = 'clients'


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'contracts/client_form.html'

    def form_valid(self, form):
        client = form.save()
        return redirect('contracts:client_detail', pk=client.pk)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'contracts/client_detail.html'
    context_object_name = 'client'


class ContractListView(LoginRequiredMixin, ListView):
    model = Contract
    template_name = 'contracts/contract_list.html'
    context_object_name = 'contracts'


class ContractCreateView(LoginRequiredMixin, CreateView):
    model = Contract
    form_class = ContractForm
    template_name = 'contracts/contract_form.html'

    def get_initial(self):
        lead_id = self.kwargs.get('lead_id')
        if lead_id:
            lead = get_object_or_404(Lead, pk=lead_id)
            return {'client': lead.client, 'house': lead.house}
        return {}

    def form_valid(self, form):
        lead_id = self.kwargs.get('lead_id')
        if lead_id:
            lead = get_object_or_404(Lead, pk=lead_id)
            form.instance.lead = lead
            lead.status = 'contract'
            lead.save()

        contract = form.save()
        return redirect('contracts:contract_detail', pk=contract.pk)


class ContractDetailView(LoginRequiredMixin, DetailView):
    model = Contract
    template_name = 'contracts/contract_detail.html'
    context_object_name = 'contract'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        payments = self.object.payments.all()
        paid_amount = payments.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        context['payments'] = payments
        context['paid_amount'] = paid_amount
        context['remaining_amount'] = self.object.total_amount - paid_amount
        context['form'] = kwargs.get('form') or PaymentForm(contract=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        payment = Payment(contract=self.object)
        form = PaymentForm(request.POST, instance=payment,contract=self.object)

        if form.is_valid():
            form.save()
            paid = self.object.payments.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
            if paid >= self.object.total_amount:
                self.object.status = 'paid'
                self.object.save()
            return redirect('contracts:contract_detail', pk=self.object.pk)

        return self.render_to_response(self.get_context_data(form=form))