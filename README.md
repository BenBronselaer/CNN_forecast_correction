# CNN_forecast_correction
code to train and apply a CNN model to improve ensemble current forecast

The files in this directory as the following:

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
