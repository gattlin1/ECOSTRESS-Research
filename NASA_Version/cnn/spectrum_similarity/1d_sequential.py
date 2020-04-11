from __future__ import print_function
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv1D, MaxPooling1D, GlobalAveragePooling1D, LeakyReLU, GaussianNoise
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard
from sklearn.utils import class_weight
import numpy as np
import pickle
import time
import os

if __name__=='__main__':
    num_classes = 2
    dense_layer_sizes = [64] #[32, 64, 128, 256]
    dense_layers = [3] #[1, 2]
    conv_layer_sizes = [32] #[32, 64, 128]
    conv_layers = [2] #[1, 2]
    save_dir = os.path.join(os.getcwd(), 'saved_models')

    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    # Loading in data
    X = pickle.load(open('./data/X_train.pickle', 'rb'))
    y = pickle.load(open('./data/y_train.pickle', 'rb'))

    n_timesteps, n_features = X.shape[1], X.shape[2]

    # calculating bias
    class_weights = class_weight.compute_class_weight('balanced', np.unique(y), y)

    #y = tf.keras.utils.to_categorical(y, num_classes)

    NAME = '1d-sequential.h5'

    # Setting up callbacks for model
    tensorboard = TensorBoard(log_dir=f'logs\\sequential\\{NAME}')
    es = EarlyStopping(monitor='val_loss', patience=2, min_delta=0.0001)
    mcp_save = ModelCheckpoint(f'{save_dir}/{NAME}',
                                save_best_only=True,
                                monitor='val_loss', mode='min')
    model = Sequential()
    model.add(Conv1D(filters=64, kernel_size=3, input_shape=(n_timesteps,n_features)))
    model.add(Activation('relu'))
    model.add(Conv1D(filters=64, kernel_size=3))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))

    model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())
    model.add(Dense(100))
    model.add(Activation('relu'))
    model.add(Dense(1, activation='sigmoid'))

    # Setting up model for training.
    model.compile(loss='binary_crossentropy',
                optimizer='adam', metrics=['accuracy'])

    # Training model
    model.fit(X, y, batch_size=32, epochs=50, validation_split=0.2,
            callbacks=[tensorboard, es, mcp_save],
            class_weight=class_weights)

    # Save model and weights
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    model_path = os.path.join(save_dir, NAME)
    model.save(model_path)

    print('Saved trained model at %s ' % model_path)
