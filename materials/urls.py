
from django.urls import path
from .views import (
    MaterialListView,
    MaterialCreateView,
    MaterialUpdateView,
    MaterialRequestCreateView,
    MaterialRequestListView,
    MaterialRequestApproveView,
    MaterialRequestRejectView,
)


urlpatterns = [
    path('', MaterialListView.as_view(), name='material_list'),
    path('create/', MaterialCreateView.as_view(), name='material_create'),
    path('<int:pk>/edit/', MaterialUpdateView.as_view(), name='material_edit'),

    path('requests/', MaterialRequestListView.as_view(), name='request_list'),
    path('requests/create/<int:project_id>/', MaterialRequestCreateView.as_view(), name='request_create'),
    path('requests/<int:pk>/approve/', MaterialRequestApproveView.as_view(), name='request_approve'),
    path('requests/<int:pk>/reject/', MaterialRequestRejectView.as_view(), name='request_reject'),
]
