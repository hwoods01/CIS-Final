from django.shortcuts import render, get_object_or_404

from .models import SingletracksTrail, TFid, TFStateArea, TFState,  MtbProjTrailId
from trailHQ.utils.trailForks_helper import requestBuilder as rebuildTf
from django.http import Http404
from trailHQ.utils.mtbpr_build import requestBuilder as rebuildmtbp
from trailHQ.utils.ST_Helper import makeRequest, tryFilter, STController
from trailHQ.utils.matcher import matchController
from trailHQ.utils.query import makeQuery
from trailHQ.utils.weather import GetWeather
from trailHQ.utils.generic_helper import combineDicts
#from trailHQ.utils.generic_helper import combineDicts
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


    type = 'AreaResults'
    area = "Crested Butte"
    state = "Colorado"
    weather = GetWeather(39.0693,-94.6716)
    results = makeQuery(type, [area, state])
    # if no results then were going to run the process to generate results
    #if results == []:
        #trails = STController(area, state)

        # this means we just added something to the database
    #matchController(area, state)
    combined = combineDicts(results)
    #results = makeQuery(type, [area, state])

    return render(request, 'trailHQ/area.html', {'results': combined, 'area': area, 'state': state, 'weather': weather} )








