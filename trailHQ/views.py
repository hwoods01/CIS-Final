from django.shortcuts import render, get_object_or_404

from .models import SingletracksTrail, TFid, TFStateArea, TFState,  MtbProjTrailId, TFTrail, TFArea
from trailHQ.utils.trailForks_helper import requestBuilder as rebuildTf
from django.http import Http404
from trailHQ.utils.mtbpr_build import requestBuilder as rebuildmtbp, buildTrail
from trailHQ.utils.ST_Helper import makeRequest, tryFilter, STController
from trailHQ.utils.matcher import matchController
from trailHQ.utils.query import makeQuery, get_or_none
from trailHQ.utils.weather import GetWeather
from trailHQ.utils.generic_helper import combineDicts
from trailHQ.utils.trailForks_helper import TFRequest
#from trailHQ.utils.generic_helper import combineDicts
# Create your views here.



def trail_detail(request, pk):

    '''type = 'singtrail'

    results = makeQuery(type, pk)

    combine = combineDicts(results)
    TF = []
    TA = []
    MP = []
    if combine['MID'] != None:
        for res in combine['MID']:
            mtrail = get_or_none()
            if mtrail == None:
                #call mtbproject builder
            MP.append(mtrail)
        print('need to do something')
    elif combine['TID'] != None:

        for res in combine["TID"]:
            tftrail =get_or_none(TFTrail, res)
            if trail == None:
                # make call to tf request
            TF.append(tftrail)
    elif combine['AID'] != None:

        for res in combine['AID']:
            area = get_or_none(TFArea, res)
            if area == None:
                #make call to tf request
            TA.append(area)


    return render(request, 'trailHQ/trail_detail.html')

'''




def all(request):

    buildTrail("", 1)
    type = 'AreaResults'
    area = "Crested Butte"
    state = "Colorado"
    weather = GetWeather(39.0693,-94.6716)
    results = makeQuery(type, [area, state])

    #TFRequest('https://www.trailforks.com/region/miller-s-meadow-12543/','area', id)
    #TFRequest('https://www.trailforks.com/trails/trail-401/', 'test', id)
    # if no results then were going to run the process to generate results
    #if results == []:
        #trails = STController(area, state)

        # this means we just added something to the database
    #matchController(area, state)
    combined = combineDicts(results)
    #results = makeQuery(type, [area, state])

    return render(request, 'trailHQ/area.html', {'results': combined, 'area': area, 'state': state, 'weather': weather} )








