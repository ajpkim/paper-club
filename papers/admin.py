from django.contrib import admin

from .models import Author, AuthorPaper, KeyWord, KeyWordPaper, Paper

admin.site.register([Author, AuthorPaper, KeyWord, KeyWordPaper, Paper])
