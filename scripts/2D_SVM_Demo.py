"""
=========================================
SVM: Maximum margin separating hyperplane
=========================================

Plot the maximum margin separating hyperplane within a two-class
separable dataset using a Support Vector Machine classifier with
linear kernel.
"""
print(__doc__)

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.datasets import make_blobs

# we create 40 separable points
X, y = make_blobs(n_samples=40, centers=2, random_state=6)

# fit the model, don't regularize for illustration purposes
#clf = svm.SVC(kernel='linear', C=1000)
clf = svm.LinearSVC()       #black
clf2 = svm.LinearSVC()      #blue
#clf3 = svm.LinearSVC(intercept_scaling = 100)
#clf4 = svm.LinearSVC()
clf5 = svm.LinearSVC()      #green


clf.fit(X, y)
clf2.fit(X, y)
#clf3.fit(X, y)
#clf4.fit(X, y)
clf5.fit(X, y)
print(clf.intercept_, 'black')
clf5.intercept_ = clf.intercept_*-8  #green
print(clf5.intercept_, 'green')
clf2.intercept_ = clf.intercept_*10      #blue
print(clf2.intercept_, 'blue')
#clf3.intercept_ = 0

plt.scatter(X[:, 0], X[:, 1], c=y, s=30, cmap=plt.cm.Paired)

# plot the decision function
plt.ylim(-12,0)
plt.xlim(0,12)
#plt.plot(0,clf.intercept_,'ro')        #plot intercept with y axis
ax2 = plt.gca()
ax = plt.gca()
xlim = ax.get_xlim()
ylim = ax.get_ylim()

# create grid to evaluate model
xx = np.linspace(xlim[0], xlim[1], 30)
yy = np.linspace(ylim[0], ylim[1], 30)
YY, XX = np.meshgrid(yy, xx)
xy = np.vstack([XX.ravel(), YY.ravel()]).T
Z = clf.decision_function(xy).reshape(XX.shape)
Z2 = clf2.decision_function(xy).reshape(XX.shape)
Z3 = clf3.decision_function(xy).reshape(XX.shape)
#Z4 = clf4.decision_function(xy).reshape(XX.shape)
Z5 = clf5.decision_function(xy).reshape(XX.shape)

# plot decision boundary and margins
ax.contour(XX, YY, Z, colors='k', levels=[0], alpha=0.5,linestyles=['-'])        #1
ax.contour(XX, YY, Z2, colors= 'b', levels=[0], alpha=0.5, linestyles=['-'])     #0.1
#ax.contour(XX, YY, Z3, colors= 'y', levels=[-1, 0, 1], alpha=0.5, linestyles=['--', '-', '--'])     #0.75
#ax.contour(XX, YY, Z4, colors= 'b', levels=[-1, 0, 1], alpha=0.5, linestyles=['--', '-', '--'])     #10
ax.contour(XX, YY, Z5, colors= 'g', levels=[0], alpha=0.5, linestyles=['-'])     #100
# plot support vectors
#ax.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1], s=100,linewidth=1, facecolors='none')

#axes.set_xlim([0,10])
#axes.set_ylim([0,10])
#plt.ylim(0,10)
#plt.xlim(0,10)
#plt.axis([0, 10, 0, 10])

plt.show()
