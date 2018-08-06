import httplib2
import json
import requests

def findARestaurant(searchType, location):
	google_api_key = 'AIzaSyBiPluvaU2U4PmvDLoEhjaese9QqpdOV_M'
	location_string = location.replace(" ", "+")
	
	google_url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + location_string + '&key=' + google_api_key
	request_obj = httplib2.Http()
	response, content = request_obj.request(google_url, 'GET')
	result = json.loads(content)
	
	latitude, longitude = result['results'][0]['geometry']['location']['lat'], result['results'][0]['geometry']['location']['lng']
	
	foursquare_url = 'https://api.foursquare.com/v2/venues/explore'
	params = dict(
		client_id='ZIPKMP2RHJOBJUNS53TCDNJJ4JRQ2RWTUZGUKMEUZXRFXCGB',
		client_secret='KBOEMJ3RUXEP1Q3FPLSJYCB5BTSTXMWA1YTEGA4SRX3RQBPY',
		v='20180323',
		ll=str(latitude) + ',' + str(longitude),
		query=searchType,
		limit=1)

	response = requests.get(url=foursquare_url, params=params)
	result = json.loads(response.text)
	
	print('The top suggested place is: ', result['response']['groups'][0]['items'][0]['venue']['name'])

searchType = input('Enter the type of search: ')
location = input('Enter the location: ')

findARestaurant(searchType, location)
