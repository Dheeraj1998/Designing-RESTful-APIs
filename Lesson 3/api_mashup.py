import json
import requests

from database_file import Base, RestaurantInfo
from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask('__name__')

table_engine = create_engine('sqlite:///restaurants.db')
Base.metadata.engine = table_engine
DBSession = sessionmaker(table_engine)
db_session = DBSession()


def geocode_lookup(location_string):
    google_api_key = 'AIzaSyBiPluvaU2U4PmvDLoEhjaese9QqpdOV_M'
    google_api_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = dict(
        address=location_string,
        key=google_api_key
    )

    response = requests.get(url=google_api_url, params=params)
    result = json.loads(response.text)
    latitude, longitude = result['results'][0]['geometry']['location']['lat'], \
        result['results'][0]['geometry']['location']['lng']

    return latitude, longitude


def foodsquare_lookup(latitude, longitude, mealtype_string):
    fs_client_id = 'ZIPKMP2RHJOBJUNS53TCDNJJ4JRQ2RWTUZGUKMEUZXRFXCGB'
    fs_client_secret = 'KBOEMJ3RUXEP1Q3FPLSJYCB5BTSTXMWA1YTEGA4SRX3RQBPY'
    foursquare_api_url = 'https://api.foursquare.com/v2/venues/explore'
    params = dict(
        client_id=fs_client_id,
        client_secret=fs_client_secret,
        v='20180323',
        llAcc='10000.0',
        limit=1,
        ll=str(latitude) + ',' + str(longitude),
        query=mealtype_string
    )

    response = requests.get(url=foursquare_api_url, params=params)
    result = json.loads(response.text)

    restaurant_name = result['response']['groups'][0]['items'][0]['venue']['name']
    restaurant_address = result['response']['groups'][0]['items'][0]['venue']['location']['address']

    return restaurant_name, restaurant_address


def db_store(restaurant_name, restaurant_address):
    new_restaurant = RestaurantInfo(name=restaurant_name, address=restaurant_address)
    db_session.add(new_restaurant)
    db_session.commit()


@app.route('/restaurants', methods=['GET', 'POST'])
def restaurant_lookup():
    if request.method == 'GET':
        all_data = db_session.query(RestaurantInfo).all()
        final_result = {}
        for value in all_data:
            final_result[value.name] = value.address

        final_result = json.dumps(final_result)

        return final_result

    else:
        location_string = request.args.get('location')
        mealtype_string = request.args.get('mealType')

        if location_string == '' or mealtype_string == '':
            return 'Valid parameters not passed.'

        else:
            location_string = location_string.replace(' ', '+')

            latitude, longitude = geocode_lookup(location_string)
            restaurant_name, restaurant_address = foodsquare_lookup(latitude, longitude, mealtype_string)
            db_store(restaurant_name, restaurant_address)

            return 'The following result has been stored in the database: [' + restaurant_name \
                + ', ' + restaurant_address + ']'


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
