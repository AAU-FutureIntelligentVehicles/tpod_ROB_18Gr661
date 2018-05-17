from sklearn.svm import LinearSVC
import numpy as np
import matplotlib.pyplot as plt
import glob
import cv2
from mpl_toolkits.mplot3d import Axes3D


def get_features(image, color_feat = True):

    traindata = []
    image = np.asarray(image)
    return image.reshape((-1, image.shape[2]))



def load_training(imgs):
    features = []
    for file in imgs:
        img = cv2.imread(file)
        training_feat = get_features(img)
        features.append(training_feat)
    return features    



a = np.asarray((0,0))
b = np.asarray((0,0.1))
data = np.stack((a,b))
data = np.concatenate((data, data+[100,0.5], data+[200,1]))
X = data
print(data)
classes = [0,1,0, 1,0, 1]

road_folder = ['C:\\Users\\marti\\PowerShell\\zed-python\\tutorials\\tpod_ROB_18Gr661\\Lane_Recognition\\Testset\\road']
nonroad_folder = ['C:\\Users\\marti\\PowerShell\\zed-python\\tutorials\\tpod_ROB_18Gr661\\Lane_Recognition\\Testset\\nonroad']

road = []
for folder in road_folder:
        road += glob.glob(folder +'/*.' + 'png')
        
nonroad = []
for folder in nonroad_folder:
        nonroad += glob.glob(folder +'/*.' + 'png')

road_features = load_training(road)
nonroad_features = load_training(nonroad)

road_features = np.array(road_features)[0, :, :]
nonroad_features = np.array(nonroad_features)[0, :, :]

x = np.vstack((road_features, nonroad_features)).astype(np.float64)
y = np.hstack((np.ones(len(road_features)), np.zeros(len(nonroad_features))))

print(x, y)

classifier = LinearSVC(max_iter = 100000, random_state = np.random.RandomState())
classification = classifier.fit(x, y)


print(classification.__dict__)

w = classification.coef_[0]
print(w)

a = -w[0] / w[1]

xx = np.linspace(0,220)
yy = a * xx  - classification.intercept_[0] / w[1]

#h0 = plt.plot(xx, yy, 'k-', label="non weighted div")

#plt.scatter(X[:, 0], X[:, 1], c = classes)
#plt.legend()


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

print(x)
ax.scatter(x[..., 0],x[..., 1],x[..., 2], c=y)

plt.show()