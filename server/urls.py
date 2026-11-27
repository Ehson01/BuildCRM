from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('accounts.urls')),
    path('staff/', include('staff.urls')),
    path('materials/', include('materials.urls')),
    path('projects/', include('projects.urls')),
    path('stages/', include('stages.urls')),
    path('contracts/', include('contracts.urls')),
    path('leads/', include('leads.urls')),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )