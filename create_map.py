import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl
import folium
import os.path


from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="specify_your_app_name_here", timeout=100)
from geopy.extra.rate_limiter import RateLimiter
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)


# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py
# Ignore SSL certificate errors


def inform_friends(acct):
    """
    Return a information about the account followers in json format.
    """
    while True:
        # acct = input('Enter Twitter Account:')
        # acct = str(acct)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

        if (len(acct) < 1): break
        url = twurl.augment(TWITTER_URL,
                            {'screen_name': acct, 'count': '25'})
        
        connection = urllib.request.urlopen(url, context=ctx)
        data = connection.read().decode()

        js = json.loads(data)

        headers = dict(connection.getheaders())
        print('Remaining', headers['x-rate-limit-remaining'])

        # print(js)
        return js



def get_data_map(acct):
    """
    Return a list of tuples(screen name, location) of account's friends.
    """
    # main_dict = inform_friends('Khrysty35589984')
    main_dict = inform_friends(acct)
    return list((key['screen_name'], key['location']) for key in main_dict['users'])



def geodata(acct):
    '''
    Return a list of lists(name, location, (geodata)).
    '''
    data_lst = get_data_map(acct)
    geo_list = []
    for friend in data_lst:
        try:
            location = geolocator.geocode(friend[1])
            loc = (location.latitude, location.longitude)
            lst = [friend[0], friend[1], loc]
            geo_list.append(lst)
        except TypeError:
            continue
        except AttributeError:
            continue
    # print(geo_list)
    return geo_list

# print(geodata())




def layer_loc_friends(acct):
    
    '''
    '''
    map = folium.Map()
    points = folium.FeatureGroup(name="Points")

    geodata_lst = geodata(acct)
    for ls in geodata_lst:
        points.add_child(folium.Marker(location=[ls[2][0], ls[2][1]], popup=ls[0], icon=folium.Icon(color='green')))
    map.add_child(points)
    # map.save('templates/Main_map.html')
    return map.get_root().render()



# layer_loc_friends()


