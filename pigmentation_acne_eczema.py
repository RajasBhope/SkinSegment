# -*- coding: utf-8 -*-
"""Pigmentation_Acne_Eczema.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AxkoLJ62vYYzmJ148RkeWE7HS37oxvGN
"""

from google.colab import drive
drive.mount('/content/drive')

#Importing Libraries
from keras.layers import Input,Dense,Flatten
from keras.models import Model
import tensorflow as tf
from tensorflow.keras import layers
from keras.applications.inception_v3 import InceptionV3

from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
import numpy as np
from glob import glob
from sklearn.model_selection import train_test_split

# re-size all the images to this
IMAGE_SIZE = [224, 224]
train_path = "/content/drive/MyDrive/Colab Notebooks/Pigmentation/train"
test_path = "/content/drive/MyDrive/Colab Notebooks/Pigmentation/test"

# add preprocessing layer to the front of Inception
incept = InceptionV3(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)


# add preprocessing layer to the front of Inception
#incept = InceptionV3(input_shape=IMAGE_SIZE + [3], weights='imagenet', classifier_activation=tf.sigmoid, include_top=False)

# don't train existing weights
for layer in incept.layers:
  layer.trainable = False

#Getting Number of Categories
folders = glob('/content/drive/MyDrive/Colab Notebooks/Pigmentation/train/*')

x = Flatten()(incept.output)
x = layers.Dense(256, 'relu', kernel_initializer='he_normal')(x)
x = layers.BatchNormalization()(x)
x = layers.Dropout(0.2)(x)

prediction = Dense(len(folders), activation='softmax')(x)

# create a model object
model = Model(inputs=incept.input, outputs=prediction)

# view the structure of the model
model.summary()

# tell the model what cost and optimization method to use
model.compile(
  loss='categorical_crossentropy',
  optimizer='adam',
  metrics=['accuracy']
)

#Data Augmentation
from keras.preprocessing.image import ImageDataGenerator

data_datagen = ImageDataGenerator(validation_split=0.09,
                                   rescale = 1./255,
                                   shear_range = 0.09,
                                   zoom_range = 0.09,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)


training_set = data_datagen.flow_from_directory('/content/drive/MyDrive/Colab Notebooks/Pigmentation/train',
                                                 target_size = (224, 224),
                                                 batch_size = 32,
                                                 class_mode = 'categorical',
                                                 subset="training")
valid_set = data_datagen.flow_from_directory(
    '/content/drive/MyDrive/Colab Notebooks/Pigmentation/train',
    target_size = (224, 224),
    batch_size = 32,
    class_mode = 'categorical',
    subset="validation"
)

test_set = test_datagen.flow_from_directory('/content/drive/MyDrive/Colab Notebooks/Pigmentation/test',
                                            target_size = (224, 224),
                                            batch_size = 32,
                                            class_mode = 'categorical')

from keras.callbacks import ModelCheckpoint

#training_set = np.asarray(training_set)
#test_set = np.asarray(test_set)
#valid_set = np.asarray(valid_set)

filepath = './my_best_model.epoch{epoch:02d}-loss{val_loss:.2f}.hdf5'

checkpoint = ModelCheckpoint(filepath=filepath,
                             monitor='loss',
                             verbose=1,
                             save_best_only=True,
                             mode='min')

callbacks = [checkpoint]

#Fit the model
history = model.fit_generator( training_set, validation_data=valid_set, epochs=50, steps_per_epoch=len(training_set),validation_steps=len(valid_set),callbacks=callbacks )

model.evaluate(test_set)

import matplotlib.pyplot as plt
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(['Training','Validation'])
plt.title('Loss')
plt.xlabel('Epoch')

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.legend(['training','validation'])
plt.title('Accuracy')
plt.xlabel('Epoch')

#fetch image
import requests
import matplotlib.pyplot as plt
from PIL import Image
url = 'https://www.shutterstock.com/image-photo/freckles-cheek-oily-skin-on-600w-1454058797.jpg'
r = requests.get(url, stream=True)
img = Image.open(r.raw)
#image size
size=(224,224)
#resize image
out = img.resize(size)
img_arr = np.argmax(out)
#img_arr = np.array(img).reshape(1,224, 224 ,3)
#img_arr =np.argmax(img.resize(1,224,224,3),axis=1)

plt.imshow(out, cmap=plt.get_cmap('gray'))

