import pandas as pd
import json

df = pd.read_csv("data/data.csv")

departure_dongs = set(df['출발동'].unique())
arrival_dongs = set(df['목적동'].unique())

total_dongs = arrival_dongs | departure_dongs
total_dongs = sorted(list(total_dongs))

dong_id = {dong : i for i, dong in enumerate(total_dongs)}

with open('data/dong_id.json', 'w') as f:
    json.dump(dong_id, f)