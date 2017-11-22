from geopy.geocoders import Nominatim

geolocator = Nominatim()
location = geolocator.geocode("175 5th Avenue NYC")
print(location.address)


geolocator = Nominatim()
location = geolocator.reverse("25.12786, 121.7327")
print(location.address)
location = geolocator.reverse("25.12786, 121.7680")
print(location.address)

