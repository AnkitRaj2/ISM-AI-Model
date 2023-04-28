# Library for collecting computer resource utilization data
import psutil

# Library for data visualization
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Library for obtaining user preferences
import sys

# Stores utilization data in text files
file1 = open("CPU_data-2.txt", "w")
file2 = open("RAM_data-2.txt", "w")

elapsed_time = []
CPU_data = []
RAM_data = []

# Plots data points
fig, ax = plt.subplots()
line1, = ax.plot(elapsed_time, CPU_data)
line2, = ax.plot(elapsed_time, RAM_data)

i = 0

# Function for collecting data in real-time
def update(frame):
    global i
    
    ax.clear()
    
    elapsed_time.append(i)
    
    # Records CPU utilization data every second
    CPU_data.append(psutil.cpu_percent(1))
    
    # Records RAM utilization data every second
    RAM_data.append(psutil.virtual_memory()[2])
    
    # Writes data to text file in following format: "elapsed_time utilization_percentage"
    file1.write(str(i) + " " + str(CPU_data[len(CPU_data) - 1]) + "\n")
    file2.write(str(i) + " " + str(RAM_data[len(RAM_data) - 1]) + "\n")
    
    # Plots data points
    ax.plot(elapsed_time, CPU_data)
    ax.plot(elapsed_time, RAM_data)
    ax.set_xlabel('Time Elapsed (Seconds)')
    ax.set_ylabel('Resource Utilization (%)')
    
    i += 1

# Repeatedly collects data
animation = FuncAnimation(fig, update, cache_frame_data=False)

# Displays graph of data based on user preference for viewing data visualization
if len(sys.argv) == 2:
    plt.show()