import requests as r 
import json

class Geopy():
    def __init__(self):
        self.url = 'https://nominatim.openstreetmap.org/search'

    def request(self, street, city, country):
        try:
            req = json.loads(r.get(self.url, params={
                'street': street,
                'city': city,
                'country': country,
                'format': 'json'
            }).text)[0]
        except:
            req = {'lat': '', 'lon': ''}
        if len(req) != 0:
            return {'lat': req['lat'], 'lon': req['lon']}
        else:
            return {'lat': '', 'lon': ''}

# (Geopy().request('weimarrrr', 'dourados', 'brasil'))
