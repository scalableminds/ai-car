from __future__ import print_function
import os, os.path
import numpy as np
import cv2
import load_data

# pylint: disable=C0103
batch_size = 128
num_classes = 4
epochs = 7

train_dir = './data/train/'
test_dir = './data/test/'
train_classes_name = './data/train/classes.csv'
test_classes_name = './testdata/classes.csv'
outfile_name = './model.h5'

def load_data_from_files():
   x_train, y_train = load_data.load_data(train_classes_name, train_dir)
   x_test, y_test = load_data.load_data(test_classes_name, test_dir)
   return (x_train, y_train), (x_test, y_test)

# input image dimensions
img_rows, img_cols = 50, 100

# the data, shuffled and split between train and test sets
(x_train, y_train), (x_test, y_test) = load_data_from_files()


# this takes way too long
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K

print('Imported modules')

if K.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
    x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
else:
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255

print('x_train shape:', x_train.shape)
print('y_train shape:', y_train.shape)
print('x_test shape:', x_test.shape)
print('y_test shape:', y_test.shape)

#MODEL 
model = Sequential()
model.add(Conv2D(12, kernel_size=(5, 5),
                 activation='relu',
                 input_shape=input_shape))
model.add(Conv2D(16, (5, 5), activation='relu'))
#model.add(Conv2D(48, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
#model.add(Dense(256, activation='sigmoid'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(num_classes, activation='sigmoid'))

print('Compiling model')

model.compile(loss=keras.losses.binary_crossentropy,
              optimizer='adam',
              metrics=['accuracy'])

print('Done compiling, starting training')
model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          shuffle=True,
          verbose=1)
score = model.evaluate(x_test, y_test, verbose=1)

model.save(outfile_name)

print('Test loss:', score[0])
print('Test accuracy:', score[1])
