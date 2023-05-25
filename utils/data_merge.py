import pandas as pd

# Read the Excel files into separate DataFrames
df1 = pd.read_excel('data/data1.xlsx')
df2 = pd.read_excel('data/data2.xlsx')
df3 = pd.read_excel('data/data3.xlsx')
df4 = pd.read_excel('data/data4.xlsx')
df5 = pd.read_excel('data/data5.xlsx')

# Merge the DataFrames into a single DataFrame
df = pd.concat([df1, df2, df3, df4, df5], ignore_index=True)

# Drop na, Only Seoul
df = df.dropna()
df = df[df['출발시'] == '서울특별시']
df = df[df['목적시'] == '서울특별시']

# Save the merged DataFrame to name data
df.to_csv("data/data.csv")
