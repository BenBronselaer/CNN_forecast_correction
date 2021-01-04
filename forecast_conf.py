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
x_location=271.5
y_location=28.19

# size of image to consider, in +/- from data location, in number of pixels
range_pixels=25

# which lead time to train on
target_lead_time=30

# how many extra data points to take on either side of the desired lead time, in order to increase data points
# note that forecasts are issued every week, so shouldn't use more 6 days before/after
extra_data_lead_times = 2

# number of forecasts tested per batch, we take two batches
test_forecasts_per_set=3

# first forecasts of each batch
test_time_1=27
test_time_2=35