import math
import numpy as np
import sys
import cv2
from sklearn.externals import joblib
import RoadRecognition as rr


def main():

    zed, runtime_parameters = rr.ZED_live()  #ZED_live() is for live feed and ZED_SVO() is for loading an SVO from the commandline.
    i = 0
    image = rr.core.PyMat()
    #depth = rr.core.PyMat()
    point_cloud = rr.core.PyMat()
    confidence = rr.core.PyMat()
    classifier = joblib.load("./Road_classifier.pkl") #Load Classifier created before.

    for j in range(60):             #Let the camera start up when using ZED_live
        zed.grab(runtime_parameters)
    #zed.set_svo_position(178) #Jumping to a frame number in the SVO file.
    while i < 50:
        i = i + 1
        # A new image is available if grab() returns PySUCCESS
        if zed.grab(runtime_parameters) == rr.tp.PyERROR_CODE.PySUCCESS:
            zed.grab(runtime_parameters)
            zed.grab(runtime_parameters)
            # Retrieve left image
            zed.retrieve_image(image, rr.sl.PyVIEW.PyVIEW_LEFT)
            zed.retrieve_measure(point_cloud, rr.sl.PyMEASURE.PyMEASURE_XYZRGBA)
            #zed.retrieve_measure(depth, rr.sl.PyMEASURE.PyMEASURE_DEPTH)

            #print(point_cloud.get_data()[240, 140, :], point_cloud.get_data()[1:, 1:, :].shape)

            feat_img = image.get_data()[:, : , :3]
            feat_col = feat_img[:704, :, :3]
            classes = rr.classify(feat_col, point_cloud, classifier)#Classify the pixels in the image


            points = rr.compute_center(classes, feat_col, point_cloud) #Computer center points of the recognized road
            points = np.asarray(points)/1000
            print([points[1], -points[0]]) #Print the center point for the anonymous pipe to read.



if __name__ == '__main__':
    main()
