from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView

from .models import Author, AuthorPaper, Paper
from .forms import ArxivURLForm
from .utils import get_arxiv_paper_data, get_random_arxiv_paper, process_arxiv_data, process_paper_url




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
        paper, authors = process_paper_url(url)
        return HttpResponseRedirect(reverse('papers:paper-detail', kwargs={'pk': paper.id}))

    
def random_paper_view(request):
    paper = get_random_arxiv_paper()
    # breakpoint()
    return render(request, 'papers/paper_detail.html', {'paper': paper})
    

# TODO
# class AddConfirmView(View):
# def AddConfirmView(request):
#     def get(self, request):
#         pass

# TODO add keywords



