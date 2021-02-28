import numpy as np
from sklearn.svm import SVC
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
print("Loading data...", flush=True)
x_trained = np.load("tfidf.npy")
y = np.load("label.npy")
x = preprocessing.scale(x_trained)
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
#print(x.mean(axis=0))
#print(x.std(axis=0))
print(len(x))
index = np.random.permutation(range(len(x)))
print("Training...", flush=True)
clf = SVC(gamma='auto', verbose=True)
#clf.fit(x[index[:240000]], y[index[:240000]])
clf.fit(X_train, y_train)
#print(clf.score(x[index[50000:60000]], y[index[50000:60000]]))
print(clf.score(X_test, y_test))
y_pred = clf.predict(X_test)
c = confusion_matrix(y_test, y_pred)
print(c)
