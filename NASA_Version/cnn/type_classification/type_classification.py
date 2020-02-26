from __future__ import print_function
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
import pickle
import time
import os

if __name__=='__main__':
    num_classes = 8
    dense_layers = [1, 2]
    layer_sizes = [16, 32, 64]
    conv_layers = [1, 2, 3]
    save_dir = os.path.join(os.getcwd(), 'saved_models')

    X = pickle.load(open('./data/X.pickle', 'rb'))
    y = pickle.load(open('./data/y.pickle', 'rb'))


    y = tf.keras.utils.to_categorical(y, num_classes)
    X = X / 255

    for dense_layer in dense_layers:
        for layer_size in layer_sizes:
            for conv_layer in conv_layers:
                NAME = f'{conv_layer}-conv-{layer_size}-nodes-{dense_layer}-dense-{int(time.time())}.h5'
                tensorboard = tf.keras.callbacks.TensorBoard(log_dir=f'logs\\{NAME}')

                model = Sequential()

                model.add(Conv2D(layer_size, (3, 3), input_shape=X.shape[1:]))
                model.add(Activation('relu'))
                model.add(MaxPooling2D(pool_size=(2,2)))

                for i in range(conv_layer - 1):
                    model.add(Conv2D(layer_size, (3, 3)))
                    model.add(Activation('relu'))
                    model.add(MaxPooling2D(pool_size=(2,2)))

                model.add(Flatten())
                for i in range(dense_layer):
                    model.add(Dense(32))
                    model.add(Activation('relu'))

                model.add(Dense(num_classes))
                model.add(Activation('sigmoid'))

                model.compile(loss='categorical_crossentropy',
                            optimizer='adam',
                            metrics=['accuracy'])

                model.fit(X, y, batch_size=32, epochs=25, validation_split=0.2, callbacks=[tensorboard])

                # Save model and weights
                if not os.path.isdir(save_dir):
                    os.makedirs(save_dir)
                model_path = os.path.join(save_dir, NAME)
                model.save(model_path)

                print('Saved trained model at %s ' % model_path)
