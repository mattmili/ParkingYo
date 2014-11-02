from yofindparking import app
from flask import request, render_template
import requests

YO_API = "https://api.justyo.co/yo/"
api_token = "e6263ea5-e7ed-4142-bc9c-54c07b41ecfe"


# def get_parking_spot(lat, lon):
    

# def get_parking_price(ref):
    

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
    street_number = request.args.get('msg')
    cost = request.args.get('name')
    return render_template('response.html',address=street_number,price=cost)

@app.route('/yo')
def yo():
    """Handle callback request"""
    username = request.args.get('username')
    location = request.args.get('location')
    splitted = location.split(';')
    latitude = splitted[0]
    longitude = splitted[1]
    
    # address = get_parking_spot(latitude, longitude)
    # price = get_parking_price(ref)
    
    link = "https://aqueous-cove-8179.herokuapp.com/response?msg={0}&name={1}".format(
            '$3.50', '123 fake street')
    send_yo(username, link)
    return 'OK'
