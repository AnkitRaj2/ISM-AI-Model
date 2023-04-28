# Libraries for data analysis
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Library for collecting computer resource utilization data
import psutil

# Library for controlling screen brightness
import screen_brightness_control as sbc

# Library for data visualization
import matplotlib.pyplot as plt

# Library for obtaining user preferences
import sys

# Read Excel files into pandas DataFrame and
# extracts resource utilization and screen brightness data from second and third columns

df = pd.read_excel('sheet_0.xlsx')

utilization_data = df.iloc[:, 1].tolist()
screen_brightness = df.iloc[:, 2].tolist()

df = pd.read_excel('sheet_1.xlsx')

utilization_data += df.iloc[:, 1].tolist()
screen_brightness += df.iloc[:, 2].tolist()

df = pd.read_excel('sheet_2.xlsx')

utilization_data += df.iloc[:, 1].tolist()
screen_brightness += df.iloc[:, 2].tolist()

# Reshapes utilization data into two-dimensional array
utilization_data = np.array(utilization_data).reshape(-1, 1)

# Performs ordinary least-squares linear regression to predict screen brightness levels using utilization data 

regression_model = LinearRegression()
regression_model.fit(utilization_data, screen_brightness)

screen_brightness_predictions = regression_model.predict(utilization_data)
slope = regression_model.coef_[0]
intercept = regression_model.intercept_

# Displays scatter plot and least-squares linear regression line based on user preference for viewing data visualization
if len(sys.argv) == 2:
    plt.scatter(utilization_data, screen_brightness, color='blue', label='Data Points')
    plt.plot(utilization_data, screen_brightness_predictions, color='red', label='Least Squares Line')
    plt.xlabel('Resource Utilization (%)')
    plt.ylabel('Screen Brightness (%)')
    plt.legend()
    plt.show()

# Predicts screen brightness for current utilization percentage using regression model
predicted_brightness = int(slope * psutil.cpu_percent(1) + intercept)

# Stores screen brightness level predictions in text file
file = open("output.txt", "a")
file.write(str(predicted_brightness) + "\n")

# Sets actual screen brightness level to predicted value
sbc.set_brightness(predicted_brightness)