from django.urls import path
from .views import MaterialListView, MaterialCreateView, MaterialUpdateView


urlpatterns = [
    path('', MaterialListView.as_view(), name='material_list'),
    path('create/', MaterialCreateView.as_view(), name='material_create'),
    path('<int:pk>/edit/', MaterialUpdateView.as_view(), name='material_edit'),
]