from io import BytesIO
import sys
import requests
from PIL import Image
from pos import object_pos

search_api_server = "https://search-maps.yandex.ru/v1/"
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"


toponym_to_find = " ".join(sys.argv[1:])

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"
}


response_geocoder = requests.get(geocoder_api_server, params=geocoder_params)

if not response_geocoder:
    pass

json_response_geocoder = response_geocoder.json()

toponym = json_response_geocoder["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
toponym_coodrinates_pos = toponym["Point"]["pos"]


search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": ",".join(toponym_coodrinates_pos.split()),
    "type": "biz"
}

response_search = requests.get(search_api_server, params=search_params)

if not response_search:
    pass

json_response_search = response_search.json()
x_min, x_max, y_min, y_max = 0, 999, 0, 999
org_point = ""
for i in range(10):
    organization = json_response_search["features"][i]
    org_name = organization["properties"]["CompanyMetaData"]["name"]
    org_address = organization["properties"]["CompanyMetaData"]["address"]
    point = organization["geometry"]["coordinates"]
    if point[0] > x_min:
        x_min = point[0]
    if point[0] < x_max:
        x_max = point[0]
    if point[1] > y_min:
        y_min = point[1]
    if point[1] < y_max:
        y_max = point[1]
    list_keys_dict = organization["properties"]["CompanyMetaData"]["Hours"]["Availabilities"][0].keys()
    if "TwentyFourHours" in list_keys_dict:
        org_point += "{0},{1},pm2dgl~".format(str(point[0]), str(point[1]))
    elif "Intervals" in list_keys_dict:
        org_point += "{0},{1},pm2dbl~".format(str(point[0]), str(point[1]))
    else:
        org_point += "{0},{1},pm2grl~".format(str(point[0]), str(point[1]))
point_1 = "{0} {1}".format(str(x_min), str(y_min))
point_2 = "{0} {1}".format(str(x_max), str(y_max))

toponym_longitude, toponym_lattitude, delta_x, delta_y = object_pos(point_1, point_2)

map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join([delta_x, delta_y]),
    "l": "map",
    "pt": "{0}".format(org_point) + ",".join(toponym_coodrinates_pos.split()) + ",pm2al",
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(response.content)).show()
