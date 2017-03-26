from django.contrib import admin
from .models import SingletracksTrail, MtbProjTrailId, MtbProjStateId, TFid, TFStateArea, TFState

# Register your models here.

admin.site.register(SingletracksTrail)
admin.site.register(MtbProjStateId)
admin.site.register(MtbProjTrailId)
admin.site.register(TFState)
admin.site.register(TFStateArea)
admin.site.register(TFid)
