from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, ListView

from .models import Paper
# from .forms import ProposalForm

class HomeView(ListView):
    template_name = 'papers/home.html'
    context_object_name = 'papers_list'  # TODO: Change to recent

    # TODO: Conver this to return the most recent papers by proposal date
    # May need to use Proposals to do this and then return the unique papers
    def get_queryset(self):
        return Paper.objects.all()
    
    
class ProposeView(CreateView):
    pass
    # form_class = ProposalForm
    # success_url = reverse('')
    # template_name = 'papers/propose.html'

