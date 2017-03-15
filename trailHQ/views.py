from django.shortcuts import render, get_object_or_404
from .models import SingletracksTrail

# Create your views here.

def trail_detail(request, pk):

    trail = get_object_or_404(SingletracksTrail, pk)
    return render(request, 'trailHQ/trail_detail.html',  {'trail': trail })


def all(request):
    trails =  SingletracksTrail.objects.all()
    return render(request, 'trailHQ/all.html', {'trails': trails})