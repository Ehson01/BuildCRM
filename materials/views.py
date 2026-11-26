from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import Material
from .forms import MaterialForm
from django.db import models


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