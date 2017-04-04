from trailHQ.models import MtbProjStateId, MtbProjTrailId
from trailHQ.models import SingletracksTrail
from trailHQ.models import TFState, TFStateArea, TFid

omit_list=  [ 'the', 'in', 'trail', 'and' ]

# ALGORITHIM
    #first we'll try querying data based on the area to see if we can get a solid list of trails

    #take list of trails returned omit unecessary words and words less than 3 characters

    # preform like query on each of the big words
    # store id of results, and then make another query on next word. if the trail_ids in this queryset matches one of the others
        # that trail (s) id is a result to use

    # create match database from that and store id's of trails found from all 3 databases with trail name from singletracks as master name


# this will handle all the functioncalls for the other methods
def matchController(areaName, state, trailList ):
    trails = SingletracksTrail.objects.filter(city = areaName, state = state)

    #first we'll search for trails we've already found
    #getMatches(trails)
    #matchArea(areaName, state)

    matchTF(trails)


'''
 Going to focus on getting trail name matches working first

# this will attempt to get a list of trails from that area,
def matchArea(areaName,state):
    areaParts = areaName.split(' ')

    # this will always be list
    areaTrails = TFid.objects.filter()
'''

# this will search for previously matched trails
def getMatches(trails):
     print("do work")
     #TODO write table for storing matches

# builds the search lists, going to use them for both comparisons so might as well separate it out.
def buildMatchStrings(trails):
    searchNames = []
    partsToSearch = []
    for tr in trails:
        trName = tr.name

        partsToSearch.append(tr.key)
        # split the name up if it's multiple words
        for part in trName.split(' '):
            add = True
            #if it's in the omit list were not going to add it to the searching part
            for o in omit_list:
                if(part == o || len(part) < 3):

                    add = False
                    break

            if(add):
               partsToSearch.append(part)
        # appending the id to the last item of the list, to ensure all matches are found
        partsToSearch.append(tr.key)
        searchNames.append(partsToSearch)

    return searchNames

# this will preform the match for trailforks
def matchTF(searchNames):

    # search with each part of the search string of each trail
    # not the most efficient but that way i don't have to get fancy with django
    # compare based on id if they are a match or not.


    foundMatches=[]

    for trail in searchNames:
        elems = len(trail)

        # if there are more than 2 search terms then we can search on more than one word
        if (elems > 2):
            # going to do searches at most to start out
            results1 = TFid.objects.filter(name__contains = trail[0])

            results2 = TFid.objects.filter(name__contains= trail[1])
            for r1 in results1:
                for r2 in results2:

                    # Search by matches, and if one is found add that id later to build the
                    # match table
                    if (r1.id == r2.id):
                        foundMatches.append(r1.id)
        # if there are less than 3 then we only want to search on the first term because the second term is the
        # id of the trail from SingleTracks Table.
        # we also want to make sure we search by the whole word
        else:
            results = TFid.objects.filter(name__contains = ' '+trail[0] + ' ')

            if (not results == [] ):

                # for now we're going to store all trails that claim to match
                for r in results:
                    foundMatches.append(r)

    return foundMatches

# this will preform the match for mtbProj
def matchMTBP():

# this will create the relational match for that table
def createMatch():