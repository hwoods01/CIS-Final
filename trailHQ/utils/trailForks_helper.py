# coding: interpy

import requests
from bs4 import BeautifulSoup

import time
from random import randint


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
                #buildTable(trail_list, state)


#def buildTable(trails, state):




def makeRequest(request, num, state):

    with open("samp_resp_tf.txt", "r")as content_file:
        content = content_file.read()


    return parseRequest(content, num, state)
    '''a bit of randomizing so I don't ddos the site


    delay = randint(10, 45)

    time.sleep(delay)


    try:
        r = requests.get(request)
        return parseRequest(r, num, state)
    except Exception as e:
        print("Something went wrong with the request,  the url probably changed.")
        print(e)
    '''

def parseRequest(response, num, state):

    try:
        #html = response.content()
        html = response
        filename = str(num) + state +"tf"

        #with open("#{filename}.txt", 'w') as file:
            #file.write(html)



        soup = BeautifulSoup(html, 'html.parser')
        trails = list()
        for link in soup.find_all('tr'):
            links = link.find_all('a')
            if (links != []):
                trail = links[0].get('href')
                region = links[1].get('href')
                print(trail)
                print(region)



            #print(trail)

            #print(link)

    except Exception as e:
        print(e)


# Function to try converting string to int because not all TF have number id's
def tryConvert(stringConv):
    def RepresentsInt(s):
        try:
            convert = int(s)
            return convert
        except ValueError:
            return None
