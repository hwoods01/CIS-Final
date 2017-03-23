# coding: interpy

import requests




SingleTracksURL = 'https://trailapi-trailapi.p.mashape.com/'
key = '"X-Mashape-Key": "Li4lO5svuRmshPnqogrJpkOC4KxAp1kej3ijsnXCRbpxawhJ5f"'

radius = "radius=50"
activity_string = 'q[activities_activity_type_name_eq]=mountain+biking'


country_string = 'q[country_cont]=United States'
headers = {key, 'Accept": "text/plain'}


#https://trailapi-trailapi.p.mashape.com/?lat=34.1&limit=25&lon=-105.2&q[activities_activity_type_name_eq]=mountain+biking&q[city_cont]=Wichita&q[country_cont]=United+States&q[state_cont]=Kansas&radius=50

def makeRequest(city, state):
    city_string = "q[city_cont]=#{city}"
    state_string = "q[state_cont]=#{state}"
    print(city_string)
    unformreq = SingleTracksURL + '?' + activity_string + '&' + city_string + '&'+ state_string + '&' + country_string +'&' + radius

    print(unformreq)

    r=requests.get(unformreq, headers=headers)
    print(r)


