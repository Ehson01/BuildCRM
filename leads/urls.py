from django.urls import path
from . import views

app_name = 'leads'

urlpatterns = [
    path('', views.LeadListView.as_view(), name='list'),
    path('create/<int:house_id>/', views.LeadCreateView.as_view(), name='create'),
    path('<int:pk>/', views.LeadDetailView.as_view(), name='detail'),
    path('<int:pk>/convert/', views.LeadConvertView.as_view(), name='convert'),
]