from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from website.models import Beatmap


class IndexView(generic.TemplateView):
    template_name = 'website/index.html'


def listing(request, genre_id, language_id, page_id):
    try:
        mgr = Beatmap.objects.order_by('-date_ranked').select_related()
        if genre_id:
            mgr.filter(genre_id=genre_id)
        if language_id:
            mgr.filter(language_id=language_id)
        paginator = Paginator(mgr, 30)
        beatmaps = paginator.page(page_id)
    except EmptyPage or PageNotAnInteger as exception:
        raise Http404(exception)
    return render(request, 'website/listing.html',
                  {"genre_id": genre_id, "language_id": language_id, "page_id": page_id, "beatmaps": beatmaps})


class DisclaimerView(generic.TemplateView):
    template_name = 'website/disclaimer.html'


def item(request, beatmap_id):
    beatmap = get_object_or_404(Beatmap, pk=beatmap_id)
    return render(request, 'website/item.html', {"beatmap": beatmap})