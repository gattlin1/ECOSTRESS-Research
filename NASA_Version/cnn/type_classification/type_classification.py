from __future__ import print_function
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard
import pickle
import time
import os

if __name__=='__main__':
    num_classes = 8
    dense_layers = [1, 2]
    layer_sizes = [32, 64, 128]
    conv_layers = [1, 2]
    save_dir = os.path.join(os.getcwd(), 'saved_models')

    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    # Loading in data
    X = pickle.load(open('./data/X.pickle', 'rb'))
    y = pickle.load(open('./data/y.pickle', 'rb'))


    y = tf.keras.utils.to_categorical(y, num_classes)
    X = X / 255

    for dense_layer in dense_layers:
        for layer_size in layer_sizes:
            for conv_layer in conv_layers:
                NAME = f'{conv_layer}-conv-{layer_size}-nodes-{dense_layer}-dense-{int(time.time())}.h5'

                # Setting up callbacks for model
                tensorboard = TensorBoard(log_dir=f'logs\\15x300-images\\{NAME}')
                es = EarlyStopping(monitor='val_loss', patience=2, min_delta=0.0001)
                mcp_save = ModelCheckpoint(f'{save_dir}/{NAME}', save_best_only=True, monitor='val_loss', mode='min')

                model = Sequential()

                model.add(Conv2D(layer_size, (3, 3), padding='same', input_shape=X.shape[1:]))
                model.add(Activation('relu'))
                model.add(Dropout(0.4))
                model.add(MaxPooling2D(pool_size=(2,2)))

                for i in range(conv_layer - 1):
                    model.add(Conv2D(layer_size, (3, 3)))
                    model.add(Activation('relu'))
                    model.add(MaxPooling2D(pool_size=(2,2)))

                model.add(Flatten())
                for i in range(dense_layer):
                    model.add(Dense(512))
                    model.add(Activation('relu'))
                    model.add(Dropout(0.4))

                model.add(Dense(num_classes))
                model.add(Activation('softmax'))

                # Setting up model for training.
                model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

                # Training model
                model.fit(X, y, batch_size=32, epochs=25, validation_split=0.2, callbacks=[tensorboard, es, mcp_save])
