from django.shortcuts import render
from django.views import generic
# Create your views here.


class IndexView(generic.TemplateView):
    template_name = 'website/index.html'


def listing(request):
    return render(request, 'website/listing.html')


class DisclaimerView(generic.TemplateView):
    template_name = 'website/disclaimer.html'