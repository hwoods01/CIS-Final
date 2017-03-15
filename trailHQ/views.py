from django.shortcuts import render, get_object_or_404
from .models import SingletracksTrail
#from trailHQ.apiReq import  THIS WILL BE USED WHEN i HAVE CALLS TO MAKE

# Create your views here.

def trail_detail(request, pk):
    try:
        trail = SingletracksTrail.objects.get( pk= pk)
        return render(request, 'trailHQ/trail_detail.html', {'trail': trail})
    except SingletracksTrail.DoesNotExist:





def all(request):
    trails =  SingletracksTrail.objects.all()
    return render(request, 'trailHQ/all.html', {'trails': trails})