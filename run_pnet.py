import numpy as np
from sklearn.datasets import fetch_openml
from trees import PUExtraTrees
import matplotlib.pyplot as plt

X, y = fetch_openml('mnist_784', return_X_y = True, as_frame = False)
y = y.astype(np.int8)
y[y != 0] = -1 # 1 -> 9 forms N class
y[y == 0] = 1 # 0 forms P class

pi = (y == 1).mean()
X_train, y_train, X_test, y_test = X[:60000], y[:60000], X[60000:], y[60000:]

g = PUExtraTrees(n_estimators = 10, 
                 estimator = 'PN',
                 criterion = 'gini',
                 max_depth = None, 
                 min_samples_leaf = 1, 
                 max_features = 'auto', 
                 max_candidates = 1, 
                 n_jobs = 10)

g.fit(P = X_train[y_train == 1], N = X_train[y_train == -1], pi = pi)
predictions = g.predict(X_test)

TP = (predictions[y_test == 1] == 1).sum()
TN = (predictions[y_test == -1] == -1).sum()
FP = (predictions[y_test == -1] == 1).sum()
FN = (predictions[y_test == 1] == -1).sum()
acc = (TP+TN)/(TP+TN + FP+FN)
f = 2*TP/(2*TP+FP+FN)

print('Accuracy', acc)
print('F score', f)

print('Number of leaves in 6th tree of forest:', g.n_leaves(5))
print('Maximum depth of any tree in forest:', g.current_max_depth)
print('Depth of the first tree in forest', g.get_depth(0))

importances = g.feature_importances()
plt.figure()
plt.imshow(importances.reshape(28,28), cmap = 'gray')
plt.show()
