# coding: interpy

import requests
from bs4 import BeautifulSoup
from trailHQ.models import TFState, TFStateArea, TFid
import time
from random import randint
import re


'''these objects will help loop get the specific trail numbers of all the trails'''
#states_though_f = {"alabama": , "alaska": , "arizona":, :, "california":, :, "connecticut":, "delaware":, }
#states_through_L={"florida":, "georgia":, "hawaii":, "idaho":, "illnois":,"indiana":, "iowa":, :, "kentucky": , "louisiana":, }
#states_through_N ={"maine":, "maryland":, "massachusetts":, "michigan":, "minnesota":, :,"montana":, "nebraska":, "nevada":, "nebraska":, "nevada":, "new_hampshire":, "new_jersey":, "new_mexico":, "new_york":, "north_carolina":, "north_dakota":,}
#states_though_W ={"ohio":, :,"oregon":, "pennsylvania":, "rhode_island":, "south_carolina":, "south_dakota":, "tennessee":, "texas":, "utah":, "vermont":, "virginia":, "washington":, "west_virginia":, "wisconsin":, "wyoming":}


small_test_states = ["colorado", "kansas", "oklahoma", "missouri", "arkansas"]

def requestBuilder():
    for state in small_test_states:
        #time.sleep(randint(60, 120))
        req_number = 0
        while (req_number != ""):
            if (req_number == 25):
                time.sleep(2)
            base_request = "https://www.trailforks.com/region/#{state}/trails"
            query_request = "/trails/?page=#{req_number}"
            query = base_request
            if (req_number != 0):
                query = base_request + query_request

            trail_list = makeRequest(query, req_number, state)

            # if none then were out of trails for that state, which means we can move on to the next one
            if (trail_list == None):
                req_number = ""
                break
            else:
                req_number = req_number + 1
                buildTable(trail_list, state)


def buildTable(trails, state):
    try:
        dbstate = TFState(state_name= state)
        dbstate.save()
        for trail in trails:
            area = trail[1]
            #check if last bit is int
                #if not put back on rest of string
                #if is put into db as id for trail/area
            #need to grab everything but the last off the split for this to work.
            #put the
            split_area = area.split('-')
            trail_spaces = trail[0].replace('-', ' ')
            length = len(split_area) -1
            # if it has an id, it's in the last spot of the area string
            areadb = None
            area_id = tryConvert(split_area[length])
            if (area_id == None):
                areadb= TFStateArea(stateId=dbstate, riding_area=area)
            else:
                areadb= TFStateArea(stateId=dbstate, riding_area=area, area_id=area_id )

            trailObj = TFid(areaId= areadb, name=trail_spaces, trail_id=trail[2], url=trail[3])
            areadb.save()
            trailObj.save()
    except Exception as e:
        print(e)









def makeRequest(request, num, state):
    '''
    with open("samp_resp_tf.txt", "r")as content_file:
        content = content_file.read()

    return parseRequest(content, num, state)
    '''

    #a bit of randomizing so I don't ddos the site


    #delay = randint(10, 45)

    #time.sleep(delay)


    try:
        r = requests.get(request)
        trails = parseRequest(r, num, state)
        return  trails
    except Exception as e:
        print("Something went wrong with the request,  the url probably changed.")
        print(e)


def parseRequest(response, num, state):

    try:
        html = response.content
        #html = response
        filename = str(num) + state +"tf"

        with open("#{filename}.txt", 'w') as file:
            file.write(str(html))

        soup = BeautifulSoup(html, 'html.parser')
        trails = list()
        count=0
        for link in soup.find_all('tr'):
            links = link.find_all('a')
            if (links != []):
                if count ==98:
                    time.sleep(1)
                ul = link.find("ul", {"id": lambda x: x and x.startswith("trail_")})
                trail_tag= ul['id']
                tag_split = trail_tag.split('_')
                trail_id = tag_split[1]
                trail = links[0].get('href')
                region = links[1].get('href')

                print(trail)
                print(region)

                trail_split = trail.split('/')
                region_split = region.split('/')
                print(trail_split)
                print(region_split)
                trail_name = trail_split[4]
                region_id = region_split[4]
                trails.append((trail_name, region_id, trail_id, trail))
                count = count+1

                #we know trailforks will never return more than 100 trails at a time
                if count == 99:
                    return trails
        return trails

    except Exception as e:
        print(e)



# Function to try converting string to int because not all TF have number id's
def tryConvert(stringConv):

     try:
           convert = int(stringConv)
           return convert
     except ValueError:
           return None
