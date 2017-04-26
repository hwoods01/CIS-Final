# coding: interpy

import requests
from bs4 import BeautifulSoup
from trailHQ.models import MtbProjStateId, MtbProjTrailId, MtbProjTr
import time
from random import randint
import re



'''these objects are used to help denote matching the states to the ID's
    these are really only here to serve as a reference incase something goes wrong
'''
states_though_f = {"alabama":8006784, "alaska":8006825, "arizona":8006911,  "california":8007121,  "connecticut":8007566, "delaware":8007678,}
states_through_L={"florida":8007709, "georgia":8007899, "hawaii":8007980, "idaho":8008046, "illnois":8008095,"indiana":8008178, "iowa":8008217,  "kentucky":800833, "louisiana":8008394,}
states_through_N ={"maine":8008431, "maryland":8008490, "massachusetts":8008552, "michigan":8008690, "minnesota":8008797, "montana":8009001, "nebraska":8009077, "nevada":8009101, "new_hampshire":8009200, "new_jersey":8009265, "new_mexico":8009312, "new_york":8009404, "north_carolina":8009607, "north_dakota":8009672,}
states_though_W ={"ohio":8009705,"oregon":8009849, "pennsylvania":8009971, "rhode_island":8010144, "south_carolina":8010166, "south_dakota":8010224, "tennessee":8010292, "texas":8010374, "utah":8010491, "vermont":8010585, "virginia":8010655, "washington":8010742, "west_virginia":8010938, "wisconsin":8010991, "wyoming":8011070}

states_1 = { "kansas":8008293, "missouri":8008930, "arkansas":8007054, "oklahoma":8009794,}

rebuildStates = {"colorado": 8007418, "oklahoma": 8009794 }

def requestBuilder():


        idList = rebuildStates.items()


        for tuple in idList:
            #UNCOMMENT THIS IF YOURE GOING TO MASS GATHER TRAILS
            #time.sleep(randint(60,120))
            req_number = 0
            while(req_number != ""):
                area_id = tuple[1]
                state_name = tuple[0]
                requestString = "https://www.mtbproject.com/ajax/area/#{area_id}/trails?idx=#{req_number}"
                trail_list = readFile(requestString, req_number, state_name)
                #if none then were out of trails for that state, which means we can move on to the next one
                if (trail_list == None):
                    req_number = ""
                    break
                else:
                    req_number = req_number+1
                    buildTable(trail_list, state_name, area_id)






def buildTable(tuple_list, state, area_id):
    mtbprojstate = MtbProjStateId.objects.get_or_create(state_id= area_id, state_name= state)
    for tuple in tuple_list:
        id = tuple[0]
        name_no_space = tuple[1]
        # other websites don't use dashes, so this should make it easier to do queries on
        name_spaces = name_no_space.replace('-', ' ')
        MtbProjTrailId.objects.update_or_create(mtrailId=id, name=name_spaces, stateId=mtbprojstate[0])




import json
def makeRequest(request, num, name):

    '''a bit of randomizing so I don't ddos the site'''

    delay = randint(10,45)

    time.sleep(delay)


    try:
        r = requests.get(request)
        return parseRequest(r, num, name)
    except Exception as e:
        print("Something went wrong with the request,  the url probably changed.")
        print(e)



def readFile(request, num, state):
    try:
        import json
        filename = str(num) + state
        with open ("trailHQ/RawData/#{filename}.txt") as content_file:
            content = content_file.read()
            json = json.loads(content)

            trailList = parseRequest(json, num, state)
            return trailList


    except Exception as e:
        print(e)
        time.sleep(25)
        return None


def parseRequest(response, num, name):
    try:
        #json_content = response.json()
        json_content = response
        #test json Response


        #writing raw response files in case they block me
        filename = str(num) + name

        '''
        import json
        with open("#{filename}.txt", 'w') as file:
            json.dump(json_content, file)
        '''
        html = json_content['markup']

        # if html is empty string then we know there are no more trails for that state
        if (html == ""):
            return None
        else:
            soup = BeautifulSoup(html, 'html.parser')
            trails = list()
            for link in soup.find_all('tr'):
                trail_string = link.get('data-href')
                trail_parts = trail_string.split('/')
                print(trail_parts)
                tuple = (trail_parts[4], trail_parts[5])
                trails.append((tuple))
            print(trails)
            return trails
    except Exception as e:
        print("Failed parsing JSON in the response")
        print(e)
        return None




def buildTrail(url, id):
    #url = "https://www.mtbproject.com/trail/346657"
    response = requests.get(url)
    html = response.content

    parsed = BeautifulSoup(html, 'html.parser')

    stats = parsed.find(id= "trail-stats-bar")
    statList = []
    for stat in stats.findAll("span"):
        statList.append(stripString(stat.text))
    # id's to take, [0, 4, 8, 12, 16, 20, 21]
    # [length, ascent, descent, top, low elev, avg_grade, max grade]

    orgList = []
    descr = stripString(parsed.find("div", class_="body").text)

    for org in parsed.find_all("p", class_="org"):
        orgList.append(org.text)
    orgs = ', '.join(orgList)
    try:
        trail = MtbProjTrailId.objects.get(mtrailId=id)
        MtbProjTr.objects.update_or_create(Mid= trail, description= descr, orgs= orgs, length=statList[0], ascent=statList[4], descent=statList[8], highElev=statList[12], lowElev=statList[16], avgGrade=statList[20], maxGrade=statList[21])
    except:
        print("The mtbproject trail does not exist, somebody should slap the developer")

def stripString(string):
    return re.sub('\s+', ' ', string).strip()
