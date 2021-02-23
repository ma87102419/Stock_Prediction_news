#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
import random
from random import sample


# In[6]:


up = pd.read_csv("/Users/pangyuan/Desktop/up2三天_output.csv")
down = pd.read_csv("/Users/pangyuan/Desktop/down2三天_output.csv")


# In[7]:


up_word = pd.read_csv("/Users/pangyuan/Desktop/up_diff-2.csv")
down_word = pd.read_csv("/Users/pangyuan/Desktop/down_diff-2.csv")
same_word = pd.read_csv("/Users/pangyuan/Desktop/same.csv")


# In[8]:


up["Target"] = 1
down["Target"] = 0
all_data = pd.concat([up,down])
all_data = all_data.dropna()

final_data = all_data.sample(n = 100000)
Target = final_data["Target"]


# In[9]:


words = []
for i in up_word:
    words.append(i)
for i in down_word:
    words.append(i)
for i in same_word:
    words.append(i)


# In[10]:


z = []
for i in (final_data["title"] + final_data["content"]):
    y = []
    for j in words:
        x = 0
        if j in i:
            x += i.count(j)
        y.append(x)
    z.append(y)


# In[11]:


from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import numpy as np


# In[12]:


train_data , test_data , train_label , test_label = train_test_split(z, Target,test_size=0.2)


# In[11]:


knn = KNeighborsClassifier()


# In[12]:


knn.fit(train_data,train_label)


# In[13]:


pre = (knn.predict(test_data))


# In[14]:


list1 = list(test_label)
list2 = list(pre)


# In[15]:


cc = 0
ww = 0
cw = 0
wc = 0

for i in range(len(list1)):
    if (list1[i] == list2[i]) and (list1[i] == 1):
        cc += 1
    elif (list1[i] == list2[i]) and (list1[i] == 0):
        ww += 1
    elif (list1[i] == 0) and (list1[i]!= list2[i]):
        wc += 1
    else:
        cw += 1


# In[17]:


print(cc, ww, cw, wc)
print((cc+ww)/20000)


# In[13]:


# vectorize
def vectorize_sequences(sequences, dimension = 1000):
    results = np.zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.
    return results


# In[16]:


x_train = vectorize_sequences(z)
y_train = np.asarray(Target).astype('float32')


# In[24]:


from keras import models
from keras import layers

model = models.Sequential()
model.add(layers.Dense(16, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))


# In[25]:


from keras import optimizers
model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])


# In[26]:


x_val = x_train[:20000]
partial_x_train = x_train[20000:80000]
y_val = y_train[:20000]
partial_y_train = y_train[20000:80000]


# In[27]:


history = model.fit(partial_x_train,
                    partial_y_train,
                    epochs=10,
                    batch_size=512,
                    validation_data=(x_val, y_val))


# In[28]:


a = model.predict(x_train[80000:])


# In[29]:


for i in a :
    print(i)


# In[ ]:





# In[ ]:




