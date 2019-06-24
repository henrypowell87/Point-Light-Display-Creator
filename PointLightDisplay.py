"""
Author: Henry Powell
Institution: Institute of Neuroscience and Psychology, University of Glasgow, UK.

This program takes a csv file of positions of motion tracking markers and turns them into a point light display using
the X, Z coordinates axes. This has only been tested on Vicon data but there's no reason it shouldn't work on data from
other mo cap systems.

The program outputs n frames of data as n scatter plots, plotting the x position of the markers on the x-axis and
the z-position of the markers on the y-axis. You will then need to use a program like ffmpeg to animate plots (this can
be done from the commandline by first installing ffmpeg, navigating to the directory containing the plots and typing:

ffmpeg -i %d.png -framerate 30 -pix_fmt yuv420p desired_file_name.mp4

If you are capturing data at high frame rates you will then need to slow down the resulting .mp4 file. This can be done
by typing:

ffmpeg -i previous_movie_filename.mp4 -filter:v "setpts=0.15*PTS" new_movie_file_name.mp4


"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Enter path to data file location
file = ''

num_cols = pd.read_csv(file).shape[1]
col_names = [str(i) for i in range(num_cols)]

raw_data = pd.read_csv(file, names=col_names)
non_data = ['0']

# This makes the assumption that the data file has mostly empty columns after column 119 (but this should be checked)
# If these columns are not empty and you want to include the data then comment out these two lines or amend them.
non_data.append(str(i) for i in range(119, raw_data.shape[1]))
non_data = [i for j in non_data for i in j]
raw_data = raw_data.drop(non_data, axis=1)

# This drops the y-axis from the the data set
drop_y = [str(i) for i in range(2, 119, 3)]
raw_data = raw_data.drop(drop_y, axis=1)
print(raw_data)

col_names = [str(i) for i in range(raw_data.shape[1])]

raw_data.columns = col_names

# Change "raw_data.shape[0]" to any integer < the total number of frames (rows) in the data set. This will determine
# how many frames of data to turn into an animation.
num_frames = raw_data.shape[0]

# Find min and max values in the data to set the fixed axes limits for the plots
min_x = raw_data.min()
min_x = int(np.min(min_x[::2]))
max_x = raw_data.max()
max_x = int(np.max(max_x[::2]))

min_y = raw_data.min()
min_y = int(np.min(min_y[1::2]))
max_y = raw_data.max()
max_y = int(np.max(max_y[1::2]))

# This for-loop cycles through the data by rows creating an x-position vector and y-position vector from all the markers
# at each time step. It then plot these as a scatter plot and saves the plot to the current working directory.
num = 1
for i in range(num_frames):
    fig = plt.figure()
    plt.rcParams['axes.facecolor'] = 'black'
    x = []
    y = []
    for j in [n for n in range(0, 77, 2)]:
        x.append(raw_data[str(j)][i])
    for k in [n for n in range(1, 78, 2)]:
        y.append(raw_data[str(k)][i])
    plt.scatter(x, y, color='w')
    plt.xlim(min_x, max_x)
    plt.ylim(min_y, max_y)
    plt.xticks([])
    plt.yticks([])
    plt.savefig(str(num))
    plt.close(fig)
    num += 1
