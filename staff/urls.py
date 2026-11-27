from django.urls import path
from .views import BrigadeListView, BrigadeCreateView, BrigadeUpdateView


urlpatterns = [
    path('brigades/', BrigadeListView.as_view(), name='brigade_list'),
    path('brigades/create/', BrigadeCreateView.as_view(), name='brigade_create'),
    path('brigades/<int:pk>/edit/', BrigadeUpdateView.as_view(), name='brigade_edit'),
]