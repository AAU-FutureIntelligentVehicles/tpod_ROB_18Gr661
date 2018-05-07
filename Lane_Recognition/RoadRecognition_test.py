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
import multiprocessing as mp


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

def _ch(roi): #compute harelick mapped function
    return mahotas.features.haralick(roi).mean(0)[:5]

def compute_haralick(crop_img):

    haralick_features = []
    crop_img = np.array(crop_img)
    windows = slide_window_helper(crop_img)
    t = time.process_time()

    rois = []
    pool = mp.Pool(mp.cpu_count())
    print ("        start pools:  {}".format(time.process_time()-t))
    #Extract features from the localized areas of the image. These 32x32 blocks can be resized in slide_window_helper().
    for window in windows:
        #t2 = time.process_time()
        #print ("window time        {0}".format(t2 - t))
        #t = t2
        roi = crop_img[window[1]:window[3], window[0]:window[2], :3]
        rois.append(roi)
        #haralick_feat = mahotas.features.haralick(roi).mean(0)
        
        #haralick_features.append(haralick_feat[:5])
    print ("        create windows:  {}".format(time.process_time()-t))

    haralick_features = pool.map(_ch, rois, 10)
    pool.close()
    pool.join()
    haralick_arr = np.array(haralick_features)
    dims = crop_img.shape
    total = np.zeros((0, dims[1], 5))
    print ("        extract haralick:  {}".format(time.process_time()-t))

    #Create a matrix with the haralick features, which can be stacked with the other features.
    window_count = dims[0]//32
    array = haralick_arr.reshape((window_count, -1, 5)).repeat(32, axis = 0).repeat(32, axis = 1)
    print(array.shape)
    #for i in range(dims[0]// 32):
    #    partial = np.zeros((32, 0, 5))
    #    for j in range(dims[1]//32):
    #        feat = np.ones((32, 32, 5))
    #        feat = feat*haralick_features[dims[1]//32*i+j]
    #        partial = np.concatenate((partial, feat), 1)
    #    total = np.concatenate((total, partial), 0)
    print ("        reconstruct image:  {}".format(time.process_time()-t))

    return array #total

def get_features(image, color_feat = True):

    traindata = []
    image = np.asarray(image)
    windows = slide_window_helper(image)

    if color_feat == True:
        for i in range(0, image.shape[0]):
            for j in range(0, image.shape[1]):
                colors = tuple(image[i,j])
                traindata.append(colors)

    training_data = np.array(traindata)


    return training_data




def show(classes, feat_col, feat_img):
    blank_image = np.zeros((np.shape(feat_col)[0], np.shape(feat_col)[1],3), np.uint8)
    
    classified = np.dstack((blank_image, classes))

    for k in range(0, blank_image.shape[0]):
       for l in range(0, blank_image.shape[1]):

            if classified[k,l,3] == 1:
                blank_image[k, l] = (255, 255, 255)


            elif classified[k,l,3] == 0:
                blank_image[k, l] = (0, 0, 0)

    feat_img = cv2.cvtColor(feat_img, cv2.COLOR_BGR2RGB)
    kernel = np.ones((9,9),np.uint8) #(15,15)
    median = cv2.medianBlur(blank_image, 15)#(31, 31)
    opening = cv2.morphologyEx(median, cv2.MORPH_OPEN, kernel)        
    closing1 = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    closing = cv2.cvtColor(closing1, cv2.COLOR_BGR2GRAY)

    ret, closing = cv2.threshold(closing, 1, 255, cv2.THRESH_BINARY)


    im2, contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:
        
        cont_img = np.array(feat_col)

        cv2.drawContours(cont_img, contours, -1, (0,0,255), 3, 6)

        c = max(contours, key = cv2.contourArea)

        x,y,w,h = cv2.boundingRect(c)
    
        cv2.rectangle(cont_img,(x,y),(x+w,y+h),(0,255,0),2)

        #print(x, y, w, h)

        cropped = cont_img[y:y+h, x:x+w]
        cropped1 = closing[y:y+h, x:x+w]


    #Perspective transform
    #Perspective matricies both regular and inverse
    
    Pts =  np.float32([[0, 0], [0, h], [w, h], [w, 0]])
    Pts_inv = np.float32([[0, 0], [w-(w/1.5), h], [w-(w/2), h], [w, 0]]) #np.float32([[500, dims[0]], [700, dims[0]], [0, 0], [dims[1], 0]]) (w/1.5) (w/3)

    M =cv2.getPerspectiveTransform(Pts, Pts_inv)
    Minv = cv2.getPerspectiveTransform(Pts, Pts_inv)
    #print(contours[0])
    #print(np.array(contours).shape)

    warped_img = cv2.warpPerspective(cropped1, M, (w, h))


    plt.subplot(131)
    plt.imshow(closing1)
    red_patch = mpatches.Patch(color='white', label='road')
    green_patch = mpatches.Patch(color='black', label='non-road')
    plt.legend(handles=[red_patch, green_patch])
    plt.title('Road Extraction')
    plt.subplot(132)
    plt.imshow(cont_img)
    plt.title('Original Image')
    plt.subplot(133)
    plt.imshow(warped_img)
    plt.title('Perspective Transformation')
    plt.show()



