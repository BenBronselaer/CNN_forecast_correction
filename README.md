# CNN_forecast_correction
Code to train and apply a CNN model to improve ensemble current forecast.

The forecast model outputs 2D fields of current speed, current direction and sea surface temperature for each lead time in the forecast. The forecast model has been found to show skill over simply climatology by comparing it against current speed data measured at a given location. The idea here is to use the 2D fields as images to train a convolutional neural net to then predict the ensemble error relative to the measurements, using a set of historic forecasts. The point of using the CNN is to capture spatial features in the current that might be interpreted by the CNN. 



The files in this directory:

### 1. Jupyter notebook 'Process_CNN_correction'
  This notebook is where the convolutional neural network is trained. Can be run as a jupyter notebook as individual cells, or exported as python script and run in a terminal. 
  
  The notebook reads in the data, organized it, train the network and plots some diagnostics of the training and the testing results.
  
  Note that the current model forecast and current measurements are private data so are not uploaded.


### 2. Python script 'main_example'
  This script simply reads a forecast, loads the pre-trained CNN model weights and performs the correction
  
### 3. forecast_conf.py
  This file contains a set of paramaters for training and running the CNN model, in both the files listed above
  
### 4. forecast_helper.py
  Defines a forecast class with methods to be used in main_example. The forecast class is made up of the components developed in the jupyter notebook
  
### 5. helper_functions.py
  Defines helper functions used in the main files above
