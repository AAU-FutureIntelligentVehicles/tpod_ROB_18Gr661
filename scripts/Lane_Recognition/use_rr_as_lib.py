import math
import numpy as np
import sys
import cv2
from sklearn.externals import joblib
import RoadRecognition as rr
import time

def main():

    zed, runtime_parameters = rr.ZED_SVO()
    i = 0
    image = rr.core.PyMat()
    depth = rr.core.PyMat()
    point_cloud = rr.core.PyMat()
    confidence = rr.core.PyMat()
    classifier = joblib.load("Road_classifier.pkl")


    print("own data start \n")


    zed.set_svo_position(2500)

    while i < 1:
        t1 = time.time()

        i = i + 1
        # A new image is available if grab() returns PySUCCESS
        if zed.grab(runtime_parameters) == rr.tp.PyERROR_CODE.PySUCCESS:
            # Retrieve left image
            zed.retrieve_image(image, rr.sl.PyVIEW.PyVIEW_LEFT)
            zed.retrieve_measure(point_cloud, rr.sl.PyMEASURE.PyMEASURE_XYZRGBA)
            zed.retrieve_measure(depth, rr.sl.PyMEASURE.PyMEASURE_DEPTH)

            #print(point_cloud.get_data()[240, 140, :], point_cloud.get_data()[1:, 1:, :].shape)

            feat_img = image.get_data()[:, : , :3]
            feat_col = feat_img[:704, :, :3]
            #print(classifier.intercept_scaling)
            classifier.intercept_ = classifier.intercept_ * -70 #This is the intercept value that has to be changed.
            classes = rr.classify(feat_col, point_cloud, classifier)
            points = rr.compute_center(classes, feat_col, point_cloud)
            points = np.asarray(points)/1000
            print([points[1], -points[0]])
            t2 = time.time()
            print(t2-t1)



if __name__ == '__main__':
    main()
