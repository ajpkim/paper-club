from django.contrib import admin

from .models import Club, ClubMember

admin.site.register([Club, ClubMember])
