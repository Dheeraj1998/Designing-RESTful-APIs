import httplib2
import json

def getGeoCodeLocation(input_string):
	api_key = 'AIzaSyBiPluvaU2U4PmvDLoEhjaese9QqpdOV_M'
	location_string = input_string.replace(" ", "+")
	
	api_url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + location_string + '&key=' + api_key
	request_obj = httplib2.Http()
	
	response, content = request_obj.request(api_url, 'GET')
	result = json.loads(content)
	
	print("\nResponse code: ", response)
	print("\n\nResultant content: ", result)	

input_string = input('Enter a location: ')
getGeoCodeLocation(input_string)
