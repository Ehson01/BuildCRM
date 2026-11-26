from django.views import View
from django.shortcuts import render, redirect
from .models import Brigade
from .forms import BrigadeForm
from django.shortcuts import get_object_or_404


class BrigadeListView(View):
    def get(self, request):
        brigades = Brigade.objects.all()

        return render(request, 'staff/brigade_list.html', {
            'brigades': brigades
        })
        
    
class BrigadeCreateView(View):
    def get(self, request):
        form = BrigadeForm()

        return render(request, 'staff/brigade_form.html', {
            'form': form
        })

    def post(self, request):
        form = BrigadeForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('brigade_list')

        return render(request, 'staff/brigade_form.html', {
            'form': form
        })
        
        

class BrigadeUpdateView(View):
    def get(self, request, pk):
        brigades = get_object_or_404(Brigade, pk=pk)
        form = BrigadeForm(instance=brigades)

        return render(request, 'staff/brigade_form.html', {
            'form': form
        })

    def post(self, request, pk):
        brigades = get_object_or_404(Brigade, pk=pk)
        form = BrigadeForm(request.POST, instance=brigades)

        if form.is_valid():
            form.save()
            return redirect('brigade_list')

        return render(request, 'staff/brigade_form.html', {
            'form': form
        })