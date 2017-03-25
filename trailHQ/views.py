from django.shortcuts import render, get_object_or_404
from .models import SingletracksTrail, MtbProjTrailId
from trailHQ.utils.trailForks_helper import requestBuilder
from django.http import Http404
from trailHQ.utils.mtbpr_build import requestBuilder
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




    trails =  SingletracksTrail.objects.all()
    mtbProj = MtbProjTrailId.objects.all()

    return render(request, 'trailHQ/all.html', {'trails': trails})