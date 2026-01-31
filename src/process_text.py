# IMPORTS
import pandas as pd
import spacy

# FLAG PLACES
speeches = pd.read_csv('output/tables/speeches_ddbb.csv', index_col=0)
print('Looking for places in the speeches... This may take a while!')

places_speech = []
nlp = spacy.load("en_core_web_sm")

for speech in speeches.iterrows():
    places = []
    doc = nlp(speech[1].transcript)
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"]:
            places.append(ent.text)
    places_speech.append(places)

speeches = speeches.drop(['transcript'], axis=1)
speeches['places'] = places_speech

# COMPUTE PLACE METRICS
speeches['num_places'] = [len(row) for row in speeches['places']]
speeches['unique_places'] = [list(set(x)) for x in speeches['places']]
speeches['num_unique_places'] = [len(row) for row in speeches['unique_places']]

# SAVE FILE
speeches.to_csv('output/tables/speeches_processed.csv')