from __future__ import print_function
import os, os.path
import numpy as np
import cv2
import load_data

STEER_ONLY = True

# pylint: disable=C0103
batch_size = 128
num_classes = 3 if STEER_ONLY else 4
epochs = 20

train_dir = './data/train'
test_dir = './data/test'
outfile_name = './model.h5'

def load_dataset(directory):
    x_train, y_train = load_data.load_data(directory + "/classes.csv", directory)
    up_index = load_data.KEYS.index("UP")
    selected_rows = y_train[:, up_index] == 1
    return (x_train[selected_rows], y_train[selected_rows])


def load_data_from_files():
    return load_dataset(train_dir), load_dataset(test_dir)

# input image dimensions
img_rows, img_cols = 48, 64

# the data, shuffled and split between train and test sets
(x_train, y_train), (x_test, y_test) = load_data_from_files()

def convert_ys(old_y):

    # return np.column_stack((np.ones(len(old_y)), np.zeros(len(old_y)), np.zeros(len(old_y))))

    is_left = old_y[:, 0]
    is_right = np.logical_and(np.logical_not(is_left), old_y[:, 1])
    is_straight = np.logical_and(np.logical_not(is_left),
                                 np.logical_not(is_right))
    return np.column_stack((is_left, is_right, is_straight))

def print_y_stats(y, name):
    print("Stats for", name, ":")
    print("  Length:", len(y))
    print("  Left:", np.count_nonzero(y[:, load_data.KEYS.index('LEFT')]))
    print("  Right:", np.count_nonzero(y[:, load_data.KEYS.index('RIGHT')]))
    if STEER_ONLY:
        print("  Straight:", np.count_nonzero(y[:, 2]))
    else:
        print("  Up:", np.count_nonzero(y[:, load_data.KEYS.index('UP')]))
        print("  Down:", np.count_nonzero(y[:, load_data.KEYS.index('DOWN')]))
    print()

def get_class_weights(y):

    class_sums = y.sum(axis=0)
    class_probs = class_sums / len(y)
    class_weights = 1 / class_probs
    class_weights = class_weights / class_weights.sum()
    return {i: class_weights[i] for i in range(len(class_weights))}

if STEER_ONLY:
    y_train = convert_ys(y_train)
    y_test = convert_ys(y_test)

print_y_stats(y_train, "train")
print_y_stats(y_test, "test")

print("Class weights: ", get_class_weights(y_train))

# this takes way too long
import keras
from keras.models import Sequential
from keras.callbacks import ModelCheckpoint
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization
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
model.add(Conv2D(12, (5, 5), activation='relu',
                 input_shape=input_shape))
# model.add(BatchNormalization(axis=1))
model.add(Conv2D(16, (5, 5), activation='relu'))
# model.add(BatchNormalization(axis=1))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(12, (5, 5), activation='relu'))
# model.add(BatchNormalization(axis=1))
model.add(Conv2D(16, (5, 5), activation='relu'))
# model.add(BatchNormalization(axis=1))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
#model.add(Dense(256, activation='sigmoid'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
#model.add(Dense(32, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dropout(0.5))
last_activation = 'softmax' if STEER_ONLY else 'sigmoid'
model.add(Dense(num_classes, activation=last_activation))

print('Compiling model')

loss = keras.losses.categorical_crossentropy if STEER_ONLY else keras.losses.binary_crossentropy
model.compile(loss=loss,
              optimizer='adam',
              metrics=['accuracy'])

model.summary()

print('Done compiling, starting training')
checkpoint = ModelCheckpoint(outfile_name, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          validation_data=(x_test, y_test),
          class_weight=get_class_weights(y_train),
          shuffle=True,
          callbacks=[checkpoint],
          verbose=1)
score = model.evaluate(x_test, y_test, verbose=1)

# model.save(outfile_name)

print('Test loss:', score[0])
print('Test accuracy:', score[1])
