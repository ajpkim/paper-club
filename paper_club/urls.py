from django.contrib import admin
from django.urls import include, path

from .settings import ADMIN_URL

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', include('pages.urls')),
    path('accounts/', include('accounts.urls')),
    path(f'{ADMIN_URL}/', admin.site.urls),
    path('clubs/', include('clubs.urls')),
    path('papers/', include('papers.urls')),
]
