from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models, transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from projects.models import ConstructionProject
from .models import Material, MaterialRequest
from .forms import MaterialForm, MaterialRequestForm


class MaterialListView(View):
    def get(self, request):
        materials = Material.objects.all()

        search = request.GET.get('search')
        low_stock = request.GET.get('low_stock')

        if search:
            materials = materials.filter(name__icontains=search)

        if low_stock:
            materials = materials.filter(quantity__lt=models.F('min_quantity'))

        return render(request, 'materials/material_list.html', {
            'materials': materials,
            'search': search,
            'low_stock': low_stock
        })


class MaterialCreateView(View):
    def get(self, request):
        form = MaterialForm()

        return render(request, 'materials/material_form.html', {
            'form': form
        })

    def post(self, request):
        form = MaterialForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('material_list')

        return render(request, 'materials/material_form.html', {
            'form': form
        })


class MaterialUpdateView(View):
    def get(self, request, pk):
        materials = get_object_or_404(Material, pk=pk)
        form = MaterialForm(instance=materials)

        return render(request, 'materials/material_form.html', {
            'form': form
        })

    def post(self, request, pk):
        materials = get_object_or_404(Material, pk=pk)
        form = MaterialForm(request.POST, instance=materials)

        if form.is_valid():
            form.save()
            return redirect('material_list')

        return render(request, 'materials/material_form.html', {
            'form': form
        })
        
        

class MaterialRequestCreateView(LoginRequiredMixin, View):
    def get(self, request, project_id):
        project = get_object_or_404(ConstructionProject, pk=project_id)

        if request.user.role != 'foreman' or project.foreman_id != request.user.id:
            return redirect('material_list')

        form = MaterialRequestForm()

        return render(request, 'materials/request_form.html', {
            'form': form,
            'project': project
        })

    def post(self, request, project_id):
        project = get_object_or_404(ConstructionProject, pk=project_id)

        if request.user.role != 'foreman' or project.foreman_id != request.user.id:
            return redirect('material_list')

        form = MaterialRequestForm(request.POST)

        if form.is_valid():
            material_request = form.save(commit=False)
            material_request.project = project
            material_request.requested_by = request.user
            material_request.save()

            messages.success(request, 'Request created successfully.')
            return redirect('request_list')

        return render(request, 'materials/request_form.html', {
            'form': form,
            'project': project
        })


class MaterialRequestListView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role == 'manager':
            requests = MaterialRequest.objects.all()
        elif request.user.role == 'foreman':
            requests = MaterialRequest.objects.filter(
                project__foreman=request.user
            )
        else:
            return redirect('material_list')

        return render(request, 'materials/request_list.html', {
            'requests': requests
        })


class MaterialRequestApproveView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if request.user.role != 'manager':
            return redirect('request_list')

        with transaction.atomic():
            material_request = get_object_or_404(
                MaterialRequest.objects.select_for_update(),
                pk=pk
            )

            if material_request.status != 'pending':
                messages.error(request, 'Request already processed.')
                return redirect('request_list')

            material = Material.objects.select_for_update().get(
                pk=material_request.material_id
            )

            if material_request.quantity > material.quantity:
                messages.error(request, 'Not enough material in stock.')
                return redirect('request_list')

            material.quantity -= material_request.quantity
            material.save()

            material_request.status = 'approved'
            material_request.save()

        messages.success(request, 'Request approved.')
        return redirect('request_list')


class MaterialRequestRejectView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if request.user.role != 'manager':
            return redirect('request_list')

        material_request = get_object_or_404(MaterialRequest, pk=pk)

        if material_request.status == 'pending':
            material_request.status = 'rejected'
            material_request.save()
            messages.success(request, 'Request rejected.')

        return redirect('request_list')
