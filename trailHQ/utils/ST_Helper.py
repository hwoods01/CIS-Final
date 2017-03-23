# coding: interpy

import requests
from bs4 import BeautifulSoup
from trailHQ.models import SingletracksTrail




SingleTracksURL = 'https://trailapi-trailapi.p.mashape.com/'
radius = "radius=50"
activity_string = 'q[activities_activity_type_name_eq]=mountain+biking'
country_string = 'q[country_cont]=United States'
headers = {'X-Mashape-Key': 'Li4lO5svuRmshPnqogrJpkOC4KxAp1kej3ijsnXCRbpxawhJ5f', 'Accept': 'text/plain'}


#https://trailapi-trailapi.p.mashape.com/?lat=34.1&limit=25&lon=-105.2&q[activities_activity_type_name_eq]=mountain+biking&q[city_cont]=Wichita&q[country_cont]=United+States&q[state_cont]=Kansas&radius=50

'''
This method makes the response to the Singletracks API using the city and state variables passed in
right now that is the only way a request will be made
'''
def makeRequest(city, state):
    city_string = "q[city_cont]=#{city}"
    state_string = "q[state_cont]=#{state}"
    print(city_string)
    unformreq = SingleTracksURL + '?' + activity_string + '&' + city_string + '&'+ state_string + '&' + country_string +'&' + radius
    print(headers)
    print(unformreq)

    try:
        r=requests.get(unformreq, headers=headers)
        parseRequest(r)
        #print(r)

        #foreach[places]
            #[lat][lon]
            # foreach[activities]:
                # [name],[description], [length] [url], [rating]

            # TODO use url to get difficulty
    except Exception as e:
        print(e)


'''This takes the response from the api and parses it.
    Once done parsing it will read into the database
    In the future this will probably do some other work in the future'''
def parseRequest(response):


    try:
        #this is prime terrirtory for async for loop
        json_content = response.json()
        for i in json_content['places']:
            lat = i['lat']
            lon = i['lon']
            for j in i['activities']:
                name = j['name']
                desc = j['description']
                length = j['length']
                url = j['url']
                rating = j['rating']
                print(lat, lon, name, desc, length, url, rating)
                difficulty = getSingletrackRating(url)
                if(difficulty == None):
                    difficulty = "Unknown"

                trail = SingletracksTrail(city=i['city'], state=i['state'], name=j['name'], longitude=i['lon'],latitude=i['lat'], description=j['description'],url=j['url'],length=j['length'], rating=j['rating'], difficulty= difficulty)
                trail.save()

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



