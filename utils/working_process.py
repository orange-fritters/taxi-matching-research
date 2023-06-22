import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats    

#%%
df = pd.read_csv("results/visual/result.csv")
times = df["total_time"].tolist()
data = np.array(times)
params = stats.lognorm.fit(times, floc=0)
x = np.linspace(min(data), max(data), 100)
pdf_lognorm = stats.lognorm.pdf(x, *params)


df2 = pd.read_csv("results/visual/current.csv")
times2 = df2["total_time"].tolist()
data2 = np.array(times2)
params2 = stats.lognorm.fit(times2, floc=0)
x2 = np.linspace(min(data2), max(data2), 100)
pdf_lognorm2 = stats.lognorm.pdf(x2, *params2)

# Plot the histogram and the fitted lognorm distribution
# plt.hist(data, bins=100, density=True, alpha=0.6, color='g')
plt.figure(figsize=(10, 5))
plt.plot(x, pdf_lognorm, 'r-', lw=2)
plt.plot(x, pdf_lognorm2, 'b-', lw=2)
plt.title('Lognormal Distribution Fit')
plt.xlabel('Data')
plt.ylabel('Frequency')
plt.show()

# print and params of fitted distribution and compare
print("shape ", params[0], params2[0])
print("scale ", params[2], params2[2])
print("loc ", params[1], params2[1])

#%%
original = pd.read_csv("data/output.csv")
original = original.iloc[:1122, :]
print((original['ridetime'] - original['desiredtime']).mean())

df = pd.read_csv("results/bugfix/_results.csv")

df['mean_time'].min()


df = pd.read_excel("data/2022년도 로우데이터.xlsx")
dong_id = pd.read_csv("data/dong_id.csv")
freq = np.zeros(len(dong_id))
for i, row in df.iterrows():
    # if row['출발동'] is in the dong_id['dong'], then add 1 to the corresponding index.
    if row['출발동'] in dong_id['dong'].tolist():
        freq[dong_id.index[dong_id['dong'] == row['출발동']][0]] += 1

print(freq)
# somehow normalize the freq maintaining 0 to 1
freq_norm = freq / freq.max()
print(freq_norm)

# convert freq_norm to dataframe
df_freq = pd.DataFrame(freq_norm, columns=['freq'])
df_freq.to_csv("data/freq.csv", index=False)



df = pd.read_csv("results/visual/a_0.9_b_0.1_tw_1_tol_0.csv")
df2 = pd.read_csv("results/visual/greedy.csv")

# compare df and df2
df['total_time'].mean()
df2['total_time'].mean()

#%%
import pandas as pd

df = pd.read_csv("data/output.csv")
for i in range(5, 101, 5):
    df_ = df.deepcopy()



# %%
dong_id = pd.read_csv("data/dong_id.csv")
dong_equity = pd.read_csv("data/dong_equity.csv")
dong_coord = pd.read_csv("data/dong_coord.csv")

lats = []
lngs = []
for i, row in dong_equity.iterrows():
    id = row['Group']
    dong = dong_id['dong'][dong_id['id'] == id].tolist()[0]
    lat = dong_coord[dong_coord['주소'] == dong]['Latitude'].tolist()[0]
    lng = dong_coord[dong_coord['주소'] == dong]['Longitude'].tolist()[0]
    lats.append(lat)
    lngs.append(lng)
dong_equity['Latitude'] = lats
dong_equity['Longitude'] = lngs

dong_equity.to_csv("data/dong_equity.csv", index=False)
# %%


df = pd.read_csv("data/output.csv")

for i in range(5, 101, 5):
    tmp = df.copy()
    start_id = 10000
    for j, row in tmp.iterrows():
        if start_id == 10000+i:
            break
        if row['car_marker'] == 'none':
            tmp.loc[j, 'no'] = start_id
            start_id += 1
            tmp.loc[j, 'car_marker'] = 'start'
    tmp.to_csv("data/supply/plus_{}.csv".format(i), index=False)


#%%
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist

# Load the data
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
data = {
    'additional_supply': [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100],
    'total_time': [35.09634888438134, 34.122718052738335, 33.20993914807302, 32.294117647058826, 31.4158215010142, 31.176470588235293, 30.907707910750506, 30.440162271805274, 29.851926977687626, 30.080121703853955, 30.05476673427992, 29.253549695740364, 29.129817444219068, 29.23732251521298, 28.815415821501013, 28.67342799188641, 28.275862068965516, 28.02028397565923, 27.78397565922921, 27.691683569979716],
    'equity_measure': [71.49491525423728, 69.06440677966101, 68.63728813559322, 66.11864406779661, 64.58983050847458, 64.65084745762712, 63.75593220338983, 62.90169491525424, 61.9728813559322, 61.97627118644068, 62.349152542372885, 60.45084745762712, 60.23050847457627, 60.355932203389834, 59.355932203389834, 58.92203389830509, 58.03728813559322, 57.76949152542373, 57.06440677966102, 57.271186440677965]
}

df = pd.DataFrame(data)

# Calculate the curvature based on total_time
x = df['additional_supply']
y = df['total_time']

curvature = np.gradient(np.gradient(y, x), x)

# Plot the curvature
plt.plot(x, curvature)
plt.xlabel('Additional Supply')
plt.ylabel('Curvature')
plt.title('Curvature Plot')
plt.show()
# %%
