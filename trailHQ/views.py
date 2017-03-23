from django.shortcuts import render, get_object_or_404
from .models import SingletracksTrail, CityState
from .forms import SearchForm
#from utils import ST_Helper #THIS WILL BE USED WHEN i HAVE CALLS TO MAKE
from django.http import Http404
from django.template import RequestContext
import operator

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
    print(trails.values())
    return render(request, 'trailHQ/all.html', {'trails': trails})

class CitySearchListVIew(SearchListView):

def search(request):

    if request.method == "POST":
        form = SearchForm(request.POST, instance=post)

    else:


    return render(request, 'trailHQ/index.html', {'form': form} )