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
        req_number = 1
        if req_number !=1:
            #UNCOMMENT IF YOUR GOING TO MASS GATHER TRAILS
            '''time.sleep(randint(60, 120))'''
        while (req_number != ""):
            if (req_number == 25):
                time.sleep(2)
            base_request = "https://www.trailforks.com/region/#{state}/trails"
            query_request = "/?page=#{req_number}"
            query = base_request
            if (req_number != 1):
                query = base_request + query_request

            trail_list = readFile(query, req_number, state)

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
            area_id = tryConvert(split_area[length])

            areadb= TFStateArea(stateId=dbstate, riding_area=area)
            areadb.save()


            #In case we need to do something with area_id, this is basic code, needs to be reqorked.
            # if (area_id == None):
            #else:
            #   areadb= TFStateArea(stateId=dbstate, riding_area=area, area_id=area_id )

            trailObj = TFid(areaId= areadb, name=trail_spaces, trail_id=trail[2], url=trail[3])

            trailObj.save()
    except Exception as e:
        print(e)


def readFile(request, num, state):
    try:
        import json
        filename = str(num) + state +"tf"
        with open ("trailHQ/RawData/#{filename}.txt") as content_file:
            content = content_file.read()

            return parseRequest(content, num, state)


    except Exception as e:
        print(e)
        time.sleep(25)
        return None






def makeRequest(request, num, state):
    '''
    with open("samp_resp_tf.txt", "r")as content_file:
        content = content_file.read()

    return parseRequest(content, num, state)
    '''

    #a bit of randomizing so I don't ddos the site

    if num!= 1:
        delay = randint(10, 45)
        time.sleep(delay)


    try:
        r = requests.get(request)
        trails = parseRequest(r, num, state)
        return  trails
    except Exception as e:
        print("Something went wrong with the request,  the url probably changed.")
        print(e)


# this method is a bit ugly, but it does the job and no longer throws exceptions
def parseRequest(response, num, state):
    trails = list()
    try:
        #html = response.content
        html = response

        filename = str(num) + state +"tf"

        '''
        with open("#{filename}.txt", 'w') as file:
            file.write(str(html))
        '''
        soup = BeautifulSoup(html, 'html.parser')

        count=0
        added = True
        for link in soup.find_all('tr'):
            # The first iteration will always have an empty list
            # this should catch the ending condtition and allow another
            # if statment to evaluate whether to send the list back or not
            if added != True & count > 0:
                break
            links = link.find_all('a')
            added = False
            if (links != []):

                #debug breakpoint
                #if count == 93:
                    #time.sleep(1)

                # the trail id is always in the html, it doesn't always allow you to search it though
                ul = link.find("ul", {"id": lambda x: x and x.startswith("trail_")})

                # this should prohibt exceptions from being thrown, and allow method to exit nicely
                # when we cannot find a ul tag that means that we have gone through all the trails on that page
                if (ul == None):
                    break

                trail_tag= ul['id']
                tag_split = trail_tag.split('_')
                trail_id = tag_split[1]
                trail = links[0].get('href')
                region = links[1].get('href')

                trail_split = trail.split('/')
                region_split = region.split('/')

                trail_name = trail_split[4]
                region_id = region_split[4]
                trails.append((trail_name, region_id, trail_id, trail))
                count = count+1

                # if it trys to add something that's not a trail, it throws an exception.
                # it should never get here if no more trails
                added = True

        if trails != []:
            return trails
        else:
            return None

    except Exception as e:

        # if we do throw exceptions we still want to return what we got.
        if trails != []:
            return trails
        else:
            return None


# Function to try converting string to int because not all TF have number id's
def tryConvert(stringConv):

     try:
           convert = int(stringConv)
           return convert
     except ValueError:
           return None
