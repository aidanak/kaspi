# -*- coding: utf-8 -*-
import requests
import json
import traceback
import time
import sys
import psycopg2
import threading
from urlparse import urlparse
from multiprocessing import Pool
import urllib

client_id = 'IFIEMHXZIDQTEVDSEJMWP5IOZBGILU4PSJCFQQ0BO522BDZL' # Insert your own client_id
client_secret = 'AISNJLVGHXAXJEBA5LHHZO40SASLW02A2NQ0EJVRBYWW2ZYH' # Insert your own client_secret

def getVenues():
	global client_id, client_secret
	venues = []
	url = 'https://api.foursquare.com/v2/venues/explore'
	params = urllib.urlencode({'client_id': client_id,
							  'client_secret': client_secret,
							  'v': '20160901',
							  'near': 'Алматы, Казахстан',
							  'query': 'restaurant',
							  'limit': 100})

	r = requests.get(url + '?' + params)
	if r:
		data = json.loads(r.text)
		if 'response' in data:
			if 'groups' in data['response']:
				groups = data['response']['groups']
				for group in groups:
					if 'items' in group:
						items = group['items']
						for item in items:
							if 'venue' in item:
								itemID = item['venue']['id']
								name = item['venue']['name']
								lon = item['venue']['location']['lng']
								lat = item['venue']['location']['lat']
								venues.append({'id': itemID,
											   'name': name,
											   'lon': lon,
											   'lat': lat})
					break
			else:
				print(r.text)
				sys.exit()
		else:
			print(r.text)
			sys.exit()
	else:
		print(r)
		sys.exit()
	return venues

def getReviews(venue):
	global client_id, client_secret
	reviews = []
	url = 'https://api.foursquare.com/v2/venues/%s/tips' % venue['id']
	params = {'client_id': client_id,
			  'client_secret': client_secret,
			  'v': '20160901',
			  'limit': 500}
	r = requests.get(url, params = params)
	if r:
		data = r.json()
		if 'response' in data:
			if 'tips' in data['response']:
				if 'items' in data['response']['tips']:
					tips = data['response']['tips']['items']
					for tip in tips:
						text = tip['text']
						reviews.append(text)
	venue['reviews'] = reviews
	writeToDB(venue)

def writeToDB(venue):
	con = psycopg2.connect(host = 'localhost', database = 'restaurant', user = 'user1', password = 'user1', port = '5432')
	try:
		cur1 = con.cursor()
		cur1.execute('INSERT INTO myapp_venues (name,longitude, latitude) ' + \
					 'VALUES (%s, %s, %s) RETURNING rec_id',
					 (venue['name'], venue['lon'], venue['lat']))
		rec_id = cur1.fetchone()[0]
		con.commit()
		if len(venue['reviews']) > 0:
			cur2 = con.cursor()
			for review in venue['reviews']:
				cur2.execute('INSERT INTO myapp_venue_tips (venue_id, text_of_review) ' + \
							 'VALUES (%s, %s)',
							 (rec_id, review))
				con.commit()
	except:
		print(traceback.format_exc())
		con.rollback()
	finally:
		con.close()

def main():
	venues = getVenues()
	if len(venues) > 0:
		processCount = 100
		pool = Pool(processes = processCount)
		venues = pool.map(getReviews, venues)
		pool.close()
		pool.join()

if __name__ == '__main__':
	main()
