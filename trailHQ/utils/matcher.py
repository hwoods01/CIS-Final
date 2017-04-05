from trailHQ.models import MtbProjStateId, MtbProjTrailId
from trailHQ.models import SingletracksTrail
from trailHQ.models import TFState, TFStateArea, TFid
from collections import Counter

omit_list=  [ 'the', 'in', 'trail', 'and', 'for' ]

# ALGORITHIM
    #first we'll try querying data based on the area to see if we can get a solid list of trails

    #take list of trails returned omit unecessary words and words less than 3 characters

    # preform like query on each of the big words
    # store id of results, and then make another query on next word. if the trail_ids in this queryset matches one of the others
        # that trail (s) id is a result to use

    # create match database from that and store id's of trails found from all 3 databases with trail name from singletracks as master name


# this will handle all the functioncalls for the other methods
def matchController(areaName, state):
    trails = SingletracksTrail.objects.filter(city__iexact = areaName, state__iexact = state)

    #first we'll search for trails we've already found
    #getMatches(trails)
    #matchArea(areaName, state)
    print(len(trails))
    matches = dict()

    searchTrails = buildMatchStrings(trails)
    matches = matchTF(searchTrails, matches,state)

    for m in matches:
        print(m)


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


        # split the name up if it's multiple words
        for part in trName.split(' '):
            add = True
            #if it's in the omit list were not going to add it to the searching part
            for o in omit_list:
                if(part == o or len(part) < 3):

                    add = False
                    break

            if(add):
               partsToSearch.append(part.lower())
        # appending the id to the last item of the list, to ensure all matches are found and we can keep track of the order
        partsToSearch.append(tr.key)

        searchNames.append(partsToSearch)
        partsToSearch = []

    return searchNames

# this will preform the match for trailforks
def matchTF(searchNames, foundMatches, state):

    # search with each part of the search string of each trail
    # not the most efficient but that way i don't have to get fancy with django
    # compare based on id if they are a match or not.




    for trail in searchNames:
        elems = len(trail)

        # this is the id of the trail from singletracks
        trailId = trail[elems-1]

        matchCount = 0
        foundMultiple = False

        # if there are more than 2 search terms then we can search on more than one word
        if (elems > 1):
            # going to do searches at most to start out
            results1 = TFid.objects.filter(name__icontains = trail[0], areaId__stateId__state_name__iexact=state)

            results2 = TFid.objects.filter(name__icontains= trail[1], areaId__stateId__state_name__iexact=state)

            # if either is empty, it could be the there was punctuation or it could be
            # that the area is the name of the trail
            if len(results1)==0 or len(results2)==0:

                # a good number of trails will have the area as the name of the trail singletracks will return.
                checkAreaForTrails(trail, state)

            # TODO need to define what happens here
            # TODO maybe look into set operators to do this.
            for r1 in results1:
                for r2 in results2:

                    # Search by matches, and if one is found add that id later to build the
                    # match table
                    if (r1.id == r2.id):
                        if(matchCount > 1 and foundMultiple):
                            foundMatches[trailId].insert(0, "flag")
                            foundMatches[trailId].append(r1.id)
                            matchCount += 1
                        else:
                            # going to store matches as a dictionary with trailid for
                            # singletracks being the key and a list of the other 2 as value
                            foundMatches[trailId].append(r1.id)
                            matchCount+=1

                            # we set this to true because we should only have one match
                            foundMultiple=True

        # if there are less than 3 then we only want to search on the first term because the second term is the
        # id of the trail from SingleTracks Table.
        # we also want to make sure we search by the whole word
        else:
            results = TFid.objects.filter(name__contains = ' '+trail[0] + ' ')

            if (not results == [] ):

                if (len(results) > 1):
                    # going to literally attach flag to show that the we had more than one result
                    foundMatches[trailId].append("flag")
                for r in results:
                    # for now we're going to store all trails that claim to match
                    foundMatches[trailId].append(r)

    return foundMatches

# this will preform the match for mtbProj
#def matchMTBP():

# this will create the relational match for that table
#def createMatch():



# this method will check to see if the trail name is actually the area name for trailforks
def checkAreaForTrails(trail, state):

    foundIds = []
    for word in trail[:-1]:

        word = word
        results = TFStateArea.objects.filter(riding_area__icontains=word, stateId__state_name__iexact=state)

        for r in results:
            foundIds.append(r.id)

    # don't care that this duplicates
    # grasping at straws
    if foundIds == []:
        for word in trail[:-1]:

            # if this doesn't evaluate to true we're screwed
            # taking the s off the string if it's the last character
            if word[len(word)- 1] == 's':
                word = word[:-1]
                results = TFStateArea.objects.filter(riding_area__icontains=word, stateId__state_name=state.lower())
                for r in results:
                    foundIds.append(r.id)
            else :
                print('A trail by this name could not be found: ' + word)


    # found this here http://stackoverflow.com/questions/11236006/identify-duplicate-values-in-a-list-in-python
    dups = [k for k,v in Counter(foundIds).items() if v> 1]

    if len(dups) >1:
        # cry
        return None
    return dups