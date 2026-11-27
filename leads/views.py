from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import CreateView, DetailView, ListView
from contracts.models import Client
from .forms import LeadForm
from .models import Lead


class LeadCreateView(CreateView):
    model = Lead
    form_class = LeadForm
    template_name = 'leads/lead_form.html'

    def form_valid(self, form):
        House = apps.get_model('houses', 'House')
        form.instance.house = get_object_or_404(House, pk=self.kwargs['house_id'])
        form.save()
        return redirect('leads:list')


class LeadListView(LoginRequiredMixin, ListView):
    model = Lead
    template_name = 'leads/lead_list.html'
    context_object_name = 'leads'


class LeadDetailView(LoginRequiredMixin, DetailView):
    model = Lead
    template_name = 'leads/lead_detail.html'
    context_object_name = 'lead'

    def post(self, request, *args, **kwargs):
        lead = self.get_object()
        lead.status = request.POST.get('status', lead.status)
        lead.save()
        return redirect('leads:detail', pk=lead.pk)


class LeadConvertView(LoginRequiredMixin, View):
    def get(self, request, pk):
        lead = get_object_or_404(Lead, pk=pk)

        if not lead.client:
            client, _ = Client.objects.get_or_create(
                phone=lead.phone,
                defaults={
                    'full_name': lead.name,
                    'email': lead.email,
                }
            )
            lead.client = client

        lead.status = 'in_progress'
        lead.save()
        return redirect('contracts:contract_create_from_lead', lead_id=lead.pk)