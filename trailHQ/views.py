from django.shortcuts import render, get_object_or_404

from .models import SingletracksTrail, TFid, TFStateArea, TFState,  MtbProjTrailId
from trailHQ.utils.trailForks_helper import requestBuilder as rebuildTf
from django.http import Http404
from trailHQ.utils.mtbpr_build import requestBuilder as rebuildmtbp
from django.template import RequestContext
from trailHQ.utils.ST_Helper import makeRequest
from trailHQ.utils.matcher import matchController
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

    ''' Uncommenting this will build more trail objects'''
    #requestBuilder()

    #rebuildmtbp()
    #rebuildTf()

    area = "Wichita"
    state = "Kansas"

#    makeRequest(area, state)
    matchController(area, state)


    trails =  SingletracksTrail.objects.all()
    mtbProj = MtbProjTrailId.objects.all()
    tfs = TFid.objects.all()
    print(trails.values())
    return render(request, 'trailHQ/all.html', {'trails': trails, 'tfs':tfs, 'mtbProj':mtbProj})