def main():

    print("start of main: {0}".format(time.process_time()))
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

    print("Zed set up: {0}".format(time.process_time()))
    color_feat = True
    i = 0
    image = core.PyMat()
    depth = core.PyMat()
    point_cloud = core.PyMat()
    confidence = core.PyMat()
    features = []
    images = []
    depthroad = []
    classifier = joblib.load("Road_classifier.pkl")

    print("classifier loaded: {0}".format(time.process_time()))
    #print("own data start \n")

    for j in range(1):
        zed.grab(runtime_parameters)

    print("frames skipped: {0}".format(time.process_time()))

    while i < 10:
        looptime = time.process_time()
        print("start of loop{0}".format(looptime))
        i = i + 1
        # A new image is available if grab() returns PySUCCESS
        if zed.grab(runtime_parameters) == tp.PyERROR_CODE.PySUCCESS:
            # Retrieve left image
            zed.retrieve_image(image, sl.PyVIEW.PyVIEW_LEFT)
            print("    image retrieved: {0}".format(time.process_time()-looptime))
            feat_img = image.get_data()[:, : , :3]

            #feat_img = cv2.cvtColor(feat_img, cv2.COLOR_BGR2YCR_CB) #YCR_CB #RGB #HSV

            zed.retrieve_measure(point_cloud, sl.PyMEASURE.PyMEASURE_XYZRGBA)

            zed.retrieve_measure(depth, sl.PyMEASURE.PyMEASURE_DEPTH)

            zed.retrieve_measure(confidence, sl.PyMEASURE.PyMEASURE_CONFIDENCE)
            
            print("    depth computed: {0}".format(time.process_time()-looptime))


            feat_col = feat_img[:704, :, :3]
            
            haralick = compute_haralick(feat_col)
            haralick = haralick.reshape((-1, 5))

            feature = get_features(feat_col, color_feat)
            feature = np.concatenate((feature, haralick), 1)

            print("    harelick and features extracted: {0}".format(time.process_time()-looptime))

            depthroad = 1- g.is_road(point_cloud.get_data()[:704, :, :3])

            print("    depth classified: {0}".format(time.process_time()-looptime))

            features.append(feature)

            data = np.array(features)[0, :, :]

            classes = classifier.predict(data)
            classes = classes.reshape(704, 1280)
            classes = np.logical_and(classes, depthroad)
            print("    classified: {0}".format(time.process_time()-looptime))

            show(classes, feat_col, feat_img)
            print("    end of loop: {0}".format(time.process_time()-looptime))



if __name__ == '__main__':
    main()
