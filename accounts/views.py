from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from .forms import UserCreateForm

class RegisterView(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('pages:home')
    template_name = 'registration/register.html'
