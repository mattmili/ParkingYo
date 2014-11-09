from yofindparking import app
from flask import request, render_template
import requests, urllib2, json, pprint
import config
import unicodedata

YO_API = "https://api.justyo.co/yo/"
callbackURL='http://6d2e2a50.ngrok.com'

class parkingSpot:
    def __init__(self, city, lat, lng, cost, distance, lotName, spots):
        self.city=normalizeUnicode(city)
        self.lat=str(lat)
        self.lng=str(lng)
        self.price=str(cost)
        self.distance=str(distance)
        self.lotName=normalizeUnicode(lotName)
        self.availableSpots=str(spots)

def getJSONData(latitude, longitude, username):

    lat=str(latitude)
    lng=str(longitude)
    url='http://api.parkwhiz.com/search/?lat='+lat+'&lng='+lng+'&key='+config.ParkWhizAPIKey

   
    data = json.load(urllib2.urlopen(url))
    # Get the closest parking spot
    send_yo(username, callbackURL+'/noresult')
    pSpot = parkingSpot(
        data.items()[6][1][0]['city'], 
        data.items()[6][1][0]['lat'], 
        data.items()[6][1][0]['lng'],
        data.items()[6][1][0]['price_formatted'], 
        data.items()[6][1][0]['distance'],
        data.items()[6][1][0]['location_name'],
        data.items()[6][1][0]['available_spots'])
    return pSpot

def normalizeUnicode(string):
    return unicodedata.normalize('NFKD', string).encode('ascii','ignore')
    
def send_yo(username, link):
    """Yo a username"""
    requests.post(
        YO_API,
        data={'api_token': config.api_token, 'username': username, 'link': link})

@app.route('/')
def main():
    """Index Controller"""
    return render_template('index.html')

@app.errorhandler(404)
def handle_error(e):
    return render_template('404.html')

@app.route('/noresult')
def noresult():
    return render_template('noresult.html')


@app.route('/response')
def response():
    name = request.args.get('name')
    distance = request.args.get('distance')
    cost = request.args.get('price')
    city = request.args.get('city')
    parkinglng = request.args.get('parkinglong')
    parkinglat = request.args.get('parkinglat')
    userlng = request.args.get('userlong')
    userlat = request.args.get('userlat')
    return render_template('response.html',
        lotName = name,
        lotDistance = distance,
        lotPrice = cost,
        city = city,
        pLat = parkinglat,
        pLong = parkinglng,
        uLat = userlat,
        uLong = userlng
        )

@app.route('/yo')
def yo():
    """Handle callback request"""
    username = request.args.get('username')
    location = request.args.get('location')
    splitted = location.split(';')
    latitude = splitted[0]
    longitude = splitted[1]
    
    #spot = getJSONData(latitude, longitude, username)
    spot = getJSONData(40.748183, -73.985064, 0) # for testing purposes

    if spot is None:
        send_yo(username, callbackURL+"/noresult")
    else:
        link = callbackURL+"/response?name={0}&distance={1}&price={2}&city={3}&parkinglong={4}&parkinglat={5}&userlong={6}&userlat={7}".format(
            spot.lotName,
            spot.distance, 
            spot.price, 
            spot.city,
            spot.lng,
            spot.lat,
            str(latitude),
            str(longitude)
            )
        send_yo(username, link)
    return 'OK'