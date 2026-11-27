
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect

from django.views.generic import CreateView, DetailView, ListView,RedirectView
from contracts.models import Client
from django.urls import reverse
from .forms import LeadForm
from .models import Lead

from projects.models import HouseType



class LeadCreateView(CreateView):
    model = Lead
    form_class = LeadForm
    template_name = 'leads/lead_form.html'

    def form_valid(self, form):

        form.instance.house = get_object_or_404(
        HouseType,
        pk=self.kwargs['house_id']
        )
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('leads:list')



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


class LeadConvertView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        lead = get_object_or_404(Lead, pk=kwargs['pk'])

        if not lead.client:
            client, _ = Client.objects.get_or_create(
                phone=lead.phone,
                defaults={'full_name': lead.name,'email': lead.email,})
            lead.client = client


        lead.status = 'contract'

        lead.save()

        return reverse('contracts:contract_create_from_lead', kwargs={'lead_id': lead.pk})