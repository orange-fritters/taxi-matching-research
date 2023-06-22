import pandas as pd

data = pd.read_csv("data/20230227.csv")

unique_pairs = data[['departure_id', 'arrival_id']].drop_duplicates()

len(data['endposid'].unique())
len(data['startposid'].unique())

