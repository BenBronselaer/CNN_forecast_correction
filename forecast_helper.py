#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 16:54:41 2020

@author: Ben
"""

import pandas as pd
import xarray as xr
import numpy as np
import zarr
import scipy.stats as stats
from datetime import datetime, timedelta
import os
from scipy.io import loadmat
from helper_functions import standardize_dims
from forecast_conf import (xc,yc,range_pix,t_hor,t_ex,I_range,T1,T2)


class forecast:
    
    
    
    def __init__(self,f_dir):
        self.f_dir=f_dir
        
    def print_dir(self):
        print(self.f_dir)

    def load_forecast(self):
        # xc = longitude coordinate
        # yc = latitude coordinate
        # ld_time = lead time of forecast
        
        
        # parameters used for indexing
        dirx=0
        f_list=[]
        X_data=np.empty((32,2*range_pix,2*range_pix,4))
        mod=np.empty((32,))

        temp=[x[2] for x in os.walk(self.f_dir)]
        for m in temp[0]:
            if m.find('.nc') > 0:
                f_list.append(self.f_dir+'/'+m)       
        f_list.sort()

        
        arr=xr.open_dataset(f_list[0])
        arr=standardize_dims(arr)
        lat=abs(arr.lat-yc)
        lon=abs(arr.lon-xc)
        yc_i=np.argmin(lat).values
        xc_i=np.argmin(lon).values
        
        dir_p=f_list[0][2:10]
        
        
        for k in f_list:
            # check if moving to new forecast
            if k[2:10] != dir_p:
                dirx+=1
                dir_p=k[2:10]
        
            # calculate forecast lead time, in days
            date1 = datetime.strptime(k[24:32], '%Y%m%d')
            date2 = datetime.strptime(k[33:41], '%Y%m%d')
            dys=(date2-date1).days
    
            # only save data if it is used for training, which is defined by main lead time, and +/- chosen days
            if dys==t_hor:
    
                arr=xr.open_dataset(k)
                arr=standardize_dims(arr)
                # load sea surface temperature
                t=arr.water_temp_mb.squeeze()
                # load current speed
                s=100*np.sqrt(arr.water_u_mb**2+arr.water_v_mb**2).squeeze()
                # load current direction
                ddir = np.arctan2(arr.water_u_mb, arr.water_v_mb).squeeze()
                # select (x,y) window
                t=t[:,yc_i-range_pix:yc_i+range_pix,xc_i-range_pix:xc_i+range_pix]
                s=s[:,yc_i-range_pix:yc_i+range_pix,xc_i-range_pix:xc_i+range_pix]
                ddir=ddir[:,yc_i-range_pix:yc_i+range_pix,xc_i-range_pix:xc_i+range_pix]
                # calculate ensemble means
                tm=t.mean(dim='ENSEMBLE')
                sm=s.mean(dim='ENSEMBLE')
                ddirm=ddir.mean(dim='ENSEMBLE')
    
 


                for k in range(32):

                    # put data into the array used for training and testing
                    # here, you can choose which fields to use (speed, direction, seas surface temperature)
                    # potential to add other measurement, and/or reanalyses fields such as wind, in the future
                    X_data[k,:,:,0]=s[k%s.shape[0],:,:].values
                    X_data[k,:,:,1]=sm.values
                    X_data[k,:,:,2]=ddir[k%s.shape[0],:,:].values
                    #X_data[dirx,dys-(t_hor-t_ex),k,:,:,3]=ddirm.values           
                    X_data[k,:,:,3]=t[k%s.shape[0],:,:].values
                    #X_data[dirx,dys-(t_hor-t_ex),k,:,:,3]=tm.values        
                    
                    mod[k]=s[k%s.shape[0],:,:].sel(lon=xc,lat=yc, method="nearest").squeeze().values
        self.X_data=X_data
        self.mod = mod
        return mod, X_data
        
    
    def correct_forecast(self,model_dir):
        
        
        import tensorflow as tf

        from tensorflow.keras import datasets, layers, models, regularizers
        import matplotlib.pyplot as plt

        model = models.Sequential()
        model.add(layers.Conv2D(8, (3, 3), activation='relu', input_shape=(2*range_pix,2*range_pix, 4)))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(16, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(32, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        #model.add(layers.Conv2D(32, (3, 3), activation='relu'))
        model.add(layers.Flatten())
        model.add(layers.Dense(8, activation='relu',kernel_regularizer=regularizers.l2(0.01)))
        model.add(layers.Dropout(0.5))
        model.add(layers.Dense(1))
        
        model.compile(optimizer='adam', loss='mean_squared_error')
        
        model.load_weights(model_dir)
        
        P=model.predict(self.X_data)
        
        p = self.mod+np.mean(P)
        
        self.mod_correct = p
        
        return p
        
        
