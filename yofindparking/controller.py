from yofindparking import app
from flask import request, render_template
import requests, urllib2, json, pprint
import config

YO_API = "https://api.justyo.co/yo/"
callbackURL='https://yofindparking.herokuapp.com/'

class parkingSpot:
    def __init__(self, city, lat, lng, cost, distance, lotName, spots):
        self.city=city
        self.lat=lat
        self.lng=lng
        self.price=cost
        self.distance=distance
        self.lotName=lotName
        self.availableSpots=spots

def getJSONData(latitude, longitude, username):
    lat=str(latitude)
    lng=str(longitude)
    url='http://api.parkwhiz.com/search/?lat='+lat+'&lng='+lng+'&key='+config.ParkWhizAPIKey

    try:
        data = json.load(urllib2.urlopen(url))
        # Get the closest parking spot
        closestParkingLot = data.items()[6][1][0]   
    except Exception:
        send_yo(username, 'http://yofindparking.herokuapp.com/noresult')
    else:
        spot = parkingSpot(
            closestParkingLot['city'],
            closestParkingLot['lat'], 
            closestParkingLot['lng'],
            closestParkingLot['price_formatted'], 
            closestParkingLot['distance'],
            closestParkingLot['location_name'],
            closestParkingLot['available_spots'])
    
        return spot
    
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
    return render_template('response.html',lotName=name,lotDistance=distance,lotPrice=cost,city=city)

@app.route('/yo')
def yo():
    """Handle callback request"""
    username = request.args.get('username')
    location = request.args.get('location')
    splitted = location.split(';')
    latitude = splitted[0]
    longitude = splitted[1]
    
    spot = getJSONData(latitude, longitude, username)
    #spot = getJSONData(40.748183, -73.985064, 0) # for testing purposes

    parkingLotCity=spot.city
    parkingLotName=spot.lotName
    parkingLotDistance=spot.distance
    parkingLotPrice=spot.price

    link = callbackURL+"/response?name={0}&distance={1}&price={2}&city={3}".format(
        parkingLotName, parkingLotDistance, parkingLotPrice, parkingLotCity)
    send_yo(username, link)
    return 'OK'
