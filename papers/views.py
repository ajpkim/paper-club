import pdb
import urllib.request as libreq
import re

import feedparser

from django.http import HttpResponse, HttpResponseRedirect
# from django.shortcuts import render
from django.urls import reverse, reverse_lazy
# from django.views import View
from django.views.generic import CreateView, FormView, ListView

from .models import Paper
from .forms import ArxivURLForm

class HomeView(ListView):
    template_name = 'papers/home.html'
    context_object_name = 'papers_list'  # TODO: Change to recent

    # TODO: Convert this to return the most recent papers by proposal date
    # May need to use Proposals to do this and then return the unique papers
    def get_queryset(self):
        return Paper.objects.all()
    
class PaperDetailView(ListView):
    model = Paper

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx


class AddPaperView(FormView):
    
    form_class = ArxivURLForm
    success_url = reverse_lazy('papers/home')
    template_name = 'papers/add.html'

    def form_valid(self, form):
        url = form.cleaned_data['url']
        data = get_arxiv_paper_data(url)
        paper = Paper(url=url,
                      title=data.title,
                      abstract=data.summary,
                      pub_date=data.published,
                      pdf_url=get_pdf_url(data),
                      )
        
        return HttpResponseRedirect(form.cleaned_data['url'])

    
########## arXiv API functions ##########
def get_pdf_url(data):
    """Extract the pdf url from arXiv API response"""
    pdf_url = ""
    for link in data.links:
        if ('title', 'pdf') in link.items():
            pdf_url = link['href']
    return pdf_url

# TODO: Use single regex
def clean_arxiv_paper_data(data):

    def remove_new_lines(s):
        s = s.replace("\n", " ")
        pat = r" {2,5}"
        s = re.sub(pat, " ", s)
        return s

    data.title = remove_new_lines(data.title)
    data.summary = remove_new_lines(data.summary)

    return data

def get_arxiv_paper_data(url):
    """
    Query the arXiv.org API to retrieve metadata on the paper given by
    the url and return it in a feedparser dict.
    
    - url: is a url to a paper hosted at  arxiv.org with form:
      "https://arxiv.org/abs/cond-mat/0207270v3".
    """
    base, arxiv_id = url.split('abs/')
    base += 'api/query?id_list='
    query = base + arxiv_id
    response = libreq.urlopen(query)
    feed = feedparser.parse(response)
    data = feed.entries[0]
    data.summary = data.summary.replace("\n", " ")
    return clean_arxiv_paper_data(data)


