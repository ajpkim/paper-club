from django.contrib import admin

from .models import Author, KeyWord, Paper, PaperAuthor, PaperKeyWord

admin.site.register([Author, KeyWord, Paper, PaperAuthor, PaperKeyWord])
