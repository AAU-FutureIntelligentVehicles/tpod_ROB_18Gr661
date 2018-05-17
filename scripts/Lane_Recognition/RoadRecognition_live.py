import pyzed.camera as zcam
import pyzed.defines as sl
import pyzed.types as tp
import pyzed.core as core
import numpy as np
import sys
import matplotlib.image as mpimg
import cv2
from sklearn.externals import joblib
from sklearn.svm import LinearSVC
from sklearn import svm
from sklearn.preprocessing import StandardScaler
import pathlib
import matplotlib.patches as mpatches
import geometry as g
from sklearn import datasets, linear_model
import RoadRecognition as rr


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


    print("own data start \n")

    #for j in range(3032):
        #zed.grab(runtime_parameters)

    
    zed.set_svo_position(3032)
    
    while i < 1:

        i = i + 1
        # A new image is available if grab() returns PySUCCESS
        if zed.grab(runtime_parameters) == tp.PyERROR_CODE.PySUCCESS:
            # Retrieve left image
            zed.retrieve_image(image, sl.PyVIEW.PyVIEW_LEFT)

            feat_img = image.get_data()[:, : , :3]

            #feat_img = cv2.cvtColor(feat_img, cv2.COLOR_BGR2YCR_CB) #YCR_CB #RGB #HSV

            zed.retrieve_measure(point_cloud, sl.PyMEASURE.PyMEASURE_XYZRGBA)

            zed.retrieve_measure(depth, sl.PyMEASURE.PyMEASURE_DEPTH)

            zed.retrieve_measure(confidence, sl.PyMEASURE.PyMEASURE_CONFIDENCE)
            
            feat_col = feat_img[:704, :, :3]
            
            haralick = rr.compute_haralick(feat_col)

            print(haralick, haralick[..., 2:].shape)


            haralick = haralick.reshape((-1, 5))



            feature = rr.get_features(feat_col, color_feat)
            feature = np.concatenate((feature, haralick), 1)

            depthroad = 1- g.is_road(point_cloud.get_data()[:704, :, :3])

            features.append(feature)

            data = np.array(features)[0, :, :]

            classes = classifier.predict(data)
            classes = classes.reshape(704, 1280)
            classes = np.logical_and(classes, depthroad)


            rr.show(classes, feat_col, feat_img, point_cloud.get_data()[:704, :, :3])



if __name__ == '__main__':
    main()
