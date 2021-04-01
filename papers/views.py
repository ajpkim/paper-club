import pdb
import urllib.request as libreq
import re

import feedparser

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView

from .models import Author, AuthorPaper, Paper
from .forms import ArxivURLForm

# TODO Change HomeView to include the add paper form instead of button
class HomeView(ListView):
    template_name = 'papers/home.html'
    context_object_name = 'papers_list'  # TODO: Change to recent

    # TODO Convert this to return the most recent papers by proposal date
    # May need to use Proposals to do this and then return the unique papers
    def get_queryset(self):
        return Paper.objects.all()
    

class PaperDetailView(DetailView):
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

        # TODO: check if paper exists before creating
        paper.save()
        process_new_paper(paper, data)
        
        return HttpResponseRedirect(reverse('papers:paper-detail', kwargs={'pk': paper.id}))


# TODO
# class AddConfirmView(View):
# def AddConfirmView(request):
#     def get(self, request):
#         pass

# TODO add keywords
def process_new_paper(paper, data):
    for a in data.authors:
        author = Author(name=a)
        author.save()
        author_paper = AuthorPaper(paper=paper, author=author)
        author_paper.save()

        
    
########## arXiv API functions ##########
def get_pdf_url(data):
    """Extract the pdf url from arXiv API response"""
    for link in data.links:
        if ('title', 'pdf') in link.items():
            return link['href']
    return ''

# TODO: Use single regex
def clean_arxiv_paper_data(data):

    def remove_new_lines(s):
        s = s.replace("\n", " ")
        pat = r" {2,5}"
        s = re.sub(pat, " ", s)
        return s

    data.title = remove_new_lines(data.title)
    data.summary = remove_new_lines(data.summary)
    # Convert "YYYY-MM-DDTHH:MM:SSZ" to "YYYY-MM-DD"
    data.published = data.published[0:9]
    # Extract author names
    data.authors = [author['name'] for author in data.authors]
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
    return clean_arxiv_paper_data(data)