pred = np.argmax(model.predict(out))
#pred = np.argmax(model.predict(test_set[1][0][1].reshape(1,224,224,3)),axis=-1)
print("predicted sign: "+ str(pred))

test_set[0]

from tensorflow.keras.utils import plot_model
plot_model(model, show_shapes=True, expand_nested=True)

!pip install visualkeras

import keras
import tensorflow as tf
import visualkeras
from tensorflow import keras
from keras.models import Sequential
from tensorflow.keras.layers import Input, Conv2D, Dense, Flatten, Dropout
from tensorflow.keras.layers import GlobalMaxPooling2D, MaxPooling2D
from tensorflow.keras.models import Model
from tensorflow.keras import regularizers, optimizers

visualkeras.layered_view(model, legend=True) # without custom font
from PIL import ImageFont
font = ImageFont.load_default()

visualkeras.layered_view(model, legend=True, font=font) # selected font











import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
from PIL import Image
from skimage.transform import resize
from random import shuffle

list_train = "/content/drive/MyDrive/Colab Notebooks/Pigmentation/train"


list_test = "/content/drive/MyDrive/Colab Notebooks/Pigmentation/test"
list_train = list_train
list_test = list_test
index = [os.path.basename(filepath) for filepath in list_test]

from keras.preprocessing.image import ImageDataGenerator
from keras.applications.inception_v3 import preprocess_input
train_idg = ImageDataGenerator(validation_split=0.09,
                                   rescale = 1./255,
                                   shear_range = 0.09,
                                   zoom_range = 0.09,
                                   horizontal_flip = True)
train_gen = train_idg.flow_from_directory('/content/drive/MyDrive/Colab Notebooks/Pigmentation/train',
                                                 target_size = (224, 224),
                                                 batch_size = 32,
                                                 class_mode = 'categorical',
                                                 subset="training")



test_datagen = ImageDataGenerator(rescale = 1./255)


# valid_set = data_datagen.flow_from_directory(
#     '/content/drive/MyDrive/Colab Notebooks/Pigmentation/train',
#     target_size = (224, 224),
#     batch_size = 32,
#     class_mode = 'categorical',
#     subset="validation"
# )

from keras.models import Sequential
from keras.models import Model
from keras.callbacks import ModelCheckpoint, LearningRateScheduler, EarlyStopping, ReduceLROnPlateau, TensorBoard
from keras import optimizers, losses, activations, models
from keras.layers import Convolution2D, Dense, Input, Flatten, Dropout, MaxPooling2D, BatchNormalization, GlobalAveragePooling2D, Concatenate
from keras import applications
input_shape = (224, 224, 3)
nclass = len(train_gen.class_indices)

base_model = applications.InceptionV3(weights='imagenet',
                                include_top=False,
                                input_shape=(224, 224,3))
base_model.trainable = False

add_model = Sequential()
add_model.add(base_model)
add_model.add(GlobalAveragePooling2D())
add_model.add(Dropout(0.5))
add_model.add(Dense(nclass,
                    activation='softmax'))

model = add_model
model.compile(loss='categorical_crossentropy',
              optimizer=optimizers.SGD(lr=1e-4,
                                       momentum=0.9),
              metrics=['accuracy'])
model.summary()

file_path="weights.best.hdf5"

checkpoint = ModelCheckpoint(file_path, monitor='acc', verbose=1, save_best_only=True, mode='max')

early = EarlyStopping(monitor="acc", mode="max", patience=15)

callbacks_list = [checkpoint, early] #early

history = model.fit_generator(train_gen,
                              epochs=2,
                              shuffle=True,
                              verbose=True,
                              callbacks=callbacks_list)

# model.load_weights(file_path)

test_idg = ImageDataGenerator(preprocessing_function=preprocess_input)
test_gen = test_idg.flow_from_directory('/content/drive/MyDrive/Colab Notebooks/Pigmentation/test',
                                            target_size = (224, 224),
                                            batch_size = 32,
                                            class_mode = 'categorical')
len(test_gen.filenames)

predicts = model.predict_generator(test_gen, verbose = True, workers = 2)

predicts = np.argmax(predicts,
                     axis=1)
label_index = {v: k for k,v in train_gen.class_indices.items()}
predicts = [label_index[p] for p in predicts]

df = pd.DataFrame(columns=['fname', 'camera'])
df['fname'] = [os.path.basename(x) for x in test_gen.filenames]
df['camera'] = predicts
df.to_csv("sub1.csv", index=False)

