from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return HttpResponse("<h1>VOTE VOTE VOTE</h1>")
