from __future__ import print_function
import tensorflow as tf
import keras
from keras.datasets import cifar10
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
import pickle
import os

if __name__=='__main__':
    num_classes = 8
    model_name = 'ecospec.video.h5'
    save_dir = os.path.join(os.getcwd(), 'saved_models')

    X = pickle.load(open('../X.pickle', 'rb'))
    y = pickle.load(open('../y.pickle', 'rb'))


    y = keras.utils.to_categorical(y, num_classes)
    X = X / 255


    model = Sequential()

    model.add(Conv2D(32, (3, 3), input_shape=X.shape[1:]))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Flatten())
    model.add(Dense(32))

    model.add(Dense(num_classes))
    model.add(Activation('sigmoid'))

    model.compile(loss='categorical_crossentropy',
                optimizer='adam',
                metrics=['accuracy'])

    model.fit(X, y, batch_size=32, epochs=25, validation_split=0.2, shuffle=True)

    # Save model and weights
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    model_path = os.path.join(save_dir, model_name)
    model.save(model_path)
    print('Saved trained model at %s ' % model_path)
