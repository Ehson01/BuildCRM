from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('leads/', include('leads.urls')),
    path('contracts/', include('contracts.urls')),
]