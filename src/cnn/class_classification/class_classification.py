# Authors: Gattlin Walker
# Keras Sequential CNN used to classify a ECOSTRESS spectrum by it's class.

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D,\
                                    MaxPooling2D, LeakyReLU, GaussianNoise
from tensorflow.keras.callbacks import EarlyStopping, TensorBoard
from sklearn.utils import class_weight
import numpy as np
import pickle
import time
import os

if __name__=='__main__':
    num_classes = 51
    dense_layer_sizes = [32, 64, 128, 256]
    dense_layers = [1, 2]
    conv_layer_sizes = [16, 32, 64]
    conv_layers = [1, 2]
    alpha_vals = [0.01, 0.1] # [0.01, 0.1, 0.2, 0.3]
    save_dir = os.path.join(os.getcwd(), 'saved_models')

    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    # Loading in data
    X = pickle.load(open('./data/X.pickle', 'rb'))
    y = pickle.load(open('./data/y.pickle', 'rb'))

    # calculating bias
    class_weights = class_weight.compute_class_weight('balanced',
        np.unique(y), y)

    y = tf.keras.utils.to_categorical(y, num_classes)
    X = X / 255

    for dense_layer in dense_layers:
        for dense_size in dense_layer_sizes:
            for conv_size in conv_layer_sizes:
                for conv_layer in conv_layers:
                    for alpha_val in alpha_vals:
                        NAME = f'same-padding-{conv_layer}-conv-{conv_size}-' \
                            f'conv nodes-{dense_layer}-dense-{dense_size}-' \
                            f'dense nodes-{alpha_val}-alpha val.h5'

                        # Setting up callbacks for model
                        tensorboard = TensorBoard(log_dir=f'logs\\{NAME}')
                        es = EarlyStopping(monitor='val_loss', patience=2,
                            min_delta=0.0001)

                        model = Sequential()
                        model.add(Conv2D(conv_size, (3,3), padding='same',
                            input_shape=X.shape[1:]))
                        model.add(LeakyReLU(alpha=alpha_val))
                        model.add(Dropout(0.4))
                        model.add(MaxPooling2D(pool_size=(2,2), padding='same'))
                        model.add(LeakyReLU(alpha=alpha_val))

                        for i in range(conv_layer):
                            model.add(Conv2D(conv_size, (3,3), padding='same'))
                            model.add(LeakyReLU(alpha=alpha_val))
                            model.add(Dropout(0.4))
                            model.add(MaxPooling2D(pool_size=(2,2),
                                padding='same'))
                            model.add(LeakyReLU(alpha=alpha_val))

                        model.add(Flatten())
                        for i in range(dense_layer):
                            model.add(Dense(dense_size))
                            model.add(LeakyReLU(alpha=alpha_val))
                            model.add(Dropout(0.4))

                        model.add(Dense(num_classes, activation='softmax'))

                        # Setting up model for training.
                        model.compile(loss='categorical_crossentropy',
                                    optimizer='adam', metrics=['accuracy'])

                        # Training model
                        model.fit(X, y, batch_size=32, epochs=100,
                            validation_split=0.2, callbacks=[tensorboard, es],
                            class_weight=class_weights)
