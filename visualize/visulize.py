#%%
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np


original = pd.read_csv("data/output.csv")
result = pd.read_csv("results/visual/result.csv")

#%% Visualiztion of Fig 1. 
org_time = original.iloc[:len(result), :]['ridetime'] - original.iloc[:len(result), :]['desiredtime']
res_time = result["total_time"]

assert len(org_time) == len(res_time)


# plt hist stacked
# BF2323
# 6D6D6D

plt.figure(figsize=(7, 5))
plt.hist([res_time, org_time], 
         bins=15, 
         stacked=False, 
         color=[ '#BF2323', '#6D6D6DE3'], 
         label=['result', 'original'])
plt.legend(loc='upper right')
plt.xlabel('Waiting time (min)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()
#%% Stats

org_time.mean()
res_time.mean()

#%% Comparison among methods of Fig 2.
result = pd.read_csv("results/visual/result.csv")
current = pd.read_csv("results/visual/current.csv")
greedy = pd.read_csv("results/visual/greedy.csv")
random = pd.read_csv("results/visual/random.csv")

current_time = current["total_time"]
greedy_time = greedy["total_time"]
random_time = random["total_time"]
result_time = result["total_time"]

plt.subplot(3, 1, 1)
plt.xlim(0, 180)
plt.hist([result_time, current_time ],
            bins=15,
            stacked=False,
            color=['#BF2323', '#6D6D6DE3'],
            label=['result', 'current'])
plt.legend(loc='upper right')
plt.title('Current method')
plt.xlabel('Waiting time (min)')

plt.subplot(3, 1, 2)
plt.xlim(0, 180)
plt.hist([result_time, greedy_time ],
            bins=20,
            stacked=False,
            color=['#BF2323', '#6D6D6DE3'],
            label=['result', 'greedy', ])
plt.legend(loc='upper right')
plt.title('Greedy method')
plt.xlabel('Waiting time (min)')

plt.subplot(3, 1, 3)
plt.xlim(0, 180)
plt.hist([result_time, random_time ],
            bins=15,
            stacked=False,
            color=['#BF2323', '#6D6D6DE3'],
            label=['result', 'random', ])
plt.legend(loc='upper right')
plt.title('Random method')
plt.xlabel('Waiting time (min)')

plt.tight_layout()
plt.show()

#%% Stats

result_time.mean()
greedy_time.mean()
current_time.mean()
random_time.mean()

# calculate top 20% waiting time average of each method
result_time.sort_values(ascending=False).head(int(len(result_time)*0.5)).mean()
greedy_time.sort_values(ascending=False).head(int(len(greedy_time)*0.5)).mean()
current_time.sort_values(ascending=False).head(int(len(current_time)*0.5)).mean()
random_time.sort_values(ascending=False).head(int(len(random_time)*0.5)).mean()


# calculate waiting time above 1.5 IQR and count numbers above 1.5 IQR.

result_time[result_time > 1.5*(result_time.quantile(0.75) - result_time.quantile(0.25))].count()
greedy_time[greedy_time > 1.5*(greedy_time.quantile(0.75) - greedy_time.quantile(0.25))].count()
current_time[current_time > 1.5*(current_time.quantile(0.75) - current_time.quantile(0.25))].count()
random_time[random_time > 1.5*(random_time.quantile(0.75) - random_time.quantile(0.25))].count()


# calculate waiting time above 60 minutes and count numbers above 60 minutes.

result_time[result_time > 60].count()
greedy_time[greedy_time > 60].count()
current_time[current_time > 60].count()
random_time[random_time > 60].count()

#%% Arrival time match time before and after optimization

# curr_time,request_id,waiting_time,arrival_time,total_time,req_loc
result = pd.read_csv("results/visual/result.csv")
result = result.iloc[:len(result), :]
result_arr = result['arrival_time']
result_wt = result['waiting_time']

original = pd.read_csv("data/output.csv")
original = original.iloc[:len(result), :]
original_arr = original['ridetime'] - original['settime']
original_wt = original['settime'] - original['desiredtime']

plt.subplot(1, 2, 1)
plt.hist([result_arr, original_arr ],
            bins=15,
            stacked=False,
            color=['#BF2323', '#6D6D6DE3'],
            label=['result', 'original'])
plt.legend(loc='upper right')
plt.xlabel('Arrival time (min)')
plt.ylabel("Frequency")
plt.title('Arrival time')

plt.subplot(1, 2, 2)
plt.hist([result_wt, original_wt],
            bins=15,
            stacked=False,
            color=['#BF2323', '#6D6D6DE3'],
            label=['result', 'original'])
plt.legend(loc='upper right')
plt.xlabel('Waiting time (min)')
plt.title('Waiting time')

plt.tight_layout()
plt.show()

#%% a b ratio - c --> color of total time mean figure
from matplotlib import cm, colors
data = pd.read_csv("results/effect_c/_results.csv")
data_c = pd.read_csv("results/effect_c/_results_c.csv")

# Show the plot
plt.show()



# %% Lognormal fitting of Fig 3.
import scipy.stats as stats    


result = pd.read_csv("results/visual/result.csv")
result_times = np.array(result["total_time"].tolist())
params_res = stats.lognorm.fit(result_times, floc=0)

current = pd.read_csv("results/visual/current.csv")
current_times = np.array(current["total_time"].tolist())
params_curr = stats.lognorm.fit(current_times, floc=0)

original = pd.read_csv("data/output.csv")
original_time = original.iloc[:len(result), :]['ridetime'] - original.iloc[:len(result), :]['desiredtime']
org_times = np.array(original_time.tolist())
params_org = stats.lognorm.fit(org_times, floc=0)

cat_times = np.concatenate((result_times, current_times, org_times), axis=0)
x = np.linspace(min(cat_times), max(cat_times), 100)

param_res = stats.lognorm.fit(result_times, floc=0)
param_curr = stats.lognorm.fit(current_times, floc=0)
param_org = stats.lognorm.fit(org_times, floc=0)

pdf_lognorm_res = stats.lognorm.pdf(x, *param_res)
pdf_lognorm_curr = stats.lognorm.pdf(x, *param_curr)
pdf_lognorm_org = stats.lognorm.pdf(x, *param_org)

# Plot the histogram and the fitted lognorm distribution
# plt.hist(data, bins=100, density=True, alpha=0.6, color='g')
plt.figure(figsize=(10, 5))
plt.plot(x, pdf_lognorm_res, '#e70a02', lw=2, label='result')
plt.plot(x, pdf_lognorm_curr, '#f16d74', lw=2, label='current')
plt.plot(x, pdf_lognorm_org, '#6d6d6de3', lw=2, label='original')
plt.hist(result_times, bins=100, density=True, alpha=0.4, color='#e70a02')
plt.hist(current_times, bins=100, density=True, alpha=0.3, color='#f16d74')
plt.hist(org_times, bins=100, density=True, alpha=0.3, color='#6d6d6de3')
plt.legend()
plt.xlabel('Waiting time (min)')
plt.ylabel('Probability density')
plt.show()

# print lognormal distance
print("result: ", stats.kstest(result_times, 'lognorm', args=param_res))
print("current: ", stats.kstest(current_times, 'lognorm', args=param_curr))
print("original: ", stats.kstest(org_times, 'lognorm', args=param_org))

# print lognormal stadard deviation obtained from fitting
print("result: ", param_res[2])
print("current: ", param_curr[2])
print("original: ", param_org[2])

#%% repeat assuming gamma distribution

result = pd.read_csv("results/visual/result.csv")
result_times = np.array(result["total_time"].tolist())
params_res = stats.gamma.fit(result_times)

current = pd.read_csv("results/visual/current.csv")
current_times = np.array(current["total_time"].tolist())
params_curr = stats.gamma.fit(current_times)

original = pd.read_csv("data/output.csv")
original_time = original.iloc[:len(result), :]['ridetime'] - original.iloc[:len(result), :]['desiredtime']
org_times = np.array(original_time.tolist())
params_org = stats.gamma.fit(org_times)

cat_times = np.concatenate((result_times, current_times, org_times), axis=0)
x = np.linspace(min(cat_times), max(cat_times), 100)

pdf_gamma_res = stats.gamma.pdf(x, *param_res)
pdf_gamma_curr = stats.gamma.pdf(x, *param_curr)
pdf_gamma_org = stats.gamma.pdf(x, *param_org)

# Plot the histogram and the fitted lognorm distribution
# plt.hist(data, bins=100, density=True, alpha=0.6, color='g')
plt.figure(figsize=(10, 5))
plt.plot(x, pdf_gamma_res, '#e70a02', lw=2, label='result')
plt.plot(x, pdf_gamma_curr, '#f16d74', lw=2, label='current')
plt.plot(x, pdf_gamma_org, '#6d6d6de3', lw=2, label='original')
plt.hist(result_times, bins=100, density=True, alpha=0.4, color='#e70a02')
plt.hist(current_times, bins=100, density=True, alpha=0.3, color='#f16d74')
plt.hist(org_times, bins=100, density=True, alpha=0.3, color='#6d6d6de3')
plt.legend()
plt.xlabel('Waiting time (min)')
plt.ylabel('Probability density')
plt.show()

# print gamma shape and scale obtained from fitting
print("result: ", params_res)
print("current: ", params_curr)
print("original: ", params_org)

#%% calculate genie index  

result = pd.read_csv("results/visual/result.csv")
result_times = np.array(result["total_time"].tolist())

current = pd.read_csv("results/visual/current.csv")
current_times = np.array(current["total_time"].tolist())

original = pd.read_csv("data/output.csv")
original_time = original.iloc[:len(result), :]['ridetime'] - original.iloc[:len(result), :]['desiredtime']

def get_genie(waiting_times):
    waiting_times = np.sort(waiting_times)

    population = np.arange(1, len(waiting_times) + 1) / len(waiting_times)
    cumulative_waiting_times = np.cumsum(waiting_times) / np.sum(waiting_times)

    lorenz_curve = np.vstack((np.append([0], population), np.append([0], cumulative_waiting_times)))

    area_under_curve = np.trapz(lorenz_curve[1], lorenz_curve[0])
    gini_index = 1 - 2 * area_under_curve
    return lorenz_curve, gini_index

def plot_lorenz(lorenz_curve1, lorenz_curve2, lorenz_curve3):
    plt.figure(figsize=(10, 5))
    plt.plot(lorenz_curve1[0], lorenz_curve1[1], label='result', color='r', zorder=1)
    plt.plot(lorenz_curve2[0], lorenz_curve2[1], label='current', color='b')
    plt.plot(lorenz_curve3[0], lorenz_curve3[1], label='original', color='g')
    plt.plot([0, 1], [0, 1], color='r', linestyle='--', label='Perfect equality')
    plt.fill_between(lorenz_curve1[0], lorenz_curve1[1], alpha=0.2)
    plt.fill_between(lorenz_curve2[0], lorenz_curve2[1], alpha=0.2)
    plt.fill_between(lorenz_curve3[0], lorenz_curve3[1], alpha=0.2)
    plt.xlabel('Cumulative Proportion of Population')
    plt.ylabel('Cumulative Proportion of Waiting Times')
    plt.title('Lorenz Curve')
    plt.legend()
    plt.show()

lorenz_res, genie_res = get_genie(result_times)
lorenz_curr, genie_curr = get_genie(current_times)
lorenz_org, genie_org = get_genie(original_time)

plot_lorenz(lorenz_res, lorenz_curr, lorenz_org)

print("result: ", genie_res)
print("current: ", genie_curr)
print("original: ", genie_org)

# %% count number of people who waited more than 60 minutes

result = pd.read_csv("results/visual/result.csv")
result_times = np.array(result["total_time"].tolist())

current = pd.read_csv("results/visual/current.csv")
current_times = np.array(current["total_time"].tolist())

original = pd.read_csv("data/output.csv")
original_time = original.iloc[:len(result), :]['ridetime'] - original.iloc[:len(result), :]['desiredtime']

def count_more_than_60(waiting_times):
    count = 0
    for time in waiting_times:
        if time > 60:
            count += 1
    return count

print("result: ", count_more_than_60(result_times))
print("current: ", count_more_than_60(current_times))
print("original: ", count_more_than_60(original_time))

#%% 

import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV files
df1 = pd.read_csv("results/effect_c/_results.csv")
df2 = pd.read_csv("results/effect_c/_results_c.csv")

# Calculate the ratio of 'a' and '(a + b)', and add it as a new column 'a_ab_ratio'
df2['a_ab_ratio'] = df2['a'] / (df2['a'] + df2['b'])
df1['a_ab_ratio'] = df1['a'] / (df1['a'] + df1['b'])

# Group by 'a_ab_ratio' and find the row with minimum 'mean_time' in each group
best_results = df2.loc[df2.groupby('a_ab_ratio')['mean_time'].idxmin()]

print("The best results of varying 'c' in terms of less 'mean_time' for each 'a/(a+b)' ratio are:")
print(best_results)

x = df1['a_ab_ratio'].tolist()
# Plot histogram to show the effect of 'c' on 'mean_time'

bar_width = 0.3
# Set the positions of the bars
r1 = np.arange(len(df1))
r2 = [x + bar_width for x in r1]

# Create the bar plot
plt.figure(figsize=(10, 6))
plt.bar(r2, best_results['mean_time'], width=bar_width, color='#BF2323', label='considering destination demand')
plt.bar(r1, df1['mean_time'], width=bar_width, color='#6D6D6DE3', label='w/o considering destination demand')
plt.xlabel('a : b ratio')
plt.ylabel('Mean time')
plt.xticks([r + bar_width/2 for r in range(len(df1))], np.round(df1['a_ab_ratio'], 2))
plt.legend()
plt.show()

# %% visualize the effect of supply of more cars

df = pd.read_csv("results/plus.csv")

data = {
    'additional_supply': [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100],
    'mean_time': [35.09634888438134, 34.122718052738335, 33.20993914807302, 32.294117647058826, 31.4158215010142, 31.176470588235293, 30.907707910750506, 30.440162271805274, 29.851926977687626, 30.080121703853955, 30.05476673427992, 29.253549695740364, 29.129817444219068, 29.23732251521298, 28.815415821501013, 28.67342799188641, 28.275862068965516, 28.02028397565923, 27.78397565922921, 27.691683569979716],
    'equity_measure': [71.49491525423728, 69.06440677966101, 68.63728813559322, 66.11864406779661, 64.58983050847458, 64.65084745762712, 63.75593220338983, 62.90169491525424, 61.9728813559322, 61.97627118644068, 62.349152542372885, 60.45084745762712, 60.23050847457627, 60.355932203389834, 59.355932203389834, 58.92203389830509, 58.03728813559322, 57.76949152542373, 57.06440677966102, 57.271186440677965]
}

# Create a DataFrame from the data
df = pd.DataFrame(data)

data = {
    'additional_supply': [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100],
    'mean_time': [35.09634888438134, 34.122718052738335, 33.20993914807302, 32.294117647058826, 31.4158215010142, 31.176470588235293, 30.907707910750506, 30.440162271805274, 29.851926977687626, 30.080121703853955, 30.05476673427992, 29.253549695740364, 29.129817444219068, 29.23732251521298, 28.815415821501013, 28.67342799188641, 28.275862068965516, 28.02028397565923, 27.78397565922921, 27.691683569979716],
    'equity_measure': [71.49491525423728, 69.06440677966101, 68.63728813559322, 66.11864406779661, 64.58983050847458, 64.65084745762712, 63.75593220338983, 62.90169491525424, 61.9728813559322, 61.97627118644068, 62.349152542372885, 60.45084745762712, 60.23050847457627, 60.355932203389834, 59.355932203389834, 58.92203389830509, 58.03728813559322, 57.76949152542373, 57.06440677966102, 57.271186440677965]
}

df = pd.DataFrame(data)

bar_width = 2
fig, ax = plt.subplots()
ax.bar(df['additional_supply'] - bar_width/2, 
       df['mean_time'], 
       color = "#BF2323", 
       label='Waiting time avg.', width=bar_width)
ax.bar(df['additional_supply'] + bar_width/2, df['equity_measure'], 
       color = "#6D6D6DED", 
       label='Top 30% waiting time avg.', width=bar_width)
ax.set_xlabel('Additional supplies (vehicles)')
ax.set_xticks([5, 15, 25, 35, 45, 55, 65, 75, 85, 95])
ax.set_xticklabels(df['additional_supply'])
ax.set_ylabel('Waiting time avg. (min)')
ax2 = ax.twinx()
ax2.set_yticks(ax.get_yticks())
ax2.set_ylabel('Top 30% waiting time avg. (min)')
ax.legend()
plt.show()



# %%
