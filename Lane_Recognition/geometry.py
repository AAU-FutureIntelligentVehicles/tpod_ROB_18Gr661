import numpy as np
from matplotlib import pyplot as plt

def rot(r, p, y):
	
	Rx = np.array([[1, 0, 0], [0, np.cos(r), -np.sin(r)], [0, np.sin(r), np.cos(r)]])
	Ry = np.array([[np.cos(p), 0, -np.sin(p)], [0, 1, 0], [np.sin(p), 0, np.cos(p)]])
	Rz = np.array([[np.cos(y), -np.sin(y), 0], [np.sin(y), np.cos(y), 0], [0, 0, 1]])
	a = np.eye(6)
	return np.dot(Rx, np.dot(Ry, Rz)) 
	a[3:, 3:] = b
	return a




def load_data(filename):
	return np.load("training/{0}.npy".format(filename)).reshape((720, -1, 6))

def display_depth(mat, scaling):
	plt.imshow(mat[..., (0, 1, 4)]/[256 ,256, scaling])
	plt.show()

def is_road(img, rot_=(0.3, 0, 0), thresh = 1700):
	rot_mat = rot(rot_[0], rot_[1], rot_[2]) 
	rot_img = np.nan_to_num(img).dot(rot_mat)
	road = (rot_img[..., 1] < thresh)*1
	return road
	
	
def pcl_lookup (contour, point_cloud, rot_ =(0.3, 0, 0)):
	rot_mat = rot(rot_[0], rot_[1], rot_[2]) 
	rot_pc= np.nan_to_num(point_cloud).dot(rot_mat)
	new_contours = []
	for point in contour:
		#print(point[0,1])
		a=np.asarray((rot_pc[point[0,1],point[0,0], 0]+20000, rot_pc[point[0,1],point[0,0], 2]))
		a = a/50
		a = a.round()
		if a[1] == 0:
			continue
		new_contours.append([a]) #20000 is added such that the values in the list are positive #new_contours.append([[rot_pc[point[0,0],point[0,1], 0], rot_pc[point[0,0],point[0,1], 2]]]) 
	return np.asarray(new_contours)