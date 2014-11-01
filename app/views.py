from flask import render_template
from flask import request
from app import app
import yopy, config
import requests, json, urllib2

# Set the YO API token
yo = yopy.Yo(config.YO_API_TOKEN)

@app.route('/')
@app.route('/index')
def index():
	
	user = {'nickname': 'YOFINDPARKING'}  # fake user
	subscriber = {'number': yo.number()}
	return render_template('index.html',title='I NEED PARKING!',user=user,subscriber=subscriber)

