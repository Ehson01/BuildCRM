<<<<<<< HEAD
=======

from django.conf import settings
from django.conf.urls.static import static
>>>>>>> main
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
<<<<<<< HEAD
    path('admin/', admin.site.urls),
    path('leads/', include('leads.urls')),
    path('contracts/', include('contracts.urls')),
]
=======
    path("admin/", admin.site.urls),

    path("projects/", include("projects.urls")),
    path("stages/", include("stages.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
>>>>>>> main
