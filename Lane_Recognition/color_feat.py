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
from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import train_test_split
import hdbscan
import pathlib
import HOG_lib
import mahotas

def slide_window_helper(img, x_start_stop=[None, None], y_start_stop=[None, None], window_size=[5, 5]):
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


def get_features(image, color_feat = True):

    traindata = []
    colors = []
    test = []
    image = np.asarray(image)
    windows = slide_window_helper(image)

    if color_feat == True:
        for i in range(0, image.shape[0]):
            for j in range(0, image.shape[1]):
                colors = tuple(image[i,j])
                traindata.append(colors)

   # if texture == True:
    #    for i in range(0, image.shape[0]):
     #       for j in range(0, image.shape[1]):

                    #for window in windows:
                    #roi = image[window[1]:window[3], window[0]:window[2], :3]

      #          haralick_features = mahotas.features.haralick(image[i, j]).mean(0)
       
                    #harafeat_list = [item for sublist in haralick_features for item in sublist]
       #         print("The tasks at hand: ", window, j, i)
        #        test.append(haralick_features)

  
    #test = np.asarray(test)
    training_data = np.asarray(traindata)

    return training_data

def load_training(imgs):
    features = []
    for file in imgs:
        img = cv2.imread(file)
        training_feat = get_features(img)
        features.append(training_feat)

    return features



def prepare_images_for_processing(road_folder, nonroad_folder, image_type):
    road = []
    for folder in road_folder:
        road += glob.glob(folder +'/*.' + image_type)
        
    nonroad = []
    for folder in nonroad_folder:
        nonroad += glob.glob(folder +'/*.' + image_type)

    #Get a list of all the features for road and non-road samples
    road_features = load_training(road)
    nonroad_features = load_training(nonroad)

    #Convert to numpy array and slice the first entry away since we do not care about the amount of images.
    road_features = np.array(road_features)[0, :, :]
    nonroad_features = np.array(nonroad_features)[0, :, :]

    X = np.vstack((road_features, nonroad_features)).astype(np.float64)
    y = np.hstack((np.ones(len(road_features)), np.zeros(len(nonroad_features))))

    return X, y


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
    color_feat = True
    i = 0
    image = core.PyMat()
    depth = core.PyMat()
    point_cloud = core.PyMat()
    confidence = core.PyMat()
    #np.zeros((0, 8460))
    features = []
    images = []

    print("own data start \n")

    for j in range(25):
        zed.grab(runtime_parameters)

    
    while i < 1:

        i = i + 1
        # A new image is available if grab() returns PySUCCESS
        if zed.grab(runtime_parameters) == tp.PyERROR_CODE.PySUCCESS:
            # Retrieve left image
            zed.retrieve_image(image, sl.PyVIEW.PyVIEW_LEFT)

            feat_img = image.get_data()[:, : , :3]

            feat_img = cv2.cvtColor(feat_img, cv2.COLOR_BGR2RGB)

            zed.retrieve_measure(point_cloud, sl.PyMEASURE.PyMEASURE_XYZRGBA)

            zed.retrieve_measure(depth, sl.PyMEASURE.PyMEASURE_DEPTH)

            zed.retrieve_measure(confidence, sl.PyMEASURE.PyMEASURE_CONFIDENCE)
            

            feature = get_features(feat_img, color_feat)

            features.append(feature)
            


    data = np.array(features)[0, :, :]
    road_folder = ['C:/Users/marti/PowerShell/zed-python/tutorials/non-vehicles/semisupervised/Road']
    nonroad_folder = ['C:/Users/marti/PowerShell/zed-python/tutorials/non-vehicles/semisupervised/non-road']
    scaled_X, y = prepare_images_for_processing(road_folder, nonroad_folder, "png")
    print(scaled_X, y)
    classifier = LinearSVC()

    #svm.SVC(C=0.2, cache_size=200, class_weight=None, coef0=0.0,
    #decision_function_shape='ovr', degree=3, gamma='auto', kernel='rbf',
    #max_iter=-1, probability=False, random_state=None, shrinking=True,
    #tol=0.001, verbose=False)
    classifier.fit(scaled_X, y)
    classes = classifier.predict(data)
    classes = classes.reshape(720, 1280)

    blank_image = np.zeros((np.shape(feat_img)[0], np.shape(feat_img)[1],3), np.uint8)
    
    classified = np.dstack((blank_image, classes))
    print(np.shape(classified))
    for k in range(0, blank_image.shape[0]):
       for l in range(0, blank_image.shape[1]):

            if classified[k,l,3] == 1:
                blank_image[k, l] = (255, 0, 0)
                #print("i did this", k, l)

            elif classified[k,l,3] == 0:
                blank_image[k, l] = (0, 255, 0)
                #print("i did thissss")

    kernel = np.ones((5,5),np.uint8)
    opening = cv2.morphologyEx(blank_image, cv2.MORPH_OPEN, kernel)        
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    plt.subplot(211)
    plt.imshow(closing)
    plt.subplot(212)
    plt.imshow(feat_img)
    plt.title('Original Image')
    plt.show()



if __name__ == '__main__':
    main()


