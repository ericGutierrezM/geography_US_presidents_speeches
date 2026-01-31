# IMPORTS
import pandas as pd
import os
import json


# COMBINE ALL SPEECHES IN A SINGLE FILE
SPEECHES_DIR = 'data/miller_center_speeches/speeches'
OUTPUT_DIR = 'output/tables/speeches_ddbb.csv'

speech_list = []

with os.scandir(SPEECHES_DIR) as entries:
    for entry in entries:
        full_path = "\\\\?\\" + os.path.abspath(entry.path)
        with open(full_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                speech_list.append(data)                    

            except json.JSONDecodeError:
                print(f"Error parsing file: {entry.name}")

speeches = pd.DataFrame(speech_list)
speeches.to_csv(OUTPUT_DIR)
print('Speeches combined satisfactorily!')