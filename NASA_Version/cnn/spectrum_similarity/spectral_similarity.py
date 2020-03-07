from __future__ import print_function
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Input, Concatenate
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import TensorBoard, EarlyStopping, ModelCheckpoint
import pickle
import time
import os
import numpy as np

def create_model(conv_layers, conv_layer_size, dense_layers, dense_layer_size, dropout, shape):
    branch = Input(shape=shape)

    x = Conv2D(conv_layer_size, (3, 3), activation='relu', input_shape=shape)(branch) # possible use leaky relu or lu
    x = MaxPooling2D(pool_size=(2,2))(x)

    for i in range(conv_layers): # also add dropouts after conv layers.
        x = Conv2D(conv_layer_size, (3, 3), activation='relu')(x)
        x = Dropout(dropout)(x)
        x = MaxPooling2D(pool_size=(2,2))(x)

    x = Flatten()(x)
    for i in range(dense_layers):
        x = Dense(dense_layer_size, activation='relu')(x)
        x = Dropout(dropout)(x)

    model = Model(branch, x)

    return model

if __name__=='__main__':
    dense_layers = [2]
    conv_sizes = [32]
    conv_layers = [1]
    dropout = 0.4
    save_dir = os.path.join(os.getcwd(), 'saved_models')
    num_classes = 2
    X_1 = pickle.load(open('./data/X_1.pickle', 'rb'))
    X_2 = pickle.load(open('./data/X_2.pickle', 'rb'))
    y = pickle.load(open('./data/y.pickle', 'rb'))

    # y = tf.keras.utils.to_categorical(y, num_classes)
    X_1 = X_1 / 255
    X_2 = X_2 / 255

    for dense_layer in dense_layers:
        for conv_size in conv_sizes:
            for conv_layer in conv_layers:
                NAME = f'{conv_layer}-conv-{conv_size}-nodes-{dense_layer}-dense.h5'

                tensorboard = TensorBoard(log_dir=f'logs\\15x300-images\\{NAME}')
                es = EarlyStopping(monitor='val_loss', patience=2, min_delta=0.0001)
                mcp_save = ModelCheckpoint(f'{save_dir}/{NAME}', save_best_only=True, monitor='val_loss', mode='min')

                # defining 2 input models for each image
                branch_1 = create_model(conv_layer, conv_size, dense_layer, 64, dropout, X_1.shape[1:])
                branch_2 = create_model(conv_layer, conv_size, dense_layer, 64, dropout, X_2.shape[1:])
                
                # combining the models
                combined = Concatenate(axis=1)([branch_1.output, branch_2.output])

                # perform a dense layer to the number of classes
                z = Dense(1)(combined)
                z = Activation('sigmoid')(z)

                # final model
                model = Model(inputs=[branch_1.input, branch_2.input], outputs=z)
                
                # sets the model up for training
                model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

                # training the model
                model.fit([X_1, X_2], y, batch_size=32, epochs=25, validation_split=0.2, callbacks=[tensorboard, es, mcp_save])

                # Save model and weights
                if not os.path.isdir(save_dir):
                    os.makedirs(save_dir)
                model_path = os.path.join(save_dir, NAME)
                model.save(model_path)

                print('Saved trained model at %s ' % model_path)


    