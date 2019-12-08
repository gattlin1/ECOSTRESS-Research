from __future__ import print_function
import keras
from keras.datasets import cifar10
from keras.models import Sequential, load_model
import os

if __name__=='__main__':
    model = load_model('./saved_models/keras_cifar10_trained_model.h5')

    # The data, split between train and test sets:
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()

    y_test = keras.utils.to_categorical(y_test, 10)
    x_test = x_test.astype('float32')
    x_test /= 255

    # Score trained model.
    scores = model.evaluate(x_test, y_test, verbose=1)
    print('Test loss:', scores[0])
    print('Test accuracy:', scores[1])