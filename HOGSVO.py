import pyzed.camera as zcam
import pyzed.defines as sl
import pyzed.types as tp
import pyzed.core as core
import math
import numpy as np
import sys
import matplotlib.image as mpimg
import cv2
import random
import matplotlib.pyplot as plt
import glob
import time
from skimage.feature import hog
from sklearn.svm import LinearSVC
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import train_test_split
import hdbscan
import pathlib

def slide_window_helper(img, x_start_stop=[None, None], y_start_stop=[None, None], window_size=[64, 64]):
    window_size_x = window_size[0]
    window_size_y = window_size[1]
    xy_overlap=(0, 0)
    # If x and/or y start/stop positions not defined, set to image size
    if x_start_stop[0] == None:
        x_start_stop[0] = 0
    if x_start_stop[1] == None:
        x_start_stop[1] = img.shape[1]
    if y_start_stop[0] == None:
        y_start_stop[0] = 0
    if y_start_stop[1] == None:
        y_start_stop[1] = img.shape[0]
    # Compute the span of the region to be searched    
    xspan = x_start_stop[1] - x_start_stop[0]
    yspan = y_start_stop[1] - y_start_stop[0]
    # Compute the number of pixels per step in x/y
    nx_pix_per_step = np.int(window_size_x*(1 - xy_overlap[0]))
    ny_pix_per_step = np.int(window_size_y*(1 - xy_overlap[1]))
    # Compute the number of windows in x/y
    nx_windows = np.int(xspan/nx_pix_per_step) - 2
    ny_windows = np.int(yspan/ny_pix_per_step) - 2
    # Initialize a list to append window positions to
    window_list = []
    
    ys = y_start_stop[0]
    while ys + window_size_y < y_start_stop[1]: 
        xs = x_start_stop[0]
        while xs < x_start_stop[1]:
            # Calculate window position
            endx = xs + window_size_x
            endy = ys + window_size_y
                        # Append window position to list
            if endy <= img.shape[0] and endx <= img.shape[1]:
                window_list.append((xs, ys, endx, endy))

            xs += nx_pix_per_step

        #window_size_x = int(window_size_x * 1.3)
        #window_size_y = int(window_size_y * 1.3)
        nx_pix_per_step = np.int(window_size_x*(1 - xy_overlap[0]))
        ny_pix_per_step = np.int(window_size_y*(1 - xy_overlap[1]))
        ys += ny_pix_per_step

    # Return the list of windows
    return window_list

def get_hog_features(img, orient, pix_per_cell, cell_per_block, 
                        vis=False, feature_vec=True):
    # Call with two outputs if vis==True
    if vis == True:
        features, hog_image = hog(img, orientations=orient, 
                                  pixels_per_cell=(pix_per_cell, pix_per_cell),
                                  cells_per_block=(cell_per_block, cell_per_block), 
                                  transform_sqrt=True, 
                                  visualise=vis, feature_vector=feature_vec)
        return features, hog_image
    # Otherwise call with one output
    else:      
        features = hog(img, orientations=orient, 
                       pixels_per_cell=(pix_per_cell, pix_per_cell),
                       cells_per_block=(cell_per_block, cell_per_block), 
                       transform_sqrt=True, 
                       visualise=vis, feature_vector=feature_vec)
        return features

def main():

    zed = zcam.PyZEDCamera()

    # Create a PyInitParameters object and set configuration parameters
    #init_params = zcam.PyInitParameters()
    filepath = sys.argv[1]
    init_params = zcam.PyInitParameters(svo_input_filename=filepath,svo_real_time_mode=False)
    init_params.depth_mode = sl.PyDEPTH_MODE.PyDEPTH_MODE_PERFORMANCE  # Use PERFORMANCE depth mode
    init_params.coordinate_units = sl.PyUNIT.PyUNIT_MILLIMETER  # Use milliliter units (for depth measurements)

    # Open the camera
    err = zed.open(init_params)
    if err != tp.PyERROR_CODE.PySUCCESS:
        exit(1)

    # Create and set PyRuntimeParameters after opening the camera
    runtime_parameters = zcam.PyRuntimeParameters()
    runtime_parameters.sensing_mode = sl.PySENSING_MODE.PySENSING_MODE_STANDARD  # Use STANDARD sensing mode

    # Capture 50 images and depth, then stop
    i = 0
    image = core.PyMat()
    depth = core.PyMat()
    point_cloud = core.PyMat()
    #np.zeros((0, 8460))
    features = []
    images = []


    orient = 9  # HOG orientations
    pix_per_cell = 8 # HOG pixels per cell
    cell_per_block = 2 # HOG cells per block
    hog_channel = 'ALL' # Can be 0, 1, 2, or "ALL"
    spatial_size = (32, 32) # Spatial binning dimensions
    hist_bins = 32    # Number of histogram bins
    spatial_feat = True # Spatial features on or off
    hist_feat = True # Histogram features on or off
    hog_feat = True # HOG features on or off

    while i < 5:

        i = i + 1

        # A new image is available if grab() returns PySUCCESS
        if zed.grab(runtime_parameters) == tp.PyERROR_CODE.PySUCCESS:
            # Retrieve left image
            zed.retrieve_image(image, sl.PyVIEW.PyVIEW_LEFT)
            # Retrieve depth map. Depth is aligned on the left image
            #cv2.imshow("ZED", depth.get_data())
            #key = cv2.waitKey(1)

            zed.retrieve_measure(depth, sl.PyMEASURE.PyMEASURE_DEPTH)
            # Retrieve colored point cloud. Point cloud is aligned on the left image.
            #cv2.imshow("ZED", depth.get_data()*256/20000)
            #key = cv2.waitKey(1)
            windows = slide_window_helper(image.get_data())
            for window in windows:
                roi = image.get_data()[window[1]:window[3], window[0]:window[2], :3]
                roid= depth.get_data()[window[1]:window[3], window[0]:window[2]]
                #print(np.shape(roid))
                roid= cv2.convertScaleAbs(roid).reshape((roid.shape[0], roid.shape[1], 1))
                result = roi #np.dstack((roi, roid))
                images.append(result)
                hog_f = []

                for channel in range(result.shape[2]):

                    hog_f.extend(get_hog_features(result[:, :, channel], orient, pix_per_cell, cell_per_block, vis=False, feature_vec=True))
                features.append(hog_f)


    print(np.shape(features))
    data = np.array(features)
    print (data.shape)
    classifier = hdbscan.HDBSCAN(min_cluster_size=10, prediction_data=True)
    classifier.fit(data)
    print(max(classifier.labels_))
    for i in range(max(classifier.labels_+1)):
        pathlib.Path("./sorted_data/{0}".format(i)).mkdir(parents=True, exist_ok=True)
    pathlib.Path("./sorted_data/-1").mkdir(parents=True, exist_ok=True)
    for c, image, i in zip(classifier.labels_, images, range(len(images))):
        cv2.imwrite("sorted_data/{0}/{1}.jpg".format(c, i), image)

if __name__ == '__main__':
    main()








