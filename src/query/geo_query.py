from geopy.geocoders import Nominatim

def get_location_by_coordinates(latitude, longitude):
    # geolocator = Nominatim(user_agent="geoapiExercises")
    geolocator = Nominatim(user_agent="geopy_devin_zhang(devin.zhang@shopee.com)")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    address = location.raw['address']
    city = "{}-{}-{}".format(address.get('country', ''), address.get('state', ''), address.get('city', ''))

    if city == '--':
        return "unknown-geopy"
    else:
        return city

# 'latitude': 34.7732, 'longitude': 113.722
if __name__ == "__main__":
    # 示例经纬度
    latitude = 34.7732
    longitude = 113.722

    location_info = get_location_by_coordinates(latitude, longitude)
    print(location_info)
