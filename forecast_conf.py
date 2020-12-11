#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


@author: Ben
"""

# set some parameters

# which forecast to use for final calculation
f_directory = './20140302'

# directory where model weights are stored
model_directory = './checkpoint/'

# location of data
xc=271.5
yc=28.19

# size of image to consider, in +/- from data location, in number of pixels
range_pix=25

# which lead time to train on
t_hor=30

# how many extra data points to take on either side of the desired lead time, in order to increase data points
# note that forecasts are issued every week, so shouldn't use more 6 days before/after
t_ex = 2

# number of forecasts tested per batch, we take two batches
I_range=3

# first forecasts of each batch
T1=27
T2=35