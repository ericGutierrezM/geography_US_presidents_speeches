# IMPORTS
import pandas as pd
import ast

# PREPARE DATA
PLACES_PATH = 'output/tables/speeches_processed.csv'
COORDS_PATH = 'output/tables/coordinates.csv'

places = pd.read_csv(PLACES_PATH, index_col=0)
coords = pd.read_csv(COORDS_PATH, index_col=0)

# JOIN
def parse_list_string(x):
    if isinstance(x, str) and x.startswith('['):
        try:
            return ast.literal_eval(x)
        except (ValueError, SyntaxError):
            return []
    return x if isinstance(x, list) else []

places['places'] = places['places'].apply(parse_list_string)

places_exploded = places.explode('places')

df_final = places_exploded.merge(
    coords, 
    left_on='places',   
    right_on='place',
    how='left'
)

df_final.to_csv('output/tables/speeches_with_coordinates.csv')
print('Coordinates joined to speech data in file speeches_with_coordinates.csv.')