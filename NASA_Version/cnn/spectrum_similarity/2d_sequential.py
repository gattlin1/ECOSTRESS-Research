from __future__ import print_function
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D, LeakyReLU, GaussianNoise
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard
from sklearn.utils import class_weight
import numpy as np
import pickle
import time
import os

if __name__=='__main__':
    num_classes = 2
    dense_layer_sizes = [32] #[32, 64, 128, 256]
    dense_layers = [1] #[1, 2]
    conv_layer_sizes = [32] #[32, 64, 128]
    conv_layers = [1] #[1, 2]
    save_dir = os.path.join(os.getcwd(), 'saved_models')

    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    # Loading in data
    X = pickle.load(open('./data/X_train_2d.pickle', 'rb'))
    y = pickle.load(open('./data/y_train_2d.pickle', 'rb'))

    # calculating bias
    class_weights = class_weight.compute_class_weight('balanced', np.unique(y), y)

    #y = tf.keras.utils.to_categorical(y, num_classes)

    for dense_layer in dense_layers:
        for dense_size in dense_layer_sizes:
            for conv_size in conv_layer_sizes:
                for conv_layer in conv_layers:
                    NAME = '2d-sequential.h5'#f'sequential-{conv_layer}-conv-{conv_size}-conv nodes-' \
                           #f'{dense_layer}-dense-{dense_size}-dense nodes.h5'

                    # Setting up callbacks for model
                    tensorboard = TensorBoard(log_dir=f'logs\\sequential\\{NAME}')
                    es = EarlyStopping(monitor='val_loss', patience=2, min_delta=0.0001)
                    mcp_save = ModelCheckpoint(f'{save_dir}/{NAME}',
                                                save_best_only=True,
                                                monitor='val_loss', mode='min')

                    model = Sequential()
                    model.add(Conv2D(conv_size, (3,3),
                                    padding='same', input_shape=X.shape[1:],
                                    data_format='channels_first'))
                    model.add(LeakyReLU(alpha=0.1))
                    model.add(Dropout(0.4))
                    model.add(MaxPooling2D(pool_size=(2,2)))
                    model.add(LeakyReLU(alpha=0.1))

                    for i in range(conv_layer):
                        model.add(Conv2D(conv_size, (3,3)))
                        model.add(LeakyReLU(alpha=0.1))
                        model.add(Dropout(0.4))
                        model.add(MaxPooling2D(pool_size=(2,2)))
                        model.add(GaussianNoise(0.5))
                        model.add(LeakyReLU(alpha=0.1))

                    model.add(Flatten())
                    for i in range(dense_layer):
                        model.add(Dense(dense_size))
                        model.add(LeakyReLU(alpha=0.1))
                        model.add(Dropout(0.4))

                    model.add(Dense(1, activation='sigmoid'))

                    # Setting up model for training.
                    model.compile(loss='binary_crossentropy',
                                optimizer='adam', metrics=['accuracy'])

                    # Training model
                    model.fit(X, y, batch_size=32, epochs=50, validation_split=0.2,
                            callbacks=[tensorboard, es, mcp_save],
                            class_weight=class_weights)
