### Function for n-dimensional seismic facies training /classification using Convolutional Neural Nets (CNN)
### By: Charles Rutherford Ildstad (University of Trondheim), as part of a summer intern project in ConocoPhillips and private work
### Contributions from Anders U. Waldeland (University of Oslo), Chris Olsen (ConocoPhillips), Doug Hakkarinen (ConocoPhillips)
### Date: 26.10.2017
### For: ConocoPhillips, Norway,
### GNU V3.0 lesser license

# Make initial package imports
import random
import numpy as np
import keras


## Import the needed files
from facies_net_func.masterf import *


# Set random seed for reproducability
np.random.seed(7)
# Confirm backend if in doubt
#keras.backend.backend()


#### ---- Run an instance of the master function ----
filenames   = ['F3_entire.segy']    # name of the segy-cube(s) with data
inp_res     = np.float32            # formatting of the input seismic (e.g. np.int8 for 8-bit data, np.float32 for 32-bit data, etc)
cube_incr   = 30                    # number of increments in each direction to create a training cube

# Define the dictionary holding all the training parameters
train_dict = {
    'files'         : ['./class_addresses/multi_else_ilxl.pts','./class_addresses/multi_grizzly_ilxl.pts',
                       './class_addresses/multi_high_amp_continuous_ilxl.pts','./class_addresses/multi_high_amplitude_ilxl.pts',
                       './class_addresses/multi_low_amp_dips_ilxl.pts','./class_addresses/multi_low_amplitude_ilxl.pts',
                       './class_addresses/multi_low_coherency_ilxl.pts','./class_addresses/multi_salt_ilxl.pts',
                       './class_addresses/multi_steep_dips_ilxl.pts'], # list of names of class-adresses
    'epochs'        : 10,       # number of epochs we run on each training ensemble/mini-batch
    'num_train_ex'  : 80000,    # number of training examples in each training ensemble/mini-batch
    'batch_size'    : 32,       # number of training examples fed to the optimizer as a batch
    'val_split'     : 0.3,      # fraction of examples used for validation
    'opt_patience'  : 10,       # number of epochs with the same accuracy before force breaking the training ensemble/mini-batch
    'data_augmentation' : False,    # whether or not we are using data augmentation
    'save_model'    : True,         # whether or not we are saving the trained model
    'save_location' : 'F3/test2'    # file name for the saved trained model
}

# Define the dictionary holding all the prediction parameters
pred_dict = {
    'keras_model'   : keras.models.load_model('F3/test1.h5'), # input model to be used for prediction, to load a model use: keras.models.load_model('write_location')
    'section_edge'  : np.asarray([150, 700, 500, 1000, 150, 1700]), # inline and xline section to be predicted (all depths), must contain xline
    'show_feature'  : False,     # Show the distinct features before they are combined to a prediction
    'xline'         : 775,      # xline used for classification (index)(should be within section range)
    'num_class'     : len(train_dict['files']),     # number of classes to output
    'cord_syst'     : 'segy',   # Coordinate system used, default is 0,0. Set to 'segy' to give inputs in (inline,xline)
    'save_pred'     : True,    # Save the prediction as a segy-cube
    'save_location' : 'test_prediction',       # file name for the saved prediction
    'pred_batch'    : 1        # number of traces used to make batches of mini-cubes that are stored in memory at once
    #'pred_batch' : train_dict['num_train_ex']//(pred_dict['section_edge'][5]-pred_dict['section_edge'][4])    #Suggested value
}


# Run the master function and save the output in the output dictionary output_dict
output_dict1 = master(
    segy_filename   = filenames,    # Seismic filenames
    inp_format      = inp_res,      # Format of input seismic
    cube_incr       = cube_incr,    # Increments in each direction to create a training cube
    train_dict      = train_dict,   # Input training dictionary
    pred_dict       = pred_dict,    # Input prediction dictionary
    mode            = 'full'     # Input mode ('train', 'predict', or 'full' for both training AND prediction)
)


# Show additional details about the prediciton
#show_details(
#    filename,
#    cube_incr,
#    output_dict['pred'],
#    inline = 100,
#    inl_start = 75,
#    xline = 169,
#    xl_start = 155,
#    slice_number = 400,
#    slice_incr = 3
#)



### Save/load functions
## returns a prediction cube
## identical to the one saved
#prediction = np.load('filename.npy')
#
## returns a compiled model
## identical to the one saved
#loaded_model = keras.models.load_model('filename.h5')
