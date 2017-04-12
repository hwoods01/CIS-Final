# coding: interpy

import requests
from bs4 import BeautifulSoup
from trailHQ.models import SingletracksTrail
import re



SingleTracksURL = 'https://trailapi-trailapi.p.mashape.com/'
radius = "radius=50"
activity_string = 'q[activities_activity_type_name_eq]=mountain+biking'
country_string = 'q[country_cont]=United States'
headers = {'X-Mashape-Key': 'Li4lO5svuRmshPnqogrJpkOC4KxAp1kej3ijsnXCRbpxawhJ5f', 'Accept': 'text/plain'}

def tryFilter(city, state):
    return SingletracksTrail.objects.filter(city = city, state = state)

#https://trailapi-trailapi.p.mashape.com/?lat=34.1&limit=25&lon=-105.2&q[activities_activity_type_name_eq]=mountain+biking&q[city_cont]=Wichita&q[country_cont]=United+States&q[state_cont]=Kansas&radius=50

def STController(city, state):
    r =makeRequest(city, state)
    response = parseRequest(r)
    return response

'''
This method makes the response to the Singletracks API using the city and state variables passed in
right now that is the only way a request will be made
'''
def makeRequest(city, state):
    city_string = "q[city_cont]=#{city}"
    state_string = "q[state_cont]=#{state}"
    unformreq = SingleTracksURL + '?' + activity_string + '&' + city_string + '&'+ state_string + '&' + country_string +'&' + radius

    try:
        r=requests.get(unformreq, headers=headers)
        return r

    except Exception as e:
        print(e)


'''This takes the response from the api and parses it.sanatized_trail =
    Once done parsing it will read into the database
    In the future this will probably do some other work in the future'''
def parseRequest(response):


    try:
        #this is prime terrirtory for async for loop
        json_content = response.json()
        if json_content['places'] == []:
            return False
        for i in json_content['places']:

            lat = i['lat']
            lon = i['lon']
            for j in i['activities']:
                name = j['name']
                sanatized_name = re.sub(r'([^\s\w]|_)+', '', name)
                desc = j['description']
                length = j['length']
                url = j['url']
                rating = j['rating']
                print(lat, lon, sanatized_name, desc, length, url, rating)
                difficulty = getSingletrackRating(url)
                if(difficulty == None):
                    difficulty = "Unknown"

                SingletracksTrail.objects.update_or_create(city=i['city'], state=i['state'], name=sanatized_name, longitude=lon,latitude=lat, description=desc,url=url,length=length, rating=rating, difficulty= difficulty)
        return True

    except Exception as e:

        print(e)


'''This method will go and grab the difficulty rating off the trail from the url, why this wasn't included in the API we will never know'''
def getSingletrackRating(url):
    try:
        r=requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')

        difficulty = soup.find(id='st_difficulty')
        return difficulty.text
    except Exception as e:
        return None



