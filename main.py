import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Read in the data
df = pd.read_excel('2023.xlsx')
df.head()

# From 2023-01-01 to 2023-01-02
data = df[0:6037]
data = data.dropna()

def getFrequency(data, colnames, interval):
    col_1, col_2 = colnames

    # Generate a time range covering the entire period
    time_range = pd.date_range(start=pd.Timestamp('2023-01-01 00:00:00'),
                                end=pd.Timestamp('2023-01-03 00:00:00'), freq=f'{interval}T')

    # Create a new Series to store the frequency count for each time interval
    freq = pd.Series(index=time_range, data=0)

    # Iterate through each row in the dataset
    for index, row in data.iterrows():
        # Create a time range between col_1 and col_2 for the current row
        row_time_range = pd.date_range(
            start=row[col_1].floor('T'), end=row[col_2].floor('T'), freq=f'{interval}T', inclusive='left')
        # Increment the freq count for each timestamp in the row_time_range
        for timestamp in row_time_range:
            if timestamp in freq.index:
                freq[timestamp] += 1
    return freq


# Plot the frequency data
plt.figure(figsize=(12, 6))
frequency = getFrequency(data[:], ['희망일시', '배차시간'], 1)
plt.plot(frequency.index, frequency.values)
plt.xlabel('Time')
plt.ylabel('Frequency')
plt.title('Frequency Plot between Desire and Dispatch Time')
plt.show()

frequency.index
frequency.values

plt.figure(figsize=(12, 6))
frequency2 = getFrequency(data[:], ['배차시간', '하차시간'], 1)
plt.plot(frequency2.index, frequency2.values)
plt.xlabel('Time')
plt.ylabel('Frequency')
plt.title('Frequency Plot between Desire and Dispatch Time')
plt.show()

ratio = frequency.divide(frequency2)
ratio = ratio.replace([np.inf, -np.inf], np.nan)
plt.figure(figsize=(12, 6))
plt.plot(ratio.index, ratio.values)
plt.xlabel('Time')
plt.ylabel('Ratio')
plt.title('Ratio of Frequency1 to Frequency2')
plt.show()
