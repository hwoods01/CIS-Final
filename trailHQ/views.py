from django.shortcuts import render, get_object_or_404

from .models import SingletracksTrail, TFid, TFStateArea, TFState,  MtbProjTrailId, TFTrail, TFArea, MtbProjTr
from trailHQ.utils.trailForks_helper import requestBuilder as rebuildTf
from django.http import Http404, HttpResponseRedirect
from trailHQ.utils.mtbpr_build import requestBuilder as rebuildmtbp, buildTrail
from trailHQ.utils.ST_Helper import makeRequest, tryFilter, STController
from trailHQ.utils.matcher import matchController
from trailHQ.utils.query import makeQuery, get_or_none
from trailHQ.utils.weather import GetWeather
from trailHQ.utils.generic_helper import combineDicts
from trailHQ.utils.detailBuilder import singleController, multipleController
from trailHQ.utils.trailForks_helper import TFRequest
#from trailHQ.utils.generic_helper import combineDicts
from trailHQ.forms import SearchForm

# Create your views here.



def trail_detail(request, pk):



    type = 'singtrail'
    results = makeQuery(type, [pk])
    if results == None:
        return Http404
    singleController(results)

    Sresults = makeQuery("STsing", [pk])
    TFresults = makeQuery("TFsing", [pk])
    TFAresults = makeQuery("TFAsing", [pk])
    MBresults = makeQuery("MBsing", [pk])

    return render(request, 'trailHQ/trail_detail.html', {'ST': Sresults[0], 'TF': TFresults, 'TFA': TFAresults, 'MTBP': MBresults})




def area(request):

    form = SearchForm(request.GET)
    #buildTrail("", 1)
    if form.is_valid():

        city = form.cleaned_data['city']
        state = form.cleaned_data['state']
        radius = form.cleaned_data['radius']

        area = "Crested Butte"
        #state = "Colorado"

        combined = []
        results = tryFilter(city, state)

        # no call has been made to that location yet
        if not results:
            if STController(city, state):
                matchController(city, state)
                results = tryFilter(city, state)

            # bad input
            else:
                return 404

        trail = results[0]

        weather = GetWeather(trail.latitude, trail.longitude)
        type = 'AreaResults'
        results = makeQuery(type, [city, state])

        # TFRequest('https://www.trailforks.com/region/miller-s-meadow-12543/','area', id)
        # TFRequest('https://www.trailforks.com/trails/trail-401/', 'test', id)

        # matchController(area, state)
        combined = combineDicts(results)
        # results = makeQuery(type, [area, state])
        key = combined[0]["key"]
        return render(request, 'trailHQ/area.html',
                      {'results': combined, 'area': area, 'state': state, 'weather': weather})

    else:
        HttpResponseRedirect('index.html')








def index(request):

    return render(request, 'trailHQ/index.html' )








