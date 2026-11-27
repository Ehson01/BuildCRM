from django.urls import path
from . import views

app_name = 'contracts'

urlpatterns = [
    path('clients/', views.ClientListView.as_view(), name='client_list'),
    path('clients/create/', views.ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/', views.ClientDetailView.as_view(), name='client_detail'),

    path('', views.ContractListView.as_view(), name='contract_list'),
    path('create/', views.ContractCreateView.as_view(), name='contract_create'),
    path('create/from-lead/<int:lead_id>/', views.ContractCreateView.as_view(), name='contract_create_from_lead'),
    path('<int:pk>/', views.ContractDetailView.as_view(), name='contract_detail'),
]