import numpy as np
np.random.seed(1114)
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.decomposition import PCA
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import pickle

#case = "svc"
case = "rf"

print("Loading data...", flush=True)
x = np.load("tfidf_okapi.npy")
y = np.load("label.npy")
b = np.load("boundary.npy")
print(b)

tmp = []
for i in range(x.shape[1]):
    tmp.append(np.corrcoef(x[:, i], y)[0][1])
print(np.mean(np.abs(tmp)))

print(x.shape[1])
print("PCA...", flush=True)
pca = PCA(n_components=64)
x = pca.fit_transform(x)
print(pca.explained_variance_ratio_)

tmp = []
for i in range(x.shape[1]):
    tmp.append(np.corrcoef(x[:, i], y)[0][1])
print(np.mean(np.abs(tmp)), flush=True)

x = preprocessing.scale(x)
for i in range(0,9):
    print("training: {} to {}, testing: {}".format(i + 1, i + 3, i + 4))
    X_train = x[b[i]:b[i+3]]
    y_train = y[b[i]:b[i+3]]
    if i < 8:
        X_test = x[b[i+3]:b[i+4]]
        y_test = y[b[i+3]:b[i+4]]
    else:
        X_test = x[b[i+3]:]
        y_test = y[b[i+3]:]
        

    print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

    print("Training...", flush=True)
    if case == "svc":
        clf = SVC(kernel='rbf', gamma='auto', verbose=1)
    elif case == "rf":
        clf = RandomForestClassifier(verbose=1, n_jobs=4)
    else:
        exit()
    clf.fit(X_train, y_train)
    print(clf.score(X_train, y_train))

    print("Testing...", flush=True)
    print(clf.score(X_test, y_test))
    y_pred = clf.predict(X_test)
    c = confusion_matrix(y_test, y_pred)
    print(c)
