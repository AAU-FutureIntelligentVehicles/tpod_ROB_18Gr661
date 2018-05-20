import pyzed.camera as zcam
import pyzed.defines as sl
import pyzed.types as tp
import pyzed.core as core
import math
import numpy as np
import sys
import matplotlib.image as mpimg
import cv2
#import matplotlib.pyplot as plt
import glob
from sklearn.externals import joblib
from sklearn.svm import LinearSVC
from sklearn import svm
from sklearn.preprocessing import StandardScaler
import pathlib
import mahotas
import matplotlib.patches as mpatches
import geometry as g
import multiprocessing as mp
from sklearn import datasets, linear_model


windowSize = 64


def slide_window_helper(img, x_start_stop=[None, None], y_start_stop=[None, None], window_size=[64, 64]):
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

def _ch(roi): #compute haralick mapped function
    return mahotas.features.haralick(roi).mean(0)[:5]

def compute_haralick(crop_img):
    crop_img = np.array(crop_img)
    windows = slide_window_helper(crop_img)
    rois = []
    pool = mp.Pool(mp.cpu_count())

    #Extract features from the localized areas of the image. These 32x32 blocks can be resized in slide_window_helper().
    for window in windows:
        roi = crop_img[window[1]:window[3], window[0]:window[2], :3]
        rois.append(roi)
        #haralick_feat = mahotas.features.haralick(roi).mean(0)
        
        #haralick_features.append(haralick_feat[:5])
    haralick_features = pool.map(_ch, rois)
    pool.close()
    pool.join()
    haralick_arr = np.array(haralick_features)
    dims = crop_img.shape
    scaling_factor = [0.05423693486427112, 2258.078377174232,0.986424403324001,9114.763475900238,0.42569913950248545]
    #feature_weights = [0.5, 1.5, 1, 2, 1]
    #haralick_arr = haralick_arr*feature_weights

    haralick_arr = haralick_arr / scaling_factor

    window_count = dims[0]//windowSize
    array = haralick_arr.reshape((window_count, -1, 5)).repeat(windowSize, axis = 0).repeat(windowSize, axis = 1)

    return array.astype(np.float32)

def get_features(image, color_feat = True):

    traindata = []
    image = np.asarray(image)
    return image.reshape((-1, image.shape[2]))
    windows = slide_window_helper(image)

    if color_feat == True:
        for i in range(0, image.shape[0]):
            for j in range(0, image.shape[1]):
                colors = tuple(image[i,j])
                traindata.append(colors)

    training_data = np.array(traindata)


    return training_data

