from itertools import chain
from pprint import pprint

import pandas as pd
import numpy as np

from keras.utils import to_categorical
from keras import models
from keras import layers
from keras.datasets import imdb


# Import the data

data = pd.read_csv("data.csv")

# Parsing the features

## Tokenize the features 

## Generate tokens for worlds

feature_list = list(data["features"])
tokenized_features_list = []

for feature in feature_list:
    tokenized_features_list.append(feature.split())

tokenized_features_list = list(chain.from_iterable(tokenized_features_list))

### Tokenized items have to be unique

tokenized_features_list = list(set(tokenized_features_list))

tokenized_features = {}
for i in range(len(tokenized_features_list)):
    tokenized_features[tokenized_features_list[i]] = i + 1


### Replacing worlds with tokens

tokenized_features_list = []

for feature in feature_list:
    tokenized_feature = []
    for world in feature.split():
        tokenized_feature.append(tokenized_features[world])
    tokenized_features_list.append(tokenized_feature)


## Padding the vectors so that they will have the same length 

### Having the max length

max_length = len(max(tokenized_features_list, key=len))

for vector in tokenized_features_list:
    while len(vector) < 6:
        vector.append(0)

# Tokenizing labels

labels_list = list(data["labels"])

tokenized_labels = {
    "yes": 1,
    "no": 0,
    "maybe": 0.5
}

tokenized_labels_list = []

for label in labels_list:
    tokenized_labels_list.append(tokenized_labels[label])

data = np.array(tokenized_features_list)
targets = np.array(tokenized_labels_list)

# Printing details

print("Categories:", np.unique(targets))
print("Number of unique words:", len(np.unique(np.hstack(data))))

length = [len(i) for i in data]
print("Average Review length:", np.mean(length))
print("Standard Deviation:", round(np.std(length)))

print("Label:", targets[0])

# Decoding the data

reverse_tokenized_features = dict([(value, key) for (key, value) in tokenized_features.items()]) 
decoded = " ".join( [reverse_tokenized_features.get(i, "") for i in data[0]] )
print(data[0])
print(decoded) 

# Prepare the data

test_input = data[169:]
test_output = targets[169:]

train_input = data[:169]
train_output = targets[:169]

# Building and Training the Model

model = models.Sequential()

## Input - Layer
model.add(layers.Dense(3, activation = "relu", input_shape=(6, )))

## Hidden - Layers
model.add(layers.Dropout(0.3, noise_shape=None, seed=None))
model.add(layers.Dense(50, activation = "relu"))
model.add(layers.Dropout(0.2, noise_shape=None, seed=None))
model.add(layers.Dense(50, activation = "relu"))

## Output- Layer
model.add(layers.Dense(1, activation = "sigmoid"))

model.summary()

# The model options and methods

model.compile(
    optimizer = "adam",
    loss = "binary_crossentropy",
    metrics = ["accuracy"]
)

# The model fitting results

results = model.fit(
    train_input, train_output,
    epochs= 20,
    batch_size = 5000,
    validation_data = (test_input, test_output)
)

print("Test-Accuracy:", np.mean(results.history["val_acc"]))