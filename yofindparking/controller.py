from yofindparking import app
from flask import request, render_template
import requests
import parking
import urllib2
import json
import pprint

YO_API = "https://api.justyo.co/yo/"
api_token = "e6263ea5-e7ed-4142-bc9c-54c07b41ecfe"

class parkingSpot:
    def __init__(self, lat, lng, cost, distance, lotName, spots):
        self.lat=lat
        self.lng=lng
        self.price=cost
        self.distance=distance
        self.lotName=lotName
        self.availableSpots=spots

def getJSONData(latitude, longitude):
    
    ParkWhizAPIKey='d9e934eabf61b48b4885179b1c37afd6'
    # Simulated location for new york
    lat=str(latitude)
    lng=str(longitude)
    url='http://api.parkwhiz.com/search/?lat='+lat+'&lng='+lng+'&key='+ParkWhizAPIKey
    data = json.load(urllib2.urlopen(url))   
    
    # Get the closest parking spot
    closestParkingLot = data.items()[6][1][0]

    spot = parkingSpot(
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
        data={'api_token': api_token, 'username': username, 'link': link})


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
    return render_template('response.html',lotName=name,lotDistance=distance,lotPrice=cost)

@app.route('/yo')
def yo():
    """Handle callback request"""
    username = request.args.get('username')
    location = request.args.get('location')
    splitted = location.split(';')
    latitude = splitted[0]
    longitude = splitted[1]
    
    #spot = getJSONData(latitude, longitude)
    spot = getJSONData(40.748183, -73.985064)

    parkingLotName=spot.lotName
    parkingLotDistance=spot.distance
    parkingLotPrice=spot.price
        
    link = "http://5e96697a.ngrok.com/response?name={0}&distance={1}&price={2}".format(
            parkingLotName, parkingLotDistance, parkingLotPrice)
    send_yo(username, link)
    return 'OK'
