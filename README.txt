Note: This version of the artificial intelligence model only works on Windows operating systems.

To run the model, execute the "run.vbs" file.

Explanation of model:

The artificial intelligence model is intended to predict screen brightness levels in real-time by performing least-squares linear regression on resource utilization 
data of components such as the CPU (central processing unit) and RAM (random access memory). In particular, the model utilizes ordinary least-squares regression to
make brightness level predictions. The model involves three stages: data collection, data cleaning, and linear regression. Throughout these stages, it makes use of the
following Python libraries: numpy, pandas, sklearn, psutil, screen_brightness_control, matplotlib, and sys. numpy, pandas, and sklearn are utilized for data analysis
and linear regression; psutil and screen_brightness_control is used for data collection; and matplotlib and sys are used for data visualization.

The first stage, data collection, makes use of the psutil, matplotlib, and sys libraries and is performed through the "data_collection.py" file. Each second, CPU and
RAM utilization data are collected using the psutil library and stored in two text files, one for each type of resource usage. Simultaneously, the real-time resource
usage data are added as data points in a graph. The sys library is used to obtain the user's preference to visualize the data collection by viewing the graph using the
matplotlib library as the process occurs.

The second stage, data cleaning, makes use of the numpy, pandas, sklearn, matplotlib, and sys libraries and is performed through the "data_cleaning.py" file. First,
resource utilization data is read from the text files created as a result of the data collection stage. Then, the first and last 30 data points are removed from the
data set to eliminate the effects of spikes in usage percentages resulting from the execution and termination of the "data_collection.py" file. Next, multiple layers
of data cleaning are performed using the numpy and sklearn libraries, each consisting of a distinct data cleaning algorithm and a common algorithm to remove any minor
spikes resulting from the handling of the data by the corresponding distinct algorithm. The first layer consists of only the common algorithm. The second layer 
consists of the removal of major spikes and the general clustering of the data to identify average utilization percentages over the durations of distinct clusters. The
The third layer performs DBSCAN (Density-Based Spatial Clustering of Applications with Noise) clustering of the data to identify the precise time values at which the
average utilization percentage shifts from one cluster to another. Finally, the pandas library is used to store the data in an Excel file, with elapsed time values
and utilization percentages stored in the first and second columns, respectively. Finally, the sys library is used to obtain the user's preference to visualize the raw
and cleaned data in the form of "before-and-after" graphs using the matplotlib library. The Excel file is manually modified to store brightness values in the third 
column based on utilization percentage ranges in the second column.

Note: In future versions of the model, the storage of brightness values in the third column will be automated.

The final stage, linear regression, makes use of all of the above-mentioned libraries and is performed through the "linear_regression.py" file. First, the utilization 
percentages and brightness values are read from the Excel file created by the data cleaning stage using the pandas library and stored into two lists. Then, the numpy
and sklearn libraries are used to create a least-squares linear regression model that predicts screen brightness levels based on utilization percentages from the data
stored in the lists. Additionally, the sys library is used to obtain the user's preference to visualize the scatter plot and regression model using the matplotlib 
library. Finally, the regression model is used to predict screen brightness levels in real-time based on current resource utilization, and the actual screen brightness 
level is set to the new, predicted level using the screen_brightness_control library, and the predicted level is written to a text file that can be used to verify that
the overall model is functioning.

The "run.vbs," "ai_model.bat," and "linear_regression.py" files are responsible for the execution of the artificial intelligence model. The purpose of the
"ai_model.bat" file is to initiate the continuous execution of the "linear_regression.py" file with a time delay of 15 seconds. The purpose of the "run.vbs" file is to
initiate the execution of "ai_model.bat" without opening a new Command Prompt window, which is the default behavior of a batch file. Together, the three files
contribute to the indefinite execution of the artificial intelligence model as a background process.

Note: In future versions of the model, the user will have control over the execution and termination of the model through a graphical user interface. Additionally, the
user will have the option to initiate the model's execution upon computer startup to entirely eliminate the need to manually execute the model.

Since a computer's screen brightness level is considered a major determinant of the computer's operating time on a full charge, the model is intended to optimize the
computer's overall battery life by assigning relatively low brightness levels during periods of low resource usage. This optimization relies on the expected, generally
positive correlation between resource usage and computer activity, due to which the impact on the user's productivity while using the model is expected to be
negligible. As a result, the model is intended to prove the most beneficial in areas predominantly involving heavy resource usage, such as gaming, video editing and 
rendering, and general content creation. Users with professions in these areas can expect a minimum of 20 percent improvement in battery life through the model.

Note: In future versions of the model, the user will have the option to modify various parameters determining the model's performance, including the data sampling rate
(set to a default of 15 seconds) and the type of regression model used to predict real-time screen brightness levels.