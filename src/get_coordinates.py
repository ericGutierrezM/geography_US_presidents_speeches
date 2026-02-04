# IMPORTS
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import pandas as pd
import ast

# PREPARE DATA
FILE_PATH = 'output/tables/speeches_processed.csv'

data = pd.read_csv(FILE_PATH, index_col=0)
data['unique_places'] = data['unique_places'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

unique_places = list(set(data['unique_places'].explode()))

df = pd.DataFrame({
    "place": unique_places,
})

# GET COORDINATES
geolocator = Nominatim(user_agent="music_and_place", timeout=10)
geocode_with_delay = RateLimiter(geolocator.geocode, min_delay_seconds=3)

print(f'Retrieving the coordinates for {len(df['place'])} places... This may take a while!')

def get_coords_no_error(place):
    try:
        return geocode_with_delay(place)
    except (GeocoderTimedOut, GeocoderUnavailable, Exception):
        return None

df['location_obj'] = df['place'].apply(get_coords_no_error)

df['lat'] = df['location_obj'].apply(lambda loc: loc.latitude if loc else None)
df['lon'] = df['location_obj'].apply(lambda loc: loc.longitude if loc else None)

final_df = df.drop(columns=['location_obj'])

# SAVE FILE
final_df.to_csv('output/tables/coordinates.csv')
print('Coordinates saved in file coordinates.csv.')