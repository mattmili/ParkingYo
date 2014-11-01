#!/usr/bin/env python
#Credits to https://github.com/parthanium/YoPy
import requests

class Yo:
	def __init__(self, token):
		self.token = token

	def number(self):
		"""
		Function to GET the the number of subscribers of the API user account.
		Returns number of subscribers as an integer.
		If request is unsuccessful, raises an error.
		"""
		number_url = "http://api.justyo.co/subscribers_count/?api_token=" + self.token
		number = requests.get(number_url)
		if number.status_code == requests.codes.ok:
		    return number.json()["result"]
		else:
			number.raise_for_status()

	def yoall(self, *link):
		"""
		Function to send a Yo to all subscribers of the API user account.
		If request is successful, returns true.
		If request is unsuccessful, raises an error.
		"""
		yoall_data = {"api_token": self.token, "link": link}
		yoall_url = "http://api.justyo.co/yoall/"
		yoall = requests.post(yoall_url, data=yoall_data)
		if yoall.status_code == requests.codes.created:
			return True
		else:
			yoall.raise_for_status()

	def youser(self, username, *link):
		"""
		Function to send a Yo to a specific username.
		If request is successful, returns true.
		If request is unsuccessful, raises an error.
		"""
		username = username.upper()
		youser_data = {"api_token": self.token, "username": username, "link": link}
		youser_url = "http://api.justyo.co/yo/"
		youser = requests.post(youser_url, data=youser_data)
		if youser.status_code == requests.codes.ok:
		    return True
		else:
			yoall.raise_for_status()