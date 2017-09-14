from geopy.geocoders import GoogleV3
import pandas as pd

geolocator = GoogleV3(api_key = 'PUT_KEY_HERE')


columns = ['id','username','type','statuses','friends','followers','listed','join_date','url','img','location']
df_dat = pd.read_csv('twitter/ncdaction.dat', names=columns)

df_dat = df_dat[df_dat.location.notnull()]

locations_raw = []
locations = []
locations_error = []

for ind, row in df_dat.iterrows():
    try:
        l = geolocator.geocode(row.location, timeout = 20)
        locations_raw.append(l.raw)
        locations.append((l.latitude,l.longitude))
        locations_error.append(False)
        print(str(row.username) + ' processed.')
    except:
        locations_raw.append(None)
        locations.append((None,None))
        locations_error.append(True)
        print(str(row.username) + ' error.')

df_dat['raw_geocoded'] = locations_raw
df_dat['lat_long_geocoded'] = locations
df_dat['geocode_error'] = locations_error


df_dat.to_csv('twitter_followers_geocoded_1.csv')
