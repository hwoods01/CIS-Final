from django.shortcuts import render, get_object_or_404

from .models import SingletracksTrail, TFid, TFStateArea, TFState,  MtbProjTrailId
from trailHQ.utils.trailForks_helper import requestBuilder as rebuildTf
from django.http import Http404
from trailHQ.utils.mtbpr_build import requestBuilder as rebuildmtbp
from django.template import RequestContext
from trailHQ.utils.ST_Helper import makeRequest, tryFilter, STController
from trailHQ.utils.matcher import matchController
from trailHQ.utils.query import makeQuery
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

    #rea = "Wichita"
    #state = "Colorado"

    #STController(area, state)
    #matchController(area, state)

    area(request)
    '''
    trails =  SingletracksTrail.objects.all()
    mtbProj = MtbProjTrailId.objects.all()
    tfs = TFid.objects.all()
    print(trails.values())
    #return render(request, 'trailHQ/all.html', {'trails': trails, 'tfs':tfs, 'mtbProj':mtbProj})'''


'''

sql = {"select st.name as Single, tfi.name as TrailForks, mtb.name as MPRoj, tfa.riding_area as TFArea from trailHQ_matches match
	join trailHQ_singletrackstrail st on match.SingleTracksId_id =  st.key
	left join trailHQ_tfid tfi on match.TfTrailId_id = tfi.Tid
	left join trailHQ_mtbprojtrailid mtb on match.MTrailId_id = mtb.mtrailId
	left join trailHQ_tfstatearea tfa on match.TfAreaId_id = tfa.riding_area
	where st.city = 'Crested Butte' and st.state = 'Colorado' }'''

queries = {"Area": "select st.key, st.name as SingleTracks, tfi.name as TrailForks, mtb.name as MtbProject, tfa.riding_area as TFArea from trailHQ_matches match join trailHQ_singletrackstrail st on match.SingleTracksId_id =  st.key left join trailHQ_tfid tfi on match.TfTrailId_id = tfi.Tid left join trailHQ_mtbprojtrailid mtb on match.MTrailId_id = mtb.mtrailId	left join trailHQ_tfstatearea tfa on match.TfAreaId_id = tfa.riding_area where (select key from trailHQ_singletrackstrail where city = %s and state = %s)"
           }

def area(request):

    type = 'AreaResults'
    area = "Crested Butte"
    state = "Colorado"

    results = makeQuery(type, [area, state])

    # if no results then were going to run the process to generate results
    if results == []:
        trails = STController(area, state)
        if trails:
            # this means we just added something to the database
            matchController(area, state)

        else :
            # no results return 404
            return 404
    #results = makeQuery(type, [area, state])
    return render(request, 'trailHQ/area.html', {'results': results, 'area': area, 'state': state} )


