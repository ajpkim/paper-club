from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', include('pages.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('clubs/', include('clubs.urls')),
    path('papers/', include('papers.urls')),
]
