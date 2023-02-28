import googlemaps



def get_long_lat(location):

    print(location)
    gmaps = googlemaps.Client(key='AIzaSyB7HuW7zVC8D4-mKp30OslFykDVI8LA7bA')

    # Geocoding an address
    geocode_result = gmaps.geocode(location)

    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']

    return lat , lng


if __name__ == "__main__":
    # location = "Lorenzo Pizza,Pasta" + "riyadh"
    location =  "مطعم" + "فريج بن عاقول" + "المحرق" + "البحرين"

    result = get_long_lat(location)