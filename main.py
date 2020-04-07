import sys
from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image
from Complete_search.pos import object_pos

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass

# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
print(json_response["response"])
# Координаты центра топонима:

toponym_coodrinates_1 = toponym["boundedBy"]["Envelope"]["lowerCorner"]
toponym_coodrinates_2 = toponym["boundedBy"]["Envelope"]["upperCorner"]

toponym_longitude, toponym_lattitude, delta_x, delta_y = object_pos(toponym_coodrinates_1, toponym_coodrinates_2)
# Собираем параметры для запроса к StaticMapsAPI:

map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join([delta_x, delta_y]),
    "l": "map",
    "pt": ",".join([toponym_longitude, toponym_lattitude]) + ",pm2am"
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()
# Создадим картинку
# и тут же ее покажем встроенным просмотрщиком операционной системы
