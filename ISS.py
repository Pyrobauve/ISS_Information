import json
import urllib.request
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="ISS_information")
url_people = "http://api.open-notify.org/astros.json"
url_pos = "http://api.open-notify.org/iss-now.json"
data_people = urllib.request.urlopen(url_people)
data_pos = urllib.request.urlopen(url_pos)
resultat_people = json.loads(data_people.read())
resultat_pos = json.loads(data_pos.read())

number_people = resultat_people['number']
people_in = resultat_people['people']

pos_ISS = resultat_pos['iss_position']
lat = str(pos_ISS['latitude'])
lon = str(pos_ISS['longitude'])
location = geolocator.reverse(lat+","+lon)
if location != None:
    address = location.raw['address']
    city = address.get('city', '')
    state = address.get('state', '')
    country = address.get('country', '')

print("------- In the ISS -------")
print("Number of people in the ISS:", number_people)
print("")
for p in people_in:
    print(p['name'])

print('')
print('------- Location -------')

if location != None:
    print("City: ", city)
    print("State: ", state)
    print("Country: ", country)

else:
    print("The ISS is above the ocean.")
