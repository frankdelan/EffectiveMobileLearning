from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView, CreateView

from dog_app.forms import DogAddForm
from dog_app.models import Dog


# Create your views here.
class DogDetailView(DetailView):
    model = Dog
    template_name = 'dog_app/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dog'] = Dog.objects.filter(pk=self.kwargs['pk']).select_related('breed').first()
        return context


class DogListView(ListView):
    model = Dog
    template_name = 'dog_app/list.html'

#
# class DogCreateView(CreateView):
#     form_class = DogAddForm
#     model = Dog
#     template_name = 'dog_app/create.html'
#     success_url = '/list/'