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
file = '/Users/henryp/PycharmProjects/PointLightDisplay/RebeccaData/missing_reb_data.csv'


def process_data(file):
    """
    This function processes the raw data file so drop all the data we don't need to make the point light display.
    :param file: CSV file containing mo cap position data (X,Y,Z)
    :return: A modified version of the data with no empty columns on the far right side, and no y-axis.
    """
    num_cols = pd.read_csv(file).shape[1]
    col_names = [str(i) for i in range(num_cols)]

    raw_data = pd.read_csv(file, names=col_names)
    # non_data = ['0']

    # This makes the assumption that the data file has mostly empty columns after column 119 (but this should be
    # checked) If these columns are not empty and you want to include the data then comment out these two lines
    # or amend them.
    # print(raw_data)
    # non_data.append(str(i) for i in range(119, raw_data.shape[1]))
    # non_data = [i for j in non_data for i in j]
    # raw_data = raw_data.drop(non_data, axis=1)

    col_names = [str(i) for i in range(raw_data.shape[1])]

    raw_data.columns = col_names

    return raw_data


def find_min_max(data, dims=['x', 'y']):
    """
    Function to find the min and max x and z values in the whole data set. These values can then be used to set the
    limits of the x and y axes of the plots that are used as frames in the resulting point light display.
    :param data:
    :return:
    """
    dims = [0 if i == 'x' else i for i in dims]
    dims = [1 if i == 'y' else i for i in dims]
    dims = [2 if i == 'z' else i for i in dims]

    min_x = data.min()
    min_x = int(np.min(min_x[dims[0]::3]))
    max_x = data.max()
    max_x = int(np.max(max_x[dims[0]::3]))

    min_y = data.min()
    min_y = int(np.min(min_y[dims[1]::3]))
    max_y = data.max()
    max_y = int(np.max(max_y[dims[1]::3]))

    return min_x, max_x, min_y, max_y


def make_PL_display(data, min_x, max_x, min_y, max_y, dims=['x', 'y']):
    """
    Function that outputs plots with the locations of each of the position markers in 2D space. The function iterates
    over rows in the data set to create a sequence of these plots that act as frames in the resulting point light
    display.
    :param data: The processed data which is to be turned into a point light display.
    :param min_x: The minimum value of the x-axis of the outputted plots.
    :param max_x: The maximum value of the x-axis of the outputted plots.
    :param min_y: The minimum value of the y-axis of the outputted plots.
    :param max_y: The maximum value of the y-axis of the outputted plots.
    :param dims: List of strings containing the axes of the data you wish to represent in the point light display. I.e.
    ['x', 'y'] if you want the PLD to show the movement in the x,y plane.
    :return:
    """

    dims = [0 if i == 'x' else i for i in dims]
    dims = [1 if i == 'y' else i for i in dims]
    dims = [2 if i == 'z' else i for i in dims]

    # Change "data.shape[0]" to any integer < the total number of frames (rows) in the data set. This will determine
    # how many frames of data to turn into an animation.
    num_frames = data.shape[0]

    # This for-loop cycles through the data by rows creating an x-position vector and y-position vector from all the
    #  markers at each time step. It then plots these as a scatter plot and saves the plot to the current working
    # directory.
    num = 1
    for i in range(num_frames):
        x = data.iloc[i][dims[0]::3]
        y = data.iloc[i][dims[1]::3]

        fig = plt.figure()
        plt.rcParams['axes.facecolor'] = 'black'
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
min_x, max_x, min_y, max_y = find_min_max(data, dims=['x', 'z'])
make_PL_display(data, min_x, max_x, min_y, max_y, dims=['x', 'z'])

