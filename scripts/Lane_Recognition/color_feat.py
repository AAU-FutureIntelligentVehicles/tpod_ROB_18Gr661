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
from sklearn.externals import joblib
from sklearn.svm import LinearSVC
from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import train_test_split
import hdbscan
import pathlib
import HOG_lib
import mahotas
import matplotlib.patches as mpatches
import geometry as g


windowSize = 32


def slide_window_helper_old(img, x_start_stop=[None, None], y_start_stop=[None, None], window_size=[32, 32]):
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


def slide_window_helper(img, x_start_stop=[None, None], y_start_stop=[None, None], window_size=[32, 32]):
    window_size_x = window_size[0]
    window_size_y = window_size[1]
    x_windows = img.shape[0]// window_size_x
    y_windows = img.shape[1]// window_size_y

    window_list = []
    for j in range(x_windows):
        for i in range(y_windows):
            window = [i*window_size_x, j*window_size_y, (i+1)*window_size_x, (j+1)*window_size_y]
            window_list.append(window)

    return window_list



def compute_haralick(crop_img):

    crop_img = np.array(crop_img)
    windows = slide_window_helper(crop_img)
    rois = []

    #Extract features from the localized areas of the image. These 32x32 blocks can be resized in slide_window_helper().
    for window in windows:
        roi = crop_img[window[1]:window[3], window[0]:window[2], :3]

        roi = mahotas.features.haralick(roi).mean(0)[:5]
        rois.append(roi)
        #haralick_feat = mahotas.features.haralick(roi).mean(0)
        
        #haralick_features.append(haralick_feat[:5])
    haralick_features = rois
    haralick_arr = np.array(haralick_features)
    dims = crop_img.shape
    scaling_factor = [0.05423693486427112, 2258.078377174232,0.986424403324001,9114.763475900238,0.42569913950248545]
    #haralick_arr = haralick_arr / scaling_factor



    window_count = dims[0]//windowSize
    array = haralick_arr.reshape((window_count, -1, 5)).repeat(windowSize, axis = 0).repeat(windowSize, axis = 1)


    return array

def get_features(image, color_feat = True):

    traindata = []
    #traindata_dp = []
    #colors = []
    #dpimg = np.asarray(dpimg)
    image = np.asarray(image)
    windows = slide_window_helper(image)

    if color_feat == True:
        for i in range(0, image.shape[0]):
            for j in range(0, image.shape[1]):
                colors = tuple(image[i,j])
                traindata.append(colors)

    training_data = np.array(traindata)


    return training_data

def load_training(imgs):
    features = []
    for file in imgs:
        img = cv2.imread(file)
        #img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) #YCR_CB #BGR #HSV
        training_feat = get_features(img)
        hara = compute_haralick(img)
        hara = hara.reshape((-1, 5))
        print(hara.shape, training_feat.shape)
        training_feat = np.concatenate((training_feat, hara), 1)
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


def generate_classifier():
    road_folder = ['C:/Users/marti/PowerShell/zed-python/tutorials/non-vehicles/semisupervised/Road']
    nonroad_folder = ['C:/Users/marti/PowerShell/zed-python/tutorials/non-vehicles/semisupervised/non-road']
    scaled_X, y = prepare_images_for_processing(road_folder, nonroad_folder, "png")
    #print(scaled_X, y)
    classifier = LinearSVC()
    return classifier, scaled_X, y


def show(classes, feat_col, feat_img):
    blank_image = np.zeros((np.shape(feat_col)[0], np.shape(feat_col)[1],3), np.uint8)
    
    classified = np.dstack((blank_image, classes))
    #print(np.shape(classified))
    for k in range(0, blank_image.shape[0]):
       for l in range(0, blank_image.shape[1]):

            if classified[k,l,3] == 1:
                blank_image[k, l] = (255, 255, 255)
                #print("i did this", k, l)

            elif classified[k,l,3] == 0:
                blank_image[k, l] = (0, 0, 0)
                #print("i did thissss")
    feat_img = cv2.cvtColor(feat_img, cv2.COLOR_BGR2RGB)
    kernel = np.ones((9,9),np.uint8)
    median = cv2.medianBlur(blank_image, 15)
    opening = cv2.morphologyEx(median, cv2.MORPH_OPEN, kernel)        
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    plt.subplot(211)
    plt.imshow(closing)
    red_patch = mpatches.Patch(color='white', label='road')
    green_patch = mpatches.Patch(color='black', label='non-road')
    plt.legend(handles=[red_patch, green_patch])
    plt.subplot(212)
    plt.imshow(feat_img)
    plt.title('Original Image')
    plt.show()



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
    depthroad = []

    classifier, scaled_X, y = generate_classifier()

    print("own data start \n")

    for j in range(2500):
        zed.grab(runtime_parameters)

    
    while i < 1:

        i = i + 1
        # A new image is available if grab() returns PySUCCESS
        if zed.grab(runtime_parameters) == tp.PyERROR_CODE.PySUCCESS:
            # Retrieve left image
            zed.retrieve_image(image, sl.PyVIEW.PyVIEW_LEFT)

            feat_img = image.get_data()[:, : , :3]

            #feat_img = cv2.cvtColor(feat_img, cv2.COLOR_BGR2RGB)

            #feat_img = cv2.cvtColor(feat_img, cv2.COLOR_BGR2YCR_CB) #YCR_CB #RGB #HSV

            zed.retrieve_measure(point_cloud, sl.PyMEASURE.PyMEASURE_XYZRGBA)

            zed.retrieve_measure(depth, sl.PyMEASURE.PyMEASURE_DEPTH)

            zed.retrieve_measure(confidence, sl.PyMEASURE.PyMEASURE_CONFIDENCE)
            
            feat_col = feat_img[:704, :, :3]
            

            haralick = compute_haralick(feat_col)
            haralick = haralick.reshape((-1, 5))
            print(haralick.shape, feat_img.shape)




            feature = get_features(feat_col, color_feat)
            print(feature.shape)
            feature = np.concatenate((feature, haralick), 1)

            depthroad = 1- g.is_road(point_cloud.get_data()[:704, :, :3])
            plt.imshow (depthroad)
            plt.show()

            features.append(feature)
                    
            #print(np.array(features))

            data = np.array(features)[0, :, :]

            print(data.shape)


            #svm.SVC(C=0.2, cache_size=200, class_weight=None, coef0=0.0,
            #decision_function_shape='ovr', degree=3, gamma='auto', kernel='rbf',
            #max_iter=-1, probability=False, random_state=None, shrinking=True,
            #tol=0.001, verbose=False)
            classification = classifier.fit(scaled_X, y)

            joblib.dump(classification, "Road_classifier.pkl", compress=3)

            classes = classifier.predict(data)
            classes = classes.reshape(704, 1280)

            classes = np.logical_and(classes, depthroad)

            show(classes, feat_col, feat_img)



if __name__ == '__main__':
    main()
