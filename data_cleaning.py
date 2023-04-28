# Libraries for data analysis
import numpy as np
from sklearn.cluster import DBSCAN
import pandas as pd

# Library for data visualization
import matplotlib.pyplot as plt

# Library for obtaining user preferences
import sys

# Reads utilization data from text file
file = open("CPU_data-0.txt", "r")

elapsed_time = []
utilization_data = []

# Stores user preference for viewing data visualization
graph_plots = True if len(sys.argv) == 2 else False

if graph_plots:
    fig, ax1 = plt.subplots()
    fig, ax2 = plt.subplots()

line = file.readline()
while len(line) > 0:
    elapsed_time.append(int(line.split()[0]))
    utilization_data.append(float(line.split()[1]))
    line = file.readline()
    
file.close()

# Deletes first and last 30 data points to eliminate effects of spikes due to program execution and termination

elapsed_time = elapsed_time[30:]
elapsed_time = elapsed_time[:-30]

utilization_data = utilization_data[30:]
utilization_data = utilization_data[:-30]

# Plots raw data points
if graph_plots:
    ax1.plot(elapsed_time, utilization_data)
    ax1.set_xlabel('Time Elapsed (Seconds)')
    ax1.set_ylim(-5, 105)
    ax1.set_ylabel('Resource Utilization (%)')

# ----------------------------------------------------------------------------------------------------

# Stores time values of major spikes in data
major_spikes_time_values = []

