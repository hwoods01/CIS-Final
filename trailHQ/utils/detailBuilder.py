# coding: interpy

from trailHQ.models import TFTrail, TFArea, MtbProjTr, TFStateArea
from trailHQ.utils.query import get_or_none
from trailHQ.utils.trailForks_helper import TFRequest
from django.core.exceptions import ObjectDoesNotExist
from trailHQ.utils.mtbpr_build import buildTrail
#TFTrail: 'TID', TFArea: 'AID', MtbProjTr: 'Mid'
def singleController(results):
    idList = {  TFTrail: 'Tid', TFArea: 'Aid', MtbProjTr: 'Mid'}

    for row in results:
        for model, id in idList.items():
            if row[id] is not None:
                trail = get_or_none(model, row[id], id)

                if trail == None:
                    url = ''
                    if id == 'Tid':
                        url = row['TFI_URL']
                    decideURL(id, row[id], url)

# this will decide whether the program needs to build a url or not
# in the case of trailforks trail we know the id already
# in the case of trailforks area we need to get the name
# in the case of mtbproject the trail id is the same as the one in the database
# identifier is the database identifier not the id itself
def decideURL(identifier, id, url):
    if identifier == 'Aid':
        try:
            area = TFStateArea.objects.get(Aid=id)
            name = area.riding_area
            url = "https://www.trailforks.com/region/#{name}/"
            TFRequest(url, identifier, id)
        except ObjectDoesNotExist:
            print("That area could not be found its ID is :" + id)
    elif identifier == 'Mid':
        url = "https://www.mtbproject.com/trail/#{id}"
        buildTrail(url, id)
    else:
        TFRequest(url, identifier, id)


def multipleController(combined):
    idList = {TFTrail: 'TID', TFArea: 'AID', MtbProjTr: 'MID' }

    for model, id in idList.items():
        if combined[id] is not None:

            # check to see if those results are a list
            if len(combined[id]) >1:
                for item in combined[id]:
                    url = ''
                    if  id == 'TID':
                        url = combined['TFI_URL']
                    decideURL(id, item, url)
            else:
                url = ''
                if id == 'TID':
                    url = combined['TFI_URL']
                decideURL(id, combined[id], url)