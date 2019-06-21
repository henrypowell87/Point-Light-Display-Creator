# Point-Light-Display-Creator

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
