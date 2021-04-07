import random

from django.shortcuts import render
from django.views.generic import TemplateView

from papers.utils import get_random_arxiv_paper

class HomeView(TemplateView):
    template_name = 'pages/home.html'

    
class AboutView(TemplateView):
    template_name = 'pages/about.html'

