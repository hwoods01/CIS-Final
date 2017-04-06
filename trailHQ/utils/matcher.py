# coding: interpy


from trailHQ.models import MtbProjStateId, MtbProjTrailId
from trailHQ.models import SingletracksTrail
from trailHQ.models import TFState, TFStateArea, TFid
from collections import Counter

from django.db import connection
from collections import namedtuple

omit_list=  [ 'the', 'in', 'trail', 'and', 'for', 'tr', 'park' ]
word =""
state = ""



querylist = {
    'area': "select * from trailHQ_tfstatearea  tfa join trailHQ_tfstate  tfs on tfa.stateId_id = tfs.Sid where tfa.riding_area LIKE %s AND tfs.state_name = %s",
    'trail':  "select * from trailHQ_tfid tf join trailHQ_tfstatearea tfa on tf.areaId_id = tfa.Aid join trailHQ_tfstate tfs on tfa.stateId_id = tfs.Sid where tf.name LIKE %s and tfs.state_name = %s",
}


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
    matches = matchForks(searchTrails, matches, state.lower())

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

        trName = tr.name.lower()


        # split the name up if it's multiple words
        for part in trName.split(' '):
            add = True
            #if it's in the omit list were not going to add it to the searching part
            for o in omit_list:
                if(part == o or len(part) < 3):

                    add = False
                    break

            if(add):
               partsToSearch.append(part)
        # appending the id to the last item of the list, to ensure all matches are found and we can keep track of the order
        partsToSearch.append(tr.key)

        searchNames.append(partsToSearch)
        partsToSearch = []

    return searchNames


# Method:
#   check trail,
#   check no s
#       check area
#       check no area s




def matchForks(searchNames, foundMatches, state):



    for trail in searchNames:

        found = []
        # getting the id of the singletracks trail for matching.
        elems = len(trail)
        trailId = trail[elems - 1]

        # the trail has multiple dominant strings
        if elems > 1:
            found = tfQueryMultiple('trail', trail, state)

            dups = checkDups(found)

            if len(dups) < 1:
                found = tfQueryMultiple('area', trail, state)

                dups = checkDups(found)
        # there is just one dominant string which requires being handled a bit different
        else:
            found = tfQuerySingle('trail', trail, state)

            dups = checkDups(found)

            if len(dups) < 1:
                found = tfQuerySingle('area', trail, state)

                dups = checkDups(found)

        # this will give us the duplicate values in the list which hopefully there are some. :/


        if len(dups) >1:
            # cry and insert flag to tell us later that this one didn't want to be matched.
            dups.insert(0, "flag")

        # put the all the duplicate matches (hopefully one) to be with singletracks id
        foundMatches[trailId] = dups
    return foundMatches


def checkDups(found):
    dups = [k for k, v in Counter(found).items() if v > 1]
    return dups


def tfQueryMultiple(type, trail, state):

    id = ""
    if type == 'trail':
        id = 'Tid'
    else:
        id = 'Aid'



    # list to store results in
    found = []


    # every word in trail except the last one because it is the id for singletracks
    with connection.cursor() as cursor:
        for word in trail[:-1]:
            query = querylist[type]
            params = ['%'+word+'%',state]
            cursor.execute(query,params)
            results = dictfetchall(cursor)
            if results == []:

                # if we didn't get any hits were going to try removing an 's' if it's the last character and trying again.
                if word[len(word) - 1] == 's':
                    word = word[:-1]
                    query = querylist[type]
                    params = ['%'+word+'%', state]
                    cursor.execute(query, params)
                    results = dictfetchall(cursor)

            # can only enter if we have results
            if results != []:
                # add all the results to the list.
                for r in results:
                    found.append(id[0]+str(r[id]))
        if len(found) < 2: return []

        else : return found

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns,row))
        for row in cursor.fetchall()
    ]


# could probably combine the two functions but its not worth the effort currently
def tfQuerySingle(type, trail, state):

    found = []

    # add spaces to try and match on whole word
    word = ' ' + trail[0] + ' '
    query = querylist[trail]
    query= query.format(word,state)
    results = exec(query)
    if results == None:

        # if we didn't get any hits were going to try removing an 's' if it's the last character and trying again.
        if trail[0][len(trail[0]) - 1] == 's':
            word = ' ' + trail[0][:-1] + ' '

            query = querylist[type]
            query = query.format(word, state)
            results = exec(querylist[type])
            # add all the results to the list.
            for r in results:
                found.append({id[0]:r.id})

        return found



'''
# this will preform the match for mtbProj
#def matchMTBP():

# this will create the relational match for that table
#def createMatch():


'''