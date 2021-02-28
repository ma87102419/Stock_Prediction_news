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
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
print(np.sum(1 - y_train), np.sum(y_train))
print(np.sum(1 - y_test), np.sum(y_test))

print(len(x))
print("Training...", flush=True)
if case == "svc":
    clf = SVC(kernel='rbf', gamma='auto', verbose=1)
elif case == "rf":
    clf = RandomForestClassifier(verbose=1, n_jobs=4)
else:
    exit()
clf.fit(X_train, y_train)
index = np.random.permutation(range(X_train.shape[0]))
print(clf.score(X_train[index[:50000]], y_train[index[:50000]]))
with open("model_{}.pkl".format(case), "wb") as f:
    pickle.dump(clf, f)

print("Testing...", flush=True)
with open("model_{}.pkl".format(case), "rb") as f:
    clf = pickle.load(f)
print(clf.score(X_test, y_test))
y_pred = clf.predict(X_test)
c = confusion_matrix(y_test, y_pred)
print(c)
