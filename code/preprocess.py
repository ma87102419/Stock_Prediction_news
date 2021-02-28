import csv
import numpy as np
title = []
text = []
month = []
y = []
print("Reading file...", flush=True)
with open(file='./down2三天_output.csv', mode="r", encoding="utf-8") as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        title.append(row[1])
        text.append(row[2])
        month.append(int(row[0].split('/')[1]))
        y.append(1)

with open(file='./up2三天_output.csv', mode="r", encoding="utf-8") as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        title.append(row[1])
        text.append(row[2])
        month.append(int(row[0].split('/')[1]))
        y.append(0)

_, b = np.unique(month, return_counts=True)
b = np.concatenate((np.array([0]), np.cumsum(b)[:-1]))
np.save("boundary.npy", b)
print(b)

print("Reading keyword...", flush=True)
keyword_set = set()
with open(file='./up.csv', mode="r", encoding="utf-8") as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        for keyword in row:
            keyword_set.add(keyword)

with open(file='./down.csv', mode="r", encoding="utf-8") as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        for keyword in row:
            keyword_set.add(keyword)

keyword_list = list(keyword_set)
print(len(keyword_list))

print("Counting TF...", flush=True)
tf = []
for i in range(len(title)):
    temp = []
    for j in range(len(keyword_list)):
        title_tf = title[i].count(keyword_list[j])
        text_tf = text[i].count(keyword_list[j])
        temp.append(title_tf + text_tf)

    tf.append(temp)
    if i % 10000 == 0:
        print(i, flush=True)

print("Making TFIDF...", flush=True)
tf = np.array(tf)
df = np.sum(np.where(tf > 0, 1, 0), axis=0) #取代：把tf>0的變成1，否則變成0

zero_index = np.where(df == 0)[0] #找0的位置
tf = np.delete(tf, zero_index, axis=1)
df = np.delete(df, zero_index)

df = df.reshape((1, df.shape[0]))
d = np.array([len(title[i]) + len(text[i]) for i in range(len(title))])
d = d.reshape((d.shape[0] , 1))
print(tf.shape, df.shape, d.shape)
avg_d = np.mean(d)
N = len(title)
k=1.6
b=0.75
idf = np.log((N - df + 0.5) / (df + 0.5))
tfidf = ((k + 1) * tf) / (k * (1 - b + b * (d / avg_d)) + tf) * idf  #用okapi pm25算tf-idf
print(idf.shape, tfidf.shape)

print(tfidf.shape)
'''
N = len(title)
idf = np.log(N /df)
tfidf = tf * idf
'''
index = np.argsort(month)
np.save("tfidf_okapi.npy", tfidf[index])
np.save("label.npy", np.array(y)[index])
