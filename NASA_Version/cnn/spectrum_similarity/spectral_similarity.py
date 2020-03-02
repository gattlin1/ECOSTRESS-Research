from __future__ import print_function
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Input, Concatenate
from tensorflow.keras.layers import Conv2D, MaxPooling2D
import pickle
import time
import os

def create_model(layer_size):
    model = Sequential()

    model.add(Conv2D(layer_size, (3, 3), input_shape=X.shape[1:]))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Conv2D(layer_size, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Flatten())
    model.add(Dense(32))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))

    return model


if __name__=='__main__':
    NAME = 'spect-simil-model.h5'
    save_dir = os.path.join(os.getcwd(), 'saved_models')
    num_classes = 2
    X = pickle.load(open('./data/X.pickle', 'rb'))
    y = pickle.load(open('./data/y.pickle', 'rb'))


    tensorboard = tf.keras.callbacks.TensorBoard(log_dir=f'logs\\{NAME}')

    branch_1 = create_model(32)
    branch_2 = create_model(32)

    combined = Concatenate([branch_1, branch_2])

    combined_model = Sequential()
    combined_model.add(combined)

    combined_model.add(Dense(num_classes))
    combined_model.add(Activation('softmax'))

    combined_model.compile(loss='binary_crossentropy',
                            optimizer='adam',
                            metrics=['accuracy'])

    combined_model.fit([X[:, 0], X[:, 1]], y, batch_size=32, epochs=25, validation_split=0.2, callbacks=[tensorboard])

    # Save model and weights
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    model_path = os.path.join(save_dir, NAME)
    combined_model.save(model_path)

    print('Saved trained model at %s ' % model_path)


    