# Function for removing minor spikes (small fluctuations) in data for a specified number of rounds
def remove_minor_spikes(rounds):
    global utilization_data
    
    # Smoothes data using moving average with window of 10 data points
    
    window_size = 10
    
    smoothed_data = np.zeros_like(utilization_data)
    
    for round in range(rounds):
        # Threshold for detecting spikes
        spike_threshold = np.std(utilization_data)
        
        for i in range(len(utilization_data)):
            # Skip edges where window is not fully available
            if i < window_size//2 or i >= len(utilization_data) - window_size//2:
                smoothed_data[i] = utilization_data[i]
            # Calculate moving average for neighboring data points within threshold
            else:                
                neighbors = utilization_data[i - window_size//2: i + window_size//2 + 1]
                
                if np.max(neighbors) - np.min(neighbors) > spike_threshold:
                    # If spike detected, skip smoothing for that data point
                    smoothed_data[i] = utilization_data[i]
                    
                    # Adds time values corresponding to major spikes during last round of data smoothing
                    if round == rounds - 1:
                        major_spikes_time_values.append(i)
                else:
                    # Performs moving average for non-spike data points
                    smoothed_data[i] = np.mean(neighbors)
                    
        utilization_data = np.copy(smoothed_data)
        
# ----------------------------------------------------------------------------------------------------
        
# Removes minor fluctuations after 1st layer of data cleaning
remove_minor_spikes(100)

# ----------------------------------------------------------------------------------------------------

major_spikes_boundaries = [major_spikes_time_values[0]]

for i in range(len(major_spikes_time_values)):
    if i > 0 and major_spikes_time_values[i] - major_spikes_time_values[i - 1] > 1:
        major_spikes_boundaries.append(major_spikes_time_values[i - 1])
        major_spikes_boundaries.append(major_spikes_time_values[i])
        
major_spikes_boundaries.append(major_spikes_time_values[len(major_spikes_time_values) - 1])

for i in range(len(major_spikes_boundaries) // 2):
    minimum = np.min(utilization_data[major_spikes_boundaries[2 * i] : major_spikes_boundaries[2 * i + 1] + 1])
    
    for time_value in range(major_spikes_boundaries[2 * i], major_spikes_boundaries[2 * i + 1] + 1):
        utilization_data[time_value] = minimum

# General clustering to identify average utilization percentages
        
standard_deviation = np.std(utilization_data)

average_value_transitions = []

for i in range(5, len(utilization_data) - 5):
    neighbors = utilization_data[i - 5 : i + 5]
    
    if np.max(neighbors) - np.min(neighbors) > standard_deviation:
        average_value_transitions.append(i)
        
transition_clusters = [0, average_value_transitions[0]]

for i in range(len(average_value_transitions)):
    if i > 0 and average_value_transitions[i] - average_value_transitions[i - 1] > 1:
        transition_clusters.append(average_value_transitions[i - 1])
        transition_clusters.append(average_value_transitions[i])

transition_clusters.append(average_value_transitions[len(average_value_transitions) - 1])
transition_clusters.append(len(utilization_data) - 1)

for i in range(len(transition_clusters) // 2):
    cluster_with_spikes = utilization_data[transition_clusters[2 * i] : transition_clusters[2 * i + 1] + 1]
    average = np.mean(cluster_with_spikes)
    standard_deviation = np.std(cluster_with_spikes)
    
    cluster_without_spikes = [value for value in cluster_with_spikes if value - average < standard_deviation]
    if len(cluster_without_spikes) > 0:
        average = np.mean(cluster_without_spikes)
    
    for j in range(len(cluster_with_spikes)):
        if cluster_without_spikes.count(cluster_with_spikes[j]) == 0:
            cluster_with_spikes[j] = average
            
        utilization_data[j + transition_clusters[2 * i]] = cluster_with_spikes[j]

# ----------------------------------------------------------------------------------------------------

# Removes minor fluctuations after 2nd layer of data cleaning
remove_minor_spikes(100)

# ----------------------------------------------------------------------------------------------------

for i in range(len(transition_clusters) - 1):
    min_data_points_in_cluster = 50
    
    if transition_clusters[i + 1] - transition_clusters[i] >= min_data_points_in_cluster:
        sorted_values = np.sort(utilization_data[transition_clusters[i] : transition_clusters[i + 1] + 1])
        median = np.median(sorted_values)
        quartile_1 = np.median(sorted_values[:len(sorted_values) // 2])
        quartile_3 = np.median(sorted_values[(len(sorted_values) // 2):])
        interquartile_range = quartile_3 - quartile_1

        for j in range(transition_clusters[i], transition_clusters[i + 1] + 1):
            if utilization_data[j] > quartile_3 + 1.5 * interquartile_range or utilization_data[j] < quartile_1 - 1.5 * interquartile_range:
                utilization_data[j] = median
    else:
        median = np.median(np.sort(utilization_data[transition_clusters[i] : transition_clusters[i + 1] + 1]))
        
        for j in range(transition_clusters[i], transition_clusters[i + 1] + 1):
            utilization_data[j] = median

# DBSCAN (Density-Based Spatial Clustering of Applications with Noise) clustering to identify insignificant clusters

dbscan = DBSCAN(eps=np.std(utilization_data), min_samples=5)
labels = dbscan.fit_predict(np.column_stack((elapsed_time, utilization_data)))

core_samples_mask = np.zeros_like(dbscan.labels_, dtype=bool)
core_samples_mask[dbscan.core_sample_indices_] = True
    
# Finds time values of jumps in average utilization percentage
cluster_jumps = []

for i in range(1, len(labels)):
    if labels[i] != labels[i - 1]:
        cluster_jumps.append(i)

# ----------------------------------------------------------------------------------------------------

# Removes minor fluctuations after 3rd layer of data cleaning
remove_minor_spikes(10)

# ----------------------------------------------------------------------------------------------------

# Plots cleaned data points
if graph_plots:
    ax2.plot(elapsed_time, utilization_data)
    ax2.set_xlabel('Time Elapsed (Seconds)')
    ax2.set_ylim(-5, 105)
    ax2.set_ylabel('Resource Utilization (%)')

df = pd.DataFrame({'List1': elapsed_time, 'List2': utilization_data})

df.to_excel('sheet_0.xlsx', header=False, index=False)

# Displays graphs of raw and cleaned data
if graph_plots:
    plt.show()