"""
Author: Henry Powell
Institution: Institute of Neuroscience and Psychology, University of Glasgow, UK.

This program takes a csv file of positions of motion tracking markers and turns them into a point light display using
the X, Z coordinate axes. This has only been tested on Vicon data but there's no reason it shouldn't work on data from
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


def process_data(file):
    """
    This function processes the raw data file so drop all the data we don't need to make the point light display.
    :param file: CSV file containing mo cap position data (X,Y,Z)
    :return: A modified version of the data with no empty columns on the far right side, and no y-axis.
    """
    num_cols = pd.read_csv(file).shape[1]
    col_names = [str(i) for i in range(num_cols)]

    raw_data = pd.read_csv(file, names=col_names)
    non_data = ['0']

    # This makes the assumption that the data file has mostly empty columns after column 119 (but this should be
    # checked) If these columns are not empty and you want to include the data then comment out these two lines
    # or amend them.
    non_data.append(str(i) for i in range(119, raw_data.shape[1]))
    non_data = [i for j in non_data for i in j]
    raw_data = raw_data.drop(non_data, axis=1)

    # This drops the y-axis from the the data set
    drop_y = [str(i) for i in range(2, 119, 3)]
    raw_data = raw_data.drop(drop_y, axis=1)

    col_names = [str(i) for i in range(raw_data.shape[1])]

    raw_data.columns = col_names

    return raw_data


def find_min_max(data):
    """
    Function to find the min and max x and z values in the whole data set. These values can then be used to set the
    limits of the x and y axes of the plots that are used as frames in the resulting point light display.
    :param data:
    :return:
    """
    min_x = data.min()
    min_x = int(np.min(min_x[::2]))
    max_x = data.max()
    max_x = int(np.max(max_x[::2]))

    min_y = data.min()
    min_y = int(np.min(min_y[1::2]))
    max_y = data.max()
    max_y = int(np.max(max_y[1::2]))

    return min_x, max_x, min_y, max_y


def make_PL_display(data, min_x, max_x, min_y, max_y):
    """
    Function that outputs plots with the locations of each of the position markers in 2D space. The function iterates
    over rows in the data set to create a sequence of these plots that act as frames in the resulting point light
    display.
    :param data: The processed data set which is to be turned into a point light display.
    :param min_x: The minimum value of the x-axis of the outputted plots.
    :param max_x: The maximum value of the x-axis of the outputted plots.
    :param min_y: The minimum value of the y-axis of the outputted plots.
    :param max_y: The maximum value of the y-axis of the outputted plots.
    :return:
    """
    # Change "raw_data.shape[0]" to any integer < the total number of frames (rows) in the data set. This will determine
    # how many frames of data to turn into an animation.
    num_frames = data.shape[0]

    # This for-loop cycles through the data by rows creating an x-position vector and y-position vector from all the
    #  markers at each time step. It then plot these as a scatter plot and saves the plot to the current working
    # directory.
    num = 1
    for i in range(num_frames):
        fig = plt.figure()
        plt.rcParams['axes.facecolor'] = 'black'
        x = []
        y = []
        for j in [n for n in range(0, 77, 2)]:
            x.append(data[str(j)][i])
        for k in [n for n in range(1, 78, 2)]:
            y.append(data[str(k)][i])
        plt.scatter(x, y, color='w')
        plt.xlim(min_x, max_x)
        plt.ylim(min_y, max_y)
        plt.xticks([])
        plt.yticks([])
        plt.savefig(str(num))
        plt.close(fig)
        num += 1

# Run the functions
data = process_data(file)
min_x, max_x, min_y, max_y = find_min_max(data)
make_PL_display(data, min_x, max_x, min_y, max_y)
