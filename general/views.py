from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class IndexView(TemplateView):
    template_name = 'general/index.html'

class AboutView(TemplateView):
    pass 

class ContactView(TemplateView):
    pass