def compute_center(classes, feat_col, point_cloud):



    point_cloud_ = g.rotate_pc(point_cloud)
    kernel = np.ones((9,9),np.uint8) #(15,15)
    classes = classes.astype(np.uint8)
    median = cv2.medianBlur(classes, 15)#(31, 31)
    opening = cv2.morphologyEx(median, cv2.MORPH_OPEN, kernel)        
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    im2, contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cont_img = np.array(feat_col)


    if len(contours) != 0:
        
        

        c = max(contours, key = cv2.contourArea)

        blank_img = np.zeros((np.shape(feat_col)[0], np.shape(feat_col)[1],3), np.uint8)


        cont = g.pcl_lookup(c, point_cloud_)
        #print (c.dtype)
        cont = np.int32(cont)
        road_geometry = np.zeros((400, 800, 3), dtype = 'uint8')

        cv2.drawContours(road_geometry, [cont], -1, (255,255,255), -1)

        scaling_factor = 50 #convert back to milimetres
        centering_factor = 20000 #recenter the points
        lower_limit_road = 1600
        upper_limit_road = 2000

        #for i in range(10):
        a = np.zeros((400, 800))
        a[lower_limit_road//scaling_factor:upper_limit_road//scaling_factor, ...]=1 #define the region we are looking for the center points of
        b=np.logical_and(road_geometry[..., 0], a).astype('uint8') #mask the image to the region we are looking at
        #print(road_geometry[0:40,:,0], road_geometry[0:40,:,0].dtype)
        #cv2.rectangle(road_geometry,(0, 40*i),(800, 40),(0,255,0),1)

        #find contours of the part of the image we want to find the handle in 
        road_cont = cv2.findContours(road_geometry[lower_limit_road//scaling_factor:upper_limit_road//scaling_factor,:,0].copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #compute the moments of the  contour
        M = cv2.moments(road_cont[0])

        #find the center point of the contour
        if M["m00"] > 1:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            center_point = [cX, cY]
            center_point[0] = center_point [0]*scaling_factor  - centering_factor
            center_point[1] = center_point [1]*scaling_factor  + lower_limit_road 
            return center_point
    return [0,0]

def ori_lookup(pointcloud, point):
    pointcloud_ = pointcloud - (point[0] , 0, point[1])
    pointcloud_ = pointcloud_ * pointcloud_
    pointcloud_ = pointcloud_[..., 0] + pointcloud_[..., 2]
    pointcloud_ = np.sqrt(pointcloud_)
    return np.unravel_index( np.nanargmin(pointcloud_, axis=None), pointcloud_.shape)


def show(classes, feat_col, point_cloud):


    point_cloud_ = g.rotate_pc(point_cloud)

    blank_image = np.zeros((np.shape(feat_col)[0], np.shape(feat_col)[1],3), np.uint8)
    
    classified = np.dstack((blank_image, classes))
    
    for k in range(0, blank_image.shape[0]):
       for l in range(0, blank_image.shape[1]):
    
            if classified[k,l,3] == 1:
                blank_image[k, l] = (255, 255, 255)
    
            elif classified[k,l,3] == 0:
                blank_image[k, l] = (0, 0, 0)

    feat_img = cv2.cvtColor(blank_image, cv2.COLOR_BGR2RGB)
    kernel = np.ones((9,9),np.uint8) #(15,15)
    classes = classes.astype(np.uint8)
    median = cv2.medianBlur(classes, 15)#(31, 31)
    opening = cv2.morphologyEx(median, cv2.MORPH_OPEN, kernel)        
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    im2, contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cont_img = np.array(feat_col)


    if len(contours) != 0:

        c = max(contours, key = cv2.contourArea)

        blank_img = np.zeros((np.shape(feat_col)[0], np.shape(feat_col)[1],3), np.uint8)

        cv2.drawContours(blank_image, [c], -1, (0,0,255), 10)


        median1 = cv2.medianBlur(blank_image, 15)#(31, 31)
        opening1 = cv2.morphologyEx(median1, cv2.MORPH_OPEN, kernel)        
        closing1 = cv2.morphologyEx(opening1, cv2.MORPH_CLOSE, kernel)

        cont = g.pcl_lookup(c, point_cloud_)

        cont = np.int32(cont)
        road_geometry = np.zeros((400, 800, 3), dtype = 'uint8')

        cv2.drawContours(road_geometry, [cont], -1, (255,255,255), -1)

        center_points = []
        center_points_mm = []
        scaling_factor = 50 #convert back to milimetres
        centering_factor = 20000 #recenter the points
        lower_limit_road = 1600
        upper_limit_road = 2000

        for i in range(10):
            a = np.zeros((400, 800))
            a[i*40:i*40+40, ...]=1
            b=np.logical_and(road_geometry[..., 0], a).astype('uint8')
            #cv2.rectangle(road_geometry,(0, 40*i),(800, 40),(0,255,0),1)

            road_cont = cv2.findContours(road_geometry[i*40:i*40+40,:,0].copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            M = cv2.moments(road_cont[0])
            if M["m00"] > 1:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                center_point = [cX, cY]
                center_points.append((cX, cY + i*40))
                center_point[0] = center_point [0]*scaling_factor  - centering_factor
                center_point[1] = center_point [1]*scaling_factor  + i*40*scaling_factor
                center_points_mm.append(tuple(center_point))
        print (center_points, center_points_mm)

        ori_centers = []
        for points in center_points:
            cv2.circle(road_geometry, points, 5, (255, 0, 0), -1)
            ori_center = ori_lookup(point_cloud_, points)
            print(ori_center)
            cv2.circle(cont_img, ori_center, 5, (255, 0, 0), -1)           
            ori_centers.append(ori_center)
            


        svr_points = np.asarray(center_points)
        polyapprox = np.polyfit(svr_points[:, 1], svr_points[:, 0], 2)


        
        approximation = np.asarray((svr_points[:,1]*svr_points[:,1]*polyapprox[0]+ svr_points[:,1]*polyapprox[1]+polyapprox[2], svr_points[:,1]), dtype='uint16').transpose()
        #print (approximation)
        for points in zip(approximation[1:, :], approximation[:-1, :]):
            #print(points)
            cv2.line(road_geometry, (points[0][0], points[0][1]), (points[1][0], points[1][1]), (0, 255, 0), 3)


        #cv2.line(road_geometry, (400, 0), (400, 170), (255, 0 , 125), 3)

        #cv2.line(road_geometry, (400, 0), (svr_points[4][0], svr_points[4][1]), (0, 0, 255), 3)
        '''
        im3, contours1, hierarchy = cv2.findContours(road_geometry, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        M = cv2.moments(contours1[0])
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        '''

        #  cv2.circle(cont_img, (cX, cY+600), 7, (255, 0, 0), -1)

        plt.title('Road Contour')
        plt.imshow(closing1)
        plt.show()
        plt.subplot(233)
        plt.imshow(feat_col)
        plt.title('Perspective Transformation')

        plt.subplot(234)
        plt.imshow(road_geometry,origin='lower')
        plt.title('Point Cloud Geometry')
        plt.subplot(235)
        plt.axis('equal')
        plt.scatter(svr_points[:,0], svr_points[:, 1], color='darkorange', label='data')   
        plt.plot(svr_points[:,1]*svr_points[:,1]*polyapprox[0]+ svr_points[:,1]*polyapprox[1]+polyapprox[2], svr_points[:,1], color='navy', lw=2, label='RBF model')
        plt.title("Road Model")


    cont_img = cv2.cvtColor(cont_img, cv2.COLOR_BGR2RGB)
    plt.subplot(232)
    plt.imshow(cont_img)
    plt.title('Original Image')
    plt.subplot(231)
    plt.imshow(closing, cmap='gray')
    red_patch = mpatches.Patch(color='white', label='road')
    green_patch = mpatches.Patch(color='black', label='non-road')
    plt.legend(handles=[red_patch, green_patch])
    plt.title('Road Extraction')
    plt.show()


def classify(image, point_cloud, classifier):

    point_cloud_ = g.rotate_pc(point_cloud)
    #print (point_cloud_.shape)
    haralick = compute_haralick(image)


    haralick = haralick.reshape((-1, 5))


    feature = get_features(image, True)
    feature = np.concatenate((feature, haralick), 1)

    depthroad = 1- g.is_road(point_cloud_)

    classes = classifier.predict(feature)
    classes = classes.reshape(704, 1280)
    classes = np.logical_and(classes, depthroad)
    return classes

def ZED_live():

    zed = zcam.PyZEDCamera()

    # Create a PyInitParameters object and set configuration parameters
    init_params = zcam.PyInitParameters()
    init_params.camera_resolution = sl.PyRESOLUTION.PyRESOLUTION_HD720
    init_params.depth_mode = sl.PyDEPTH_MODE.PyDEPTH_MODE_PERFORMANCE   # Use HD720 video mode (default fps: 60)
    # Use a right-handed Y-up coordinate system
    #init_params.coordinate_system = sl.PyCOORDINATE_SYSTEM.PyCOORDINATE_SYSTEM_RIGHT_HANDED_Y_UP
    init_params.coordinate_units = sl.PyUNIT.PyUNIT_MILLIMETER  # Set units in meters
    err = zed.open(init_params)
    if err != tp.PyERROR_CODE.PySUCCESS:
        exit(1)
    return zed, zcam.PyRuntimeParameters()



def ZED_SVO():
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
    return zed, runtime_parameters



def main():

    zed, runtime_parameters = ZED_SVO()
    color_feat = True
    i = 0
    image = core.PyMat()
    depth = core.PyMat()
    point_cloud = core.PyMat()
    confidence = core.PyMat()
    classifier = joblib.load("Road_classifier.pkl")


    print("own data start \n")

    #for j in range(3032):
        #zed.grab(runtime_parameters)


    #zed.set_svo_position(3032)

    while i < 1:

        i = i + 1
        # A new image is available if grab() returns PySUCCESS
        if zed.grab(runtime_parameters) == tp.PyERROR_CODE.PySUCCESS:
            # Retrieve left image
            zed.retrieve_image(image, sl.PyVIEW.PyVIEW_LEFT)
            zed.retrieve_measure(point_cloud, sl.PyMEASURE.PyMEASURE_XYZRGBA)
            zed.retrieve_measure(depth, sl.PyMEASURE.PyMEASURE_DEPTH)

            #print(point_cloud.get_data()[240, 140, :], point_cloud.get_data()[1:, 1:, :].shape)

            feat_img = image.get_data()[:, : , :3]
            feat_col = feat_img[:704, :, :3]
            classes = classify(feat_col, point_cloud, classifier)

            #show(classes, feat_col, point_cloud.get_data()[:704, :, :3])


 
if __name__ == '__main__':
    main()
