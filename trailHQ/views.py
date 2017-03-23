from django.shortcuts import render, get_object_or_404
from .models import SingletracksTrail
from trailHQ.utils.ST_Helper import makeRequest #THIS WILL BE USED WHEN i HAVE CALLS TO MAKE
from django.http import Http404
from django.template import RequestContext
# Create your views here.

def trail_detail(request, pk):
    try:
        trail = SingletracksTrail.objects.filter(name__icontains=pk)
        if trail:
            print(trail.values())
            return render(request, 'trailHQ/trail_detail.html', {'trails': trail})
        else:
            print("Not found")
    except SingletracksTrail.DoesNotExist:
        raise Http404("Does not extist")
        #ST_Helper.makeRequest()






def all(request):
    makeRequest('Wichita', 'Kansas')
    trails =  SingletracksTrail.objects.all()
    print(trails.values())
    return render(request, 'trailHQ/all.html', {'trails': trails})
