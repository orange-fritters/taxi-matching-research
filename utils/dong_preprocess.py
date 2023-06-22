import json
import datetime
import pandas as pd
from workalendar.asia import SouthKorea

df = pd.read_csv("data/data.csv")

# Generate Dong id
departure_dongs = set(df['출발동'].unique())
arrival_dongs = set(df['목적동'].unique())

total_dongs = arrival_dongs | departure_dongs
total_dongs = sorted(list(total_dongs))

dong_id = {dong : i for i, dong in enumerate(total_dongs)}

with open('data/dong_id.json', 'w') as f:
    json.dump(dong_id, f)

# Label Encoding
df['departure_id'] = df['출발동'].map(dong_id)
df['arrival_id'] = df['목적동'].map(dong_id)

# Eliminate negative waiting time
df = df[df['대기시간'] > 0]

# Add weekend

columns_to_convert = ['접수일시', '희망일시', '배차시간', '탑승시간', '하차시간', '대기시간']
df[columns_to_convert] = df[columns_to_convert].apply(pd.to_datetime)

cal = SouthKorea()
df['weekend'] = df['탑승시간'].apply(lambda x: cal.is_holiday(x) or x.weekday() > 4)

df.to_csv("data/data.csv